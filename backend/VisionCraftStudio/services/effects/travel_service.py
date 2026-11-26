import math

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip


def _uint8(image):
    return np.clip(image, 0.0, 255.0).astype(np.uint8)


def _smoothstep(value):
    value = np.clip(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


def _ramp(t, start, end):
    if end <= start:
        return float(t >= end)

    return float(_smoothstep((t - start) / (end - start)))


def _luma(image):
    return (
        0.299 * image[..., 0:1]
        + 0.587 * image[..., 1:2]
        + 0.114 * image[..., 2:3]
    )


def _grade(frame, config):
    image = frame.astype(np.float32)
    luminance = _luma(image)
    chroma = image - luminance

    colorfulness = (
        image.max(axis=2, keepdims=True)
        - image.min(axis=2, keepdims=True)
    ) / 255.0

    color_gain = (
        config.get("saturation", 1.0)
        + config.get("vibrance", 0.0) * (1.0 - colorfulness)
    )

    image = luminance + chroma * color_gain

    contrast = config.get("contrast", 1.0)
    image = (image - 128.0) * contrast + 128.0
    image *= config.get("brightness", 1.0)

    luma = _luma(image)

    shadow_weight = np.clip(
        (150.0 - luma) / 150.0, 0.0, 1.0
    )

    highlight_weight = np.clip(
        (luma - 100.0) / 155.0, 0.0, 1.0
    )

    image += shadow_weight * config.get("shadow_lift", 0.0)

    image -= (
        np.clip((luma - 195.0) / 60.0, 0.0, 1.0) ** 2
        * config.get("highlight_recovery", 0.0)
    )

    shadows = np.asarray(
        config.get("shadow_tint", [0, 0, 0]),
        dtype=np.float32,
    )

    highlights = np.asarray(
        config.get("highlight_tint", [0, 0, 0]),
        dtype=np.float32,
    )

    image += (
        shadow_weight * shadows
        + highlight_weight * highlights
    )

    return _uint8(image)


def _clarity(frame, strength, radius=1.6):
    if strength <= 0:
        return frame

    image = frame.astype(np.float32)

    gray = _uint8(_luma(image)[..., 0])

    blurred = np.asarray(
        Image.fromarray(gray).filter(
            ImageFilter.GaussianBlur(radius)
        ),
        dtype=np.float32,
    )

    detail = gray.astype(np.float32) - blurred

    detail = (
        np.sign(detail)
        * np.maximum(np.abs(detail) - 1.5, 0.0)
    )

    detail = np.clip(detail, -22.0, 22.0)

    return _uint8(
        image + strength * detail[..., None]
    )


def _center_zoom(frame, factor, pan_x=0.0, pan_y=0.0):
    if factor <= 1.0:
        return frame

    height, width = frame.shape[:2]

    large_w = max(width + 2, round(width * factor))
    large_h = max(height + 2, round(height * factor))

    scaled = Image.fromarray(frame).resize(
        (large_w, large_h),
        Image.Resampling.BICUBIC,
    )

    extra_x = large_w - width
    extra_y = large_h - height

    left = round(
        extra_x * np.clip(0.5 + pan_x, 0.0, 1.0)
    )

    top = round(
        extra_y * np.clip(0.5 + pan_y, 0.0, 1.0)
    )

    return np.asarray(
        scaled.crop(
            (left, top, left + width, top + height)
        )
    )


def _classic_travel(frame, t, duration, config):
    saturation = 1.0 + (
        config["saturation_peak"] - 1.0
    ) * _ramp(
        t,
        0.0,
        config["saturation_end_seconds"],
    )

    image = frame.astype(np.float32)
    gray = _luma(image)

    image = gray + (image - gray) * saturation

    warm_progress = _ramp(
        t,
        config["warm_start_seconds"],
        config["warm_end_seconds"],
    )

    image += (
        warm_progress
        * np.asarray(
            config["warm_tint"],
            dtype=np.float32,
        )
    )

    image = _uint8(image)

    zoom = 1.0 + config["zoom_amount"] * _ramp(
        t,
        config["zoom_start_seconds"],
        config["zoom_end_seconds"],
    )

    image = _center_zoom(image, zoom)

    fade_length = min(
        config["fade_seconds"],
        duration,
    )

    fade_start = max(0.0, duration - fade_length)

    fade = 1.0 - _ramp(
        t,
        fade_start,
        duration,
    )

    return _uint8(
        image.astype(np.float32) * fade
    )


def _tropical_escape(frame, t, duration, config):
    image = _grade(frame, config).astype(np.float32)

    red, green, blue = (
        image[..., i] for i in range(3)
    )

    water = _smoothstep(
        (
            np.minimum(green, blue)
            - red
            - 8.0
        ) / 50.0
    )

    leaves = _smoothstep(
        (
            green
            - np.maximum(red, blue)
            - 4.0
        ) / 52.0
    )

    image[..., 0] -= (
        config["aqua_red_reduction"] * water
    )

    image[..., 1] += (
        config["aqua_green_boost"] * water
        + config["leaf_boost"] * leaves
    )

    image[..., 2] += (
        config["aqua_blue_boost"] * water
    )

    return _clarity(
        _uint8(image),
        config["clarity"],
    )


def _mountain_air(frame, t, duration, config):
    image = _grade(frame, config)

    return _clarity(
        image,
        config["clarity"],
        radius=config["detail_radius"],
    )


def _miniature_world(frame, t, duration, config):
    image = _grade(frame, config)

    image = _clarity(
        image,
        config["clarity"],
        radius=config["detail_radius"],
    )

    height, width = image.shape[:2]

    blur_radius = max(
        0.5,
        config["blur_radius"] * min(width, height) / 720.0,
    )

    blurred = np.asarray(
        Image.fromarray(image).filter(
            ImageFilter.GaussianBlur(blur_radius)
        ),
        dtype=np.float32,
    )

    y, x = np.ogrid[
        0:1:complex(height),
        0:1:complex(width)
    ]

    center_x = config["focus_center_x"]
    center_y = config["focus_center_y"]

    radius_x = max(
        0.01,
        config["ellipse_width"] / 2.0
    )

    radius_y = max(
        0.01,
        config["ellipse_height"] / 2.0
    )

    distance = np.sqrt(
        ((x - center_x) / radius_x) ** 2
        + ((y - center_y) / radius_y) ** 2
    )

    feather = max(
        0.01,
        config["focus_feather"]
    )

    blur_weight = _smoothstep(
        (distance - 0.78) / feather
    )

    blur_weight *= config["blur_mix"]

    blur_weight = blur_weight[..., None]

    sharp = image.astype(np.float32)

    result = (
        sharp * (1.0 - blur_weight)
        + blurred * blur_weight
    )

    return _uint8(result)


def _blue_hour_journey(frame, t, duration, config):
    image = _grade(frame, config).astype(np.float32)

    start = (
        duration
        * config["transition_start_percent"]
        / 100.0
    )

    end = (
        duration
        * config["transition_end_percent"]
        / 100.0
    )

    progress = _ramp(t, start, end)

    if progress <= 0.0:
        return _uint8(image)

    luminance = _luma(image)

    shadow_weight = np.clip(
        (155.0 - luminance) / 155.0,
        0.0,
        1.0,
    )

    highlight_weight = np.clip(
        (luminance - 105.0) / 150.0,
        0.0,
        1.0,
    )

    image *= (
        1.0 - config["twilight_darken"] * progress
    )

    shadow_tint = np.asarray(
        config["shadow_tint"],
        dtype=np.float32,
    )

    highlight_tint = np.asarray(
        config["highlight_tint"],
        dtype=np.float32,
    )

    image += progress * (
        shadow_weight * shadow_tint
        + highlight_weight * highlight_tint
    )

    height = image.shape[0]

    y = np.linspace(
        0.0,
        1.0,
        height,
        dtype=np.float32,
    )[:, None, None]

    horizon = np.exp(
        -0.5 * (
            (y - config["horizon_y"])
            / max(0.01, config["horizon_width"])
        ) ** 2
    )

    blue_score = np.clip(
        (
            image[:, :, 2]
            - image[:, :, 0]
            + config["sky_color_bias"]
        ) / config["sky_color_range"],
        0.0,
        1.0,
    )

    bright_score = np.clip(
        (
            luminance[:, :, 0]
            - config["sky_min_brightness"]
        ) / config["sky_brightness_range"],
        0.0,
        1.0,
    )

    sky_weight = (
        blue_score * bright_score
    )[:, :, None]

    horizon_tint = np.asarray(
        config["horizon_tint"],
        dtype=np.float32,
    )

    image += (
        progress
        * config["horizon_strength"]
        * horizon
        * sky_weight
        * horizon_tint
    )

    return _uint8(image)


def _travel_postcard(frame, t, duration, config):
    image = _grade(frame, config)

    progress = _ramp(
        t,
        0.0,
        max(duration, 0.01),
    )

    pan = (
        config["pan_amount"]
        * (2.0 * progress - 1.0)
    )

    image = _center_zoom(
        image,
        1.0 + config["zoom_amount"],
        pan_x=pan,
    )

    height, width = image.shape[:2]

    border = max(
        2,
        round(
            min(width, height)
            * config["border_ratio"]
        ),
    )

    inner_w = width - 2 * border
    inner_h = height - 2 * border

    if inner_w < 1 or inner_h < 1:
        return image

    canvas = Image.new(
        "RGB",
        (width, height),
        tuple(config["border_color"]),
    )

    inset = Image.fromarray(image).resize(
        (inner_w, inner_h),
        Image.Resampling.LANCZOS,
    )

    canvas.paste(
        inset,
        (border, border),
    )

    return np.asarray(canvas)

def _to_uint8(frame):
    return np.clip(frame, 0, 255).astype(np.uint8)


def _apply_basic_grade(
    frame,
    red=1.0,
    green=1.0,
    blue=1.0,
    contrast=1.0,
    brightness=1.0,
    saturation=1.0,
):
    image = Image.fromarray(frame).convert("RGB")

    array = np.asarray(image, dtype=np.float32)
    array[:, :, 0] *= red
    array[:, :, 1] *= green
    array[:, :, 2] *= blue
    array = (array - 128.0) * contrast + 128.0
    array *= brightness

    image = Image.fromarray(_to_uint8(array))

    if saturation != 1.0:
        image = ImageEnhance.Color(image).enhance(saturation)

    return np.asarray(image)


def _zoom_crop_with_shift(frame, scale, shift_x=0, shift_y=0):
    if scale <= 1.0 and shift_x == 0 and shift_y == 0:
        return frame

    image = Image.fromarray(frame).convert("RGB")
    width, height = image.size

    scaled_width = max(width, int(round(width * scale)))
    scaled_height = max(height, int(round(height * scale)))

    scaled = image.resize(
        (scaled_width, scaled_height),
        Image.Resampling.LANCZOS,
    )

    max_left = max(0, scaled_width - width)
    max_top = max(0, scaled_height - height)

    left = max_left // 2 + shift_x
    top = max_top // 2 + shift_y

    left = max(0, min(left, max_left))
    top = max(0, min(top, max_top))

    cropped = scaled.crop((left, top, left + width, top + height))
    return np.asarray(cropped)


def _apply_moving_mist(frame, t, config):
    strength = float(config.get("haze_strength", 0.0))

    if strength <= 0.0:
        return frame

    image = Image.fromarray(frame).convert("RGBA")
    width, height = image.size

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    drift = math.sin(t * 0.35) * width * 0.05

    draw.ellipse(
        (
            -width * 0.22 + drift,
            height * 0.08,
            width * 0.40 + drift,
            height * 0.92,
        ),
        fill=int(105 * strength),
    )

    draw.ellipse(
        (
            width * 0.52 - drift * 0.4,
            height * 0.02,
            width * 1.12 - drift * 0.4,
            height * 0.82,
        ),
        fill=int(82 * strength),
    )

    blur_radius = max(12, int(min(width, height) * 0.05))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    mist_color = Image.new("RGBA", (width, height), (236, 244, 255, 0))
    mist_color.putalpha(mask)

    image = Image.alpha_composite(image, mist_color)
    return np.asarray(image.convert("RGB"))


def _apply_sun_sweep(frame, t, duration, config):
    strength = float(config.get("sun_strength", 0.0))

    if strength <= 0.0 or duration <= 0:
        return frame

    result = frame.astype(np.float32)

    height, width = frame.shape[:2]
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]

    progress = t / duration
    center = -0.30 + 1.55 * progress

    diagonal = x * 0.90 + y * 0.45
    beam = np.exp(-((diagonal - center) ** 2) / 0.015)
    beam *= strength

    result[:, :, 0] += beam * 65
    result[:, :, 1] += beam * 52
    result[:, :, 2] += beam * 24

    return _to_uint8(result)


