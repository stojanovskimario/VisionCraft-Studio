

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


RESAMPLE = Image.Resampling.LANCZOS


def _smooth(x):
    x = max(0.0, min(1.0, float(x)))
    return x * x * (3.0 - 2.0 * x)


def _sample_time(t, duration, fps):
    return max(0.0, min(float(t), max(0.0, duration - 1.0 / max(fps, 1.0))))


def _get(get_frame, t, clip):
    return Image.fromarray(
        np.asarray(get_frame(_sample_time(t, clip.duration, clip.fps or 24)), dtype=np.uint8)
    ).convert('RGB')


def _fit(image, size):
    return ImageOps.fit(image, (max(1, int(size[0])), max(1, int(size[1]))), method=RESAMPLE)


def _font(size):
    try:
        return ImageFont.truetype('DejaVuSans.ttf', max(10, int(size)))
    except OSError:
        return ImageFont.load_default()


def _gradient(size, upper, lower):
    w, h = size
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    a = np.asarray(upper, dtype=np.float32)[None, None, :]
    b = np.asarray(lower, dtype=np.float32)[None, None, :]
    return Image.fromarray(np.uint8(np.clip(np.broadcast_to(a * (1 - yy) + b * yy, (h, w, 3)), 0, 255)))


def _rounded_photo(canvas, frame, bounds, radius, border, border_color, shadow=True):
    x0, y0, x1, y1 = map(int, bounds)
    w, h = x1 - x0, y1 - y0
    if w < 2 or h < 2:
        return
    if shadow:
        sh = max(2, border * 2)
        ImageDraw.Draw(canvas).rounded_rectangle(
            [x0 + sh // 3, y0 + sh // 3, x1 + sh // 3, y1 + sh // 3],
            radius=radius, fill=(4, 9, 17),
        )
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=tuple(border_color))
    inset = max(2, int(border))
    iw, ih = w - 2 * inset, h - 2 * inset
    if iw <= 0 or ih <= 0:
        return
    photo = _fit(frame, (iw, ih))
    mask = Image.new('L', (iw, ih), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, iw - 1, ih - 1], radius=max(1, radius - inset), fill=255)
    canvas.paste(photo, (x0 + inset, y0 + inset), mask)