def _build_postcard(frame, card_width, border_px, angle_degrees, shadow_opacity):
    source = Image.fromarray(frame).convert("RGB")
    source_ratio = source.height / source.width

    inner_width = max(1, card_width - border_px * 2)
    inner_height = max(
        1,
        int(round(inner_width * source_ratio))
    )

    photo = source.resize(
        (inner_width, inner_height),
        Image.Resampling.LANCZOS,
    )

    card_height = inner_height + border_px * 2
    card = Image.new(
        "RGBA",
        (card_width, card_height),
        (248, 246, 240, 255),
    )
    card.paste(photo, (border_px, border_px))

    shadow_pad = max(12, border_px * 2)
    shadow_base = Image.new(
        "RGBA",
        (
            card.width + shadow_pad * 2,
            card.height + shadow_pad * 2,
        ),
        (0, 0, 0, 0),
    )

    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    shadow_alpha = Image.new("L", card.size, shadow_opacity)
    shadow.putalpha(shadow_alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))

    shadow_base.paste(shadow, (shadow_pad, shadow_pad), shadow)
    shadow_base.paste(card, (shadow_pad, shadow_pad), card)

    rotated = shadow_base.rotate(
        angle_degrees,
        expand=True,
        resample=Image.Resampling.BICUBIC,
    )

    return rotated