def _label(canvas, text, xy, bg, fg, font_size, pad=None):
    draw = ImageDraw.Draw(canvas)
    f = _font(font_size)
    pad = max(4, font_size // 3) if pad is None else pad
    bb = draw.textbbox((0, 0), text, font=f)
    width, height = bb[2] - bb[0], bb[3] - bb[1]
    x, y = xy
    draw.rounded_rectangle([x, y, x + width + 2 * pad, y + height + 2 * pad], radius=max(3, pad), fill=tuple(bg))
    draw.text((x + pad, y + pad - bb[1]), text, fill=tuple(fg), font=f)



def _build_filmstrip(clip, cfg):
    w, h = clip.size
    samples = int(cfg["frame_count"])
    gap = max(4, int(w * cfg["panel_gap_ratio"]))
    pane_w = max(40, int(w * cfg["panel_width_ratio"]))
    pane_h = max(40, int(h * cfg["panel_height_ratio"]))
    top = (h - pane_h) // 2
    step = pane_w + gap
    film_w = samples * step

    base = Image.new("RGBA", (film_w, h), tuple(cfg["film_color"]) + (255,))
    d = ImageDraw.Draw(base)

    rail = max(8, int(h * cfg["rail_height_ratio"]))
    d.rectangle([0, 0, film_w, rail], fill=tuple(cfg["rail_color"]) + (255,))
    d.rectangle([0, h - rail, film_w, h], fill=tuple(cfg["rail_color"]) + (255,))

    hole_w = max(7, int(w * 0.014))
    hole_h = max(5, int(rail * 0.32))
    hole_step = max(16, int(w * 0.052))

    for x in range(0, film_w, hole_step):
        for yy in (int(rail * 0.20), h - rail + int(rail * 0.20)):
            d.rounded_rectangle(
                (x, yy, x + hole_w, yy + hole_h),
                radius=2,
                fill=tuple(cfg["hole_color"]) + (255,)
            )

    for i in range(samples):
        ts = clip.duration * ((i + 0.5) / samples)
        snap = Image.fromarray(
            np.asarray(
                clip.get_frame(_sample_time(ts, clip.duration, clip.fps or 24)),
                dtype=np.uint8,
            )
        ).convert("RGB")

        x = i * step + gap // 2
        border = max(3, int(h * cfg["frame_border_ratio"]))

        _rounded_photo(
            base,
            snap,
            (x, top, x + pane_w, top + pane_h),
            4,
            border,
            cfg["frame_color"],
            shadow=False,
        )

        _label(
            base,
            f"FRAME {i + 1:02}",
            (
                x + border,
                min(
                    h - rail - int(h * 0.035),
                    top + pane_h + int(h * 0.012),
                ),
            ),
            cfg["film_color"],
            cfg["text_color"],
            max(10, int(h * 0.021)),
        )

    live_slot = max(0, min(samples - 1, int(cfg["live_slot"])))
    live_x = live_slot * step + gap // 2
    border = max(3, int(h * cfg["frame_border_ratio"]))
    inside_rect = (
        live_x + border,
        top + border,
        pane_w - 2 * border,
        pane_h - 2 * border,
    )


    tilt = float(cfg.get("tilt_degrees", 5.0))

    vertical_offset = int(
        h * cfg.get("vertical_offset_ratio", 0.0)
    )

    tilt_radians = math.radians(tilt)

    padding = (
        int(
            max(w, h)
            * abs(math.sin(tilt_radians))
        )
        + 24
    )

    stage_size = (
        w + 2 * padding,
        h + 2 * padding,
    )

    def render(get_frame, t):
        strip = base.copy()

        current = _get(get_frame, t, clip)

        ix, iy, iw, ih = inside_rect

        strip.paste(
            _fit(current, (iw, ih)),
            (ix, iy),
        )

        stage = Image.new(
            "RGBA",
            stage_size,
            tuple(cfg["film_color"]) + (255,),
        )

        offset = int(
            cfg["scroll_pixels_per_second"]
            * w / 1280.0
            * t
        ) % film_w

        x = padding - offset - film_w

        while x < stage.width:
            y = padding - h + vertical_offset

            while y < stage.height:
                stage.paste(
                    strip,
                    (x, y),
                )
                y += h

            x += film_w

        angled = stage.rotate(
            tilt,
            resample=Image.Resampling.BICUBIC,
            expand=False,
        )

        result = angled.crop(
            (
                padding,
                padding,
                padding + w,
                padding + h,
            )
        )

        return np.asarray(
            result.convert("RGB")
        )

    return render


def _build_time_windows(clip, cfg):
    w, h = clip.size
    margin = max(8, int(w * cfg['margin_ratio']))
    gap = max(6, int(w * cfg['gap_ratio']))
    left_w = int((w - 2 * margin - gap) * cfg['hero_width_ratio'])
    right_x = margin + left_w + gap
    right_w = w - margin - right_x
    full_h = h - margin * 2
    right_h = (full_h - gap) // 2
    lw = max(2, int(min(w, h) * cfg['stroke_ratio']))
    r = max(6, int(h * cfg['corner_ratio']))
    delay = cfg['time_offset_seconds']
    labels = tuple(cfg['labels'])

    def render(get_frame, t):
        background = _get(get_frame, t, clip)

        background = background.filter(
            ImageFilter.GaussianBlur(
                radius=max(3, int(h * cfg.get("background_blur_ratio", 0.035)))
            )
        )

        dark_overlay = Image.new("RGB", (w, h), (0, 0, 0))

        canvas = Image.blend(
            background,
            dark_overlay,
            cfg.get("background_darkness", 0.30)
        )
        panes = [
            ((margin, margin, margin + left_w, margin + full_h), _get(get_frame, t, clip), cfg['hero_border_color'], labels[0]),
            ((right_x, margin, w - margin, margin + right_h), _get(get_frame, t - delay, clip), cfg['side_border_color'], labels[1]),
            ((right_x, margin + right_h + gap, w - margin, h - margin), _get(get_frame, t + delay, clip), cfg['side_border_color'], labels[2]),
        ]
        for (x0, y0, x1, y1), frame, color, caption in panes:
            _rounded_photo(canvas, frame, (x0, y0, x1, y1), r, lw, color, shadow=True)
            _label(canvas, caption, (x0 + 2 * lw + 5, y0 + 2 * lw + 5), cfg['label_background'], color, max(10, h * cfg['label_size_ratio']))
        return np.asarray(canvas)

    return render


def _page_turn_timeline(clip, cfg):
    turn_duration = max(
        0.15,
        float(cfg["turn_duration_seconds"])
    )

    skip = max(
        0.0,
        float(cfg.get("time_skip_seconds", 0.0))
    )

    fps = float(clip.fps or 24)

    safe_end = max(
        0.0,
        float(clip.duration) - 1.0 / fps
    )

    turns = []
    cumulative_skip = 0.0

    for start in sorted(
        set(float(v) for v in cfg["turn_times_seconds"])
    ):
        if start < 0:
            continue

        if (
            start
            + turn_duration
            + cumulative_skip
            + skip
        ) > safe_end:
            continue

        turns.append(start)
        cumulative_skip += skip

    def mapped_time(t):
        values = np.asarray(t, dtype=np.float64)
        result = values.copy()

        for start in turns:
            cut_time = start + turn_duration * 0.5
            result = result + skip * (values >= cut_time)

        if result.ndim == 0:
            return float(result)

        return result

    output_duration = (
        float(clip.duration) - cumulative_skip
    )

    return (
        turns,
        turn_duration,
        mapped_time,
        output_duration,
    )


def _build_page_turn(clip, cfg):
    w, h = clip.size

    times, duration, mapped_time, _ = (
        _page_turn_timeline(clip, cfg)
    )

    max_fold = max(
        3,
        int(w * cfg["fold_width_ratio"])
    )

    curve = float(cfg["curl_curve_ratio"])
    shadow_strength = float(cfg["shadow_strength"])
    highlight = float(cfg["edge_highlight"])

    shadow_width = max(
        3,
        int(w * cfg["shadow_width_ratio"])
    )

    x = np.arange(w, dtype=np.float32)[None, :]

    y = np.linspace(
        -1.0, 1.0, h, dtype=np.float32
    )[:, None]

    row_index = np.arange(h)[:, None]


    def render(get_frame, t):
        active = next(
            (
                (index, (t - start) / duration)
                for index, start in enumerate(times)
                if start <= t < start + duration
            ),
            None,
        )

        if active is None:
            return np.asarray(
                _get(get_frame, mapped_time(t), clip),
                dtype=np.uint8,
            )

        index, phase = active
        skip = max(
            0.0,
            float(cfg.get("time_skip_seconds", 0.0))
        )

        source_time = t + index * skip

        current = np.asarray(
            _get(get_frame, source_time, clip),
            dtype=np.uint8,
        )

        revealed = np.asarray(
            _get(get_frame, source_time + skip, clip),
            dtype=np.uint8,
        )

        progress = _smooth(phase)
        bend = math.sin(math.pi * progress)

        edge = np.clip(
            w * (1.0 - progress)
            + w * curve * bend * (1.0 - y ** 2),
            0.0,
            float(w),
        )

        output = revealed.copy()

        front = x < edge
        output[front] = current[front]

        fold_width = max(
            0,
            round(max_fold * bend),
        )

        distance = x - edge

        if fold_width > 1:
            fold_region = (
                (distance >= 0)
                & (distance < fold_width)
            )

            mirrored_x = np.clip(
                2.0 * edge - x - 1,
                0,
                w - 1,
            ).astype(np.int32)

            underside = current[
                row_index,
                mirrored_x,
            ]

            shade = (
                1.07
                - 0.52
                * np.clip(
                    distance / fold_width,
                    0.0,
                    1.0,
                )
            )

            folded = np.clip(
                underside * shade[..., None]
                + highlight,
                0,
                255,
            ).astype(np.uint8)

            output[fold_region] = folded[fold_region]

        shadow_distance = distance - fold_width

        shadow_region = (
            (shadow_distance >= 0)
            & (shadow_distance < shadow_width)
        )

        darken = (
            shadow_strength
            * bend
            * np.clip(
                1.0 - shadow_distance / shadow_width,
                0.0,
                1.0,
            ) ** 2
        )

        shading = 1.0 - darken

        shadowed = np.clip(
            output.astype(np.float32)
            * shading[..., None],
            0,
            255,
        ).astype(np.uint8)

        output[shadow_region] = shadowed[shadow_region]

        return output

    return render


def _pulse(p, start, peak, end):
    if p <= start or p >= end:
        return 0.0
    if p < peak:
        return _smooth((p - start) / max(.0001, peak - start))
    return 1.0 - _smooth((p - peak) / max(.0001, end - peak))



def _build_sliding_panels(clip, cfg):
    w, h = clip.size

    count = max(2, int(cfg["panel_count"]))
    divider = max(1, int(w * cfg["divider_ratio"]))
    accent_color = tuple(cfg["divider_color"])
    delay = float(cfg["reveal_offset_seconds"])

    buzz_duration = max(
        0.05,
        float(cfg.get("buzz_duration_seconds", 0.5))
    )

    buzz_pixels = float(
        cfg.get("buzz_pixels", 3.0)
    )

    buzz_frequency = float(
        cfg.get("buzz_frequency", 38.0)
    )

    blur_radius = float(
        cfg.get("motion_blur_radius", 2.0)
    )

    blur_mix = np.clip(
        cfg.get("motion_blur_mix", 0.55),
        0.0,
        1.0,
    )

    accent_times = [
        cfg["first_motion"][0] * clip.duration,
        cfg["first_motion"][1] * clip.duration,
        cfg["second_motion"][0] * clip.duration,
        cfg["second_motion"][1] * clip.duration,
    ]

    def render(get_frame, t):
        p = t / max(clip.duration, 0.001)

        magnitude = max(
            _pulse(p, *cfg["first_motion"]),
            _pulse(p, *cfg["second_motion"]),
        )

        current = _get(get_frame, t, clip)

        if magnitude < 0.002:
            canvas = current.copy()
        else:
            canvas = _get(get_frame, t - delay, clip)

        draw = ImageDraw.Draw(canvas)

        accent = 0.0

        if magnitude >= 0.002:
            for start in accent_times:
                delta = t - start

                if 0.0 <= delta < buzz_duration:
                    fade_in = min(
                        1.0,
                        delta / 0.07,
                    )

                    fade_out = min(
                        1.0,
                        (buzz_duration - delta) / 0.16,
                    )

                    accent = max(
                        accent,
                        _smooth(min(fade_in, fade_out)),
                    )

        accent *= min(1.0, magnitude * 4.0)

        for k in range(count):
            x0 = round(k * w / count)
            x1 = round((k + 1) * w / count)

            if magnitude >= 0.002:
                stagger = max(
                    0.25,
                    1.0 - k * cfg["stagger"],
                )

                distance = int(
                    h
                    * cfg["slide_amount"]
                    * magnitude
                    * stagger
                )

                dy = (
                    -distance
                    if k % 2 == 0
                    else distance
                )

                tile = current.crop(
                    (x0, 0, x1, h)
                )

                dx = 0

                if accent > 0.0:
                    effective_radius = (
                        blur_radius
                        * h / 720.0
                        * accent
                    )

                    blurred = tile.filter(
                        ImageFilter.GaussianBlur(
                            effective_radius
                        )
                    )

                    tile = Image.blend(
                        tile,
                        blurred,
                        float(blur_mix * accent),
                    )

                    dx = round(
                        buzz_pixels
                        * w / 1280.0
                        * accent
                        * math.sin(
                            2.0
                            * math.pi
                            * buzz_frequency
                            * t
                            + k * 1.8
                        )
                    )

                canvas.paste(
                    tile,
                    (x0 + dx, dy),
                )

            if k:
                draw.line(
                    [(x0, 0), (x0, h)],
                    fill=accent_color,
                    width=divider,
                )

        return np.asarray(canvas)

    return render


def _polaroid(image, size, cfg, caption):
    cw, ch = size
    border = max(5, int(cw * cfg['white_border_ratio']))
    bottom = max(border, int(ch * cfg['caption_space_ratio']))
    card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=max(4, border // 2), fill=tuple(cfg['paper_color']) + (255,))
    pw, ph = cw - 2 * border, ch - border - bottom
    if pw > 1 and ph > 1:
        photo = _fit(image, (pw, ph)).convert('RGBA')
        card.paste(photo, (border, border))
    f = _font(max(10, int(ch * .037)))
    draw.text((border, ch - bottom + max(2, bottom // 5)), caption, fill=tuple(cfg['caption_color']) + (255,), font=f)
    return card


def _build_photo_stack(clip, cfg):
    w, h = clip.size
    card_size = (int(w * cfg['card_width_ratio']), int(h * cfg['card_height_ratio']))
    anchors = cfg['sample_fractions']
    stills = [
        Image.fromarray(np.asarray(clip.get_frame(_sample_time(clip.duration * a, clip.duration, clip.fps or 24)), dtype=np.uint8)).convert('RGB')
        for a in anchors
    ]

    def render(get_frame, t):
        output = _gradient((w, h), cfg['background_top'], cfg['background_bottom']).convert('RGBA')
        frames = [stills[0], stills[2], _get(get_frame, t, clip)]
        positions = [-cfg['spread_ratio'], cfg['spread_ratio'], 0.0]
        angles = [cfg['left_angle'], cfg['right_angle'], cfg['front_angle']]
        labels = cfg['captions']
        for k in range(3):
            card = _polaroid(frames[k], card_size, cfg, labels[k])
            a = angles[k] + cfg['motion_degrees'] * math.sin(t * cfg['motion_speed'] + k * 1.6)
            rotated = card.rotate(a, resample=Image.Resampling.BICUBIC, expand=True)
            x = int((w - rotated.width) / 2 + positions[k] * w)
            y = int((h - rotated.height) / 2 + math.sin(t * cfg['float_speed'] + k * 2.0) * h * cfg['float_amount_ratio'])
            shadow = Image.new('RGBA', rotated.size, (0, 0, 0, 0))
            shadow.putalpha(rotated.getchannel('A').filter(ImageFilter.GaussianBlur(max(2, int(h * .012)))))
            shadow_rgb = Image.new('RGBA', rotated.size, (2, 7, 14, int(cfg['shadow_alpha'])))
            shadow_rgb.putalpha(shadow.getchannel('A').point(lambda value: int(value * cfg['shadow_alpha'] / 255)))
            output.alpha_composite(shadow_rgb, (x + max(2, int(w * .007)), y + max(2, int(h * .014))))
            output.alpha_composite(rotated, (x, y))
        return np.asarray(output.convert('RGB'))

    return render


def _build_storyboard(clip, cfg):
    w, h = clip.size
    cols, rows = 3, 2
    margin = max(6, int(w * cfg['margin_ratio']))
    gap = max(5, int(w * cfg['gap_ratio']))
    cell_w = (w - 2 * margin - (cols - 1) * gap) // cols
    cell_h = (h - 2 * margin - (rows - 1) * gap) // rows
    rects = []
    for j in range(rows):
        for i in range(cols):
            x = margin + i * (cell_w + gap)
            y = margin + j * (cell_h + gap)
            rects.append((x, y, x + cell_w, y + cell_h))
    stills = [
        Image.fromarray(np.asarray(clip.get_frame(_sample_time(clip.duration * fraction, clip.duration, clip.fps or 24)), dtype=np.uint8)).convert('RGB')
        for fraction in cfg['sample_fractions']
    ]
    focus_index = max(0, min(5, int(cfg['hero_index'])))
    begin = float(cfg["expand_start_seconds"])
    finish = float(cfg["expand_end_seconds"])
    border = max(2, int(w * cfg['border_ratio']))

    def render(get_frame, t):
        expand = _smooth(
            (t - begin) / max(0.0001, finish - begin)
        )
        if expand >= 0.999:
            return np.asarray(_get(get_frame, t, clip))

        output = Image.new('RGB', (w, h), tuple(cfg['background_color']))
        current = _get(get_frame, t, clip)
        d = ImageDraw.Draw(output)
        for i, (x0, y0, x1, y1) in enumerate(rects):
            picture = current if i == focus_index else stills[i]
            output.paste(_fit(picture, (cell_w, cell_h)), (x0, y0))
            d.rectangle((x0, y0, x1 - 1, y1 - 1), outline=tuple(cfg['grid_border_color']), width=border)
            _label(output, f'{i+1:02}', (x0 + 5, y0 + 5), cfg['label_background'], cfg['label_color'], max(10, h * cfg['label_size_ratio']), pad=max(3, h // 120))

        x0, y0, x1, y1 = rects[focus_index]
        nx0 = round(x0 * (1.0 - expand))
        ny0 = round(y0 * (1.0 - expand))
        nx1 = round(x1 + (w - x1) * expand)
        ny1 = round(y1 + (h - y1) * expand)
        output.paste(_fit(current, (nx1 - nx0, ny1 - ny0)), (nx0, ny0))
        if expand < .96:
            ImageDraw.Draw(output).rectangle(
                (nx0, ny0, nx1 - 1, ny1 - 1),
                outline=tuple(cfg['hero_border_color']),
                width=max(2, int(border * (1.0 - expand))),
            )
        return np.asarray(output)

    return render


CREATIVE_MOTION_EFFECTS = {
    'motion_filmstrip_journey': _build_filmstrip,
    'motion_time_windows': _build_time_windows,
    "motion_page_turn": _build_page_turn,
    'motion_sliding_panels': _build_sliding_panels,
    'motion_photo_stack': _build_photo_stack,
    'motion_kinetic_storyboard': _build_storyboard,
}


def _position_watermark(watermark, video, position):
    scale = min(1.0, video.w * .20 / max(1, watermark.w), video.h * .20 / max(1, watermark.h))
    if scale < 1.0:
        watermark = watermark.resized((max(1, round(watermark.w * scale)), max(1, round(watermark.h * scale))))
    margin = max(0, min(20, (video.w - watermark.w) // 2, (video.h - watermark.h) // 2))
    right = video.w - watermark.w - margin
    bottom = video.h - watermark.h - margin
    xy = {
        'top-left': (margin, margin),
        'top-right': (right, margin),
        'bottom-left': (margin, bottom),
        'bottom-right': (right, bottom),
    }
    return watermark.with_duration(video.duration).with_position(xy.get(position, xy['top-right']))


def process_creative_motion_effect(input_path, output_path, config, choices=None, watermark_path=None):
    choices = choices or {}
    effect_type = config.get('effect_type')
    builder = CREATIVE_MOTION_EFFECTS.get(effect_type)
    if builder is None:
        raise ValueError(f'Unknown Creative Motion effect: {effect_type}')


    with VideoFileClip(input_path) as original:
        render = builder(original, config)
        visual = original.transform(render)

        if effect_type == "motion_page_turn":
            _, _, map_time, output_duration = (
                _page_turn_timeline(original, config)
            )

            if float(config.get("time_skip_seconds", 0.0)) > 0:
                visual = visual.subclipped(
                    0,
                    output_duration,
                )

                if original.audio is not None:
                    synced_audio = (
                        original.audio.time_transform(
                            map_time,
                            keep_duration=True,
                        ).subclipped(
                            0,
                            output_duration,
                        )
                    )

                    visual = visual.with_audio(
                        synced_audio
                    )

        options = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": original.fps or 24,
        }
        try:
            if watermark_path and choices.get('watermark'):
                with ImageClip(watermark_path) as mark_source:
                    mark = _position_watermark(mark_source, visual, choices.get('watermarkPosition', 'top-right'))
                    with CompositeVideoClip([visual, mark], size=original.size) as output:
                        output.write_videofile(output_path, **options)
            else:
                visual.write_videofile(output_path, **options)
        finally:
            visual.close()
    return output_path