def _paste_overlay_center(base_image, overlay_image, center_x, center_y, opacity):
    if opacity <= 0:
        return base_image

    overlay = overlay_image.copy()

    if opacity < 1.0:
        alpha = overlay.getchannel("A")
        alpha = alpha.point(lambda value: int(value * opacity))
        overlay.putalpha(alpha)

    layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))

    x = int(round(center_x - overlay.width / 2))
    y = int(round(center_y - overlay.height / 2))

    layer.paste(overlay, (x, y), overlay)
    return Image.alpha_composite(base_image, layer)

def _process_summit_reveal(
    input_path,
    output_path,
    config,
    choices,
    watermark_path,
):
    with VideoFileClip(input_path) as original:
        duration = original.duration
        fps = original.fps or 24

        start_zoom = float(config.get("start_zoom", 1.08))
        end_zoom = float(config.get("end_zoom", 1.00))
        drift_x_ratio = float(config.get("drift_x_ratio", 0.012))
        drift_y_ratio = float(config.get("drift_y_ratio", 0.008))

        def render_frame(get_frame, t):
            frame = get_frame(t)

            frame = _apply_basic_grade(
                frame,
                red=float(config.get("red", 0.98)),
                green=float(config.get("green", 1.03)),
                blue=float(config.get("blue", 1.08)),
                contrast=float(config.get("contrast", 1.04)),
                brightness=float(config.get("brightness", 1.03)),
                saturation=float(config.get("saturation", 1.08)),
            )

            progress = 0.0 if duration <= 0 else t / duration
            scale = start_zoom + (end_zoom - start_zoom) * progress

            drift_x = int(
                math.sin(t * 0.40) * original.w * drift_x_ratio
            )
            drift_y = int(
                math.cos(t * 0.27) * original.h * drift_y_ratio
            )

            frame = _zoom_crop_with_shift(
                frame,
                scale=scale,
                shift_x=drift_x,
                shift_y=drift_y,
            )

            frame = _apply_sun_sweep(frame, t, duration, config)
            frame = _apply_moving_mist(frame, t, config)

            return frame

        visual = original.transform(render_frame)

        export = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": fps,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as source:
                watermark = _position_watermark(
                    source,
                    visual,
                    choices.get("watermarkPosition", "top-right"),
                )

                with CompositeVideoClip(
                    [visual, watermark],
                    size=original.size,
                ) as output:
                    if original.audio is not None:
                        output = output.with_audio(original.audio)
                    output.write_videofile(output_path, **export)
        else:
            final = visual
            if original.audio is not None:
                final = final.with_audio(original.audio)
            final.write_videofile(output_path, **export)

    return output_path




def _process_postcard_memories(
    input_path,
    output_path,
    config,
    choices,
    watermark_path,
):
    from functools import lru_cache

    choices = choices or {}

    with VideoFileClip(input_path) as original:
        duration = original.duration
        fps = original.fps or 24
        width, height = original.size

        start = float(config.get("sequence_start_seconds", 2.0))
        cycle = float(config.get("cycle_seconds", 5.0))
        swoop = float(config.get("swoop_seconds", 0.20))
        hold = float(config.get("hold_seconds", 0.38))
        exit_time = float(config.get("exit_seconds", 0.24))

        offsets = config.get(
            "sample_offsets_seconds",
            [0.65, 1.55, 2.45],
        )

        card_scale = float(config.get("card_scale", 0.84))
        tilt_angles = config.get(
            "tilt_angles",
            [-5.0, 4.5, -3.5],
        )

        saturation = float(
            config.get("snapshot_saturation", 1.15)
        )
        contrast = float(
            config.get("snapshot_contrast", 1.09)
        )
        warmth = float(
            config.get("snapshot_warmth", 0.045)
        )

        swoop_blur = float(
            config.get("swoop_blur", 14.0)
        )

        video_saturation = float(
            config.get("video_saturation", 1.13)
        )

        video_contrast = float(
            config.get("video_contrast", 1.04)
        )

        video_brightness = float(
            config.get("video_brightness", 1.01)
        )

        count = 3
        stage = swoop + hold
        sequence_duration = count * stage + exit_time

        if (
            cycle <= 0
            or swoop <= 0
            or hold <= 0
            or exit_time <= 0
            or sequence_duration > cycle
        ):
            raise ValueError("Invalid Travel Postcard timing.")

        if len(offsets) < count or len(tilt_angles) < count:
            raise ValueError(
                "Travel Postcard requires three sample offsets "
                "and three tilt angles."
            )

        def ease_out(value):
            value = np.clip(value, 0.0, 1.0)
            return float(1.0 - (1.0 - value) ** 3)

        def ease_in(value):
            value = np.clip(value, 0.0, 1.0)
            return float(value ** 3)

        @lru_cache(maxsize=6)
        def get_postcard(cycle_index, index):
            desired_time = (
                start
                + cycle_index * cycle
                + float(offsets[index])
            )

            last_frame_time = max(
                0.001, duration - 1.0 / fps
            )

            if desired_time > last_frame_time:
                sample_time = desired_time % last_frame_time
            else:
                sample_time = desired_time

            frame = original.get_frame(sample_time)
            image = Image.fromarray(frame).convert("RGB")

            image = ImageEnhance.Color(image).enhance(
                saturation
            )
            image = ImageEnhance.Contrast(image).enhance(
                contrast
            )

            warm_layer = Image.new(
                "RGB",
                image.size,
                (255, 224, 194),
            )
            image = Image.blend(
                image,
                warm_layer,
                warmth,
            )

            photo_width = max(1, int(width * card_scale))
            photo_height = max(
                1,
                int(photo_width * height / width),
            )

            image = image.resize(
                (photo_width, photo_height),
                Image.Resampling.LANCZOS,
            )

            border = max(
                3,
                int(min(width, height) * 0.012),
            )
            bottom_border = border * 2

            card_width = photo_width + border * 2
            card_height = (
                photo_height + border + bottom_border
            )

            card = Image.new(
                "RGBA",
                (card_width, card_height),
                (250, 248, 242, 255),
            )
            card.paste(image, (border, border))

            blur_radius = max(
                3,
                int(min(width, height) * 0.011),
            )
            padding = blur_radius * 3

            canvas_size = (
                card_width + padding * 2,
                card_height + padding * 2,
            )

            shadow_mask = Image.new(
                "L", canvas_size, 0
            )

            shadow_draw = ImageDraw.Draw(shadow_mask)

            shadow_draw.rectangle(
                (
                    padding + 4,
                    padding + 6,
                    padding + 4 + card_width,
                    padding + 6 + card_height,
                ),
                fill=135,
            )

            shadow_mask = shadow_mask.filter(
                ImageFilter.GaussianBlur(
                    radius=blur_radius
                )
            )

            shadow = Image.new(
                "RGBA",
                canvas_size,
                (8, 10, 20, 0),
            )
            shadow.putalpha(shadow_mask)

            shadow.alpha_composite(
                card,
                (padding, padding),
            )

            rotated = shadow.rotate(
                float(tilt_angles[index]),
                resample=Image.Resampling.BICUBIC,
                expand=True,
            )

            return rotated

        def draw_card(background, card, shift_x=0):

            left = int(
                (width - card.width) / 2 + shift_x
            )
            top = int(
                (height - card.height) / 2
            )

            dst_x = max(0, left)
            dst_y = max(0, top)
            src_x = max(0, -left)
            src_y = max(0, -top)

            visible_width = min(
                width - dst_x,
                card.width - src_x,
            )
            visible_height = min(
                height - dst_y,
                card.height - src_y,
            )

            if visible_width <= 0 or visible_height <= 0:
                return background

            portion = card.crop(
                (
                    src_x,
                    src_y,
                    src_x + visible_width,
                    src_y + visible_height,
                )
            )

            background.alpha_composite(
                portion,
                (dst_x, dst_y),
            )
            return background

        def render_frame(get_frame, t):
            video_image = Image.fromarray(
                get_frame(t)
            ).convert("RGB")

            video_image = ImageEnhance.Color(
                video_image
            ).enhance(video_saturation)

            video_image = ImageEnhance.Contrast(
                video_image
            ).enhance(video_contrast)

            video_image = ImageEnhance.Brightness(
                video_image
            ).enhance(video_brightness)

            if t < start:
                return np.asarray(video_image)

            elapsed = t - start
            cycle_index = int(elapsed // cycle)
            local_t = elapsed % cycle

            if local_t >= sequence_duration:
                return np.asarray(video_image)

            background = video_image.convert("RGBA")

            snapshots_end = count * stage

            if local_t < snapshots_end:
                index = min(
                    count - 1,
                    int(local_t // stage),
                )

                stage_time = local_t - index * stage

                current = get_postcard(
                    cycle_index,
                    index,
                )

                if index > 0:
                    previous = get_postcard(
                        cycle_index,
                        index - 1,
                    )
                    draw_card(background, previous)

                if stage_time < swoop:
                    linear_progress = max(
                        0.0,
                        min(1.0, stage_time / swoop),
                    )

                    progress = ease_out(linear_progress)

                    direction = (
                        -1 if index % 2 == 0 else 1
                    )

                    travel_distance = (
                                              width + current.width
                                      ) / 2

                    shift_x = (
                            direction
                            * travel_distance
                            * (1.0 - progress)
                    )

                    blur_radius = (
                            swoop_blur
                            * min(width, height) / 720.0
                            * (1.0 - linear_progress) ** 1.2
                    )

                    if blur_radius > 0.05:
                        moving_card = current.filter(
                            ImageFilter.GaussianBlur(
                                radius=blur_radius
                            )
                        )
                    else:
                        moving_card = current

                else:
                    shift_x = 0
                    moving_card = current

                draw_card(
                    background,
                    moving_card,
                    shift_x,
                )


            else:
                progress = ease_in(
                    (local_t - snapshots_end)
                    / exit_time
                )

                last_card = get_postcard(
                    cycle_index,
                    count - 1,
                )

                travel_distance = (
                    width + last_card.width
                ) / 2

                draw_card(
                    background,
                    last_card,
                    travel_distance * progress,
                )

            return np.asarray(
                background.convert("RGB")
            )

        visual = original.transform(render_frame)

        export = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": fps,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as source:
                watermark = _position_watermark(
                    source,
                    visual,
                    choices.get(
                        "watermarkPosition",
                        "top-right",
                    ),
                )

                with CompositeVideoClip(
                    [visual, watermark],
                    size=original.size,
                ) as output:
                    output.write_videofile(
                        output_path,
                        **export,
                    )
        else:
            visual.write_videofile(
                output_path,
                **export,
            )

    return output_path



TRAVEL_EFFECTS = {
    "classic_travel": _classic_travel,
    "tropical_escape": _tropical_escape,
    "mountain_air": _mountain_air,
    "miniature_world": _miniature_world,
    "blue_hour_journey": _blue_hour_journey,
    "travel_postcard": _travel_postcard,
}


def _position_watermark(watermark, video, position):
    max_width = max(1, int(video.w * 0.20))
    max_height = max(1, int(video.h * 0.20))

    scale = min(
        max_width / watermark.w,
        max_height / watermark.h,
        1.0,
    )

    if scale < 1.0:
        watermark = watermark.resized(
            (
                max(1, int(watermark.w * scale)),
                max(1, int(watermark.h * scale)),
            )
        )

    margin = min(
        20,
        (video.w - watermark.w) // 2,
        (video.h - watermark.h) // 2,
    )

    placements = {
        "top-left": (margin, margin),
        "top-right": (
            video.w - watermark.w - margin,
            margin,
        ),
        "bottom-left": (
            margin,
            video.h - watermark.h - margin,
        ),
        "bottom-right": (
            video.w - watermark.w - margin,
            video.h - watermark.h - margin,
        ),
    }

    return watermark.with_duration(
        video.duration
    ).with_position(
        placements.get(
            position,
            placements["top-right"],
        )
    )


def process_travel_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):


    choices = choices or {}

    effect_type = config.get("effect_type")

    if effect_type == "summit_reveal":
        return _process_summit_reveal(
            input_path=input_path,
            output_path=output_path,
            config=config,
            choices=choices,
            watermark_path=watermark_path,
        )

    if effect_type == "postcard_memories":
        return _process_postcard_memories(
            input_path=input_path,
            output_path=output_path,
            config=config,
            choices=choices,
            watermark_path=watermark_path,
        )

    choices = choices or {}

    effect_type = config.get("effect_type")

    effect = TRAVEL_EFFECTS.get(effect_type)

    if effect is None:
        raise ValueError(
            f"Unknown Travel effect type: {effect_type}"
        )

    with VideoFileClip(input_path) as original:
        visual = original.transform(
            lambda get_frame, t: effect(
                get_frame(t),
                t,
                original.duration,
                config,
            )
        )

        export = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": original.fps or 24,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as watermark_source:
                watermark = _position_watermark(
                    watermark_source,
                    visual,
                    choices.get(
                        "watermarkPosition",
                        "top-right",
                    ),
                )

                with CompositeVideoClip(
                    [visual, watermark],
                    size=original.size,
                ) as output:
                    output.write_videofile(
                        output_path,
                        **export,
                    )
        else:
            visual.write_videofile(
                output_path,
                **export,
            )

    return output_path
