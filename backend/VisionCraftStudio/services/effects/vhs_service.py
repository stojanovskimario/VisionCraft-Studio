import numpy as np
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip
from PIL import Image


def _uint8(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def _color_grade(frame, config):
    image = frame.astype(np.float32)

    gray = image.mean(axis=2, keepdims=True)
    image = gray + (image - gray) * config["saturation"]
    image *= np.asarray(config["rgb_gain"], dtype=np.float32)
    image = (image - 128.0) * config["contrast"] + 128.0

    return _uint8(image)


def _burst_progress(t, offset, interval, duration):
    if t < offset or interval <= 0 or duration <= 0:
        return None

    elapsed = (t - offset) % interval
    if elapsed >= duration:
        return None

    return elapsed / duration


def _build_classic_vhs(video, config):
    fps = video.fps or 24
    scanline_stride = config["scanline_stride"]
    scanline_gain = config["scanline_gain"]
    glitch_start = config["glitch_start_seconds"]
    glitch_end = min(config["glitch_end_seconds"], video.duration)
    glitch_intensity = config["glitch_intensity"]
    noise_strength = config["noise_strength"]

    def transform(get_frame, t):
        frame = _color_grade(get_frame(t), config)

        frame[::scanline_stride] = _uint8(
            frame[::scanline_stride].astype(np.float32) * scanline_gain
        )

        rng = np.random.default_rng(max(0, round(t * fps)))

        if glitch_intensity > 0 and glitch_start <= t < glitch_end:
            height, width = frame.shape[:2]
            shift = max(1, int(width * 0.01 * glitch_intensity))

            frame[:, :, 0] = np.roll(frame[:, :, 0], shift, axis=1)
            frame[:, :, 2] = np.roll(frame[:, :, 2], -shift, axis=1)

            slice_height = max(2, height // 15)

            for y in range(0, height, slice_height):
                if rng.random() < config["slice_probability"]:
                    end_y = min(y + slice_height, height)
                    slice_shift = int(rng.integers(-shift, shift + 1))

                    frame[y:end_y] = np.roll(
                        frame[y:end_y], slice_shift, axis=1
                    )

        if noise_strength > 0:
            noise = rng.normal(
                0.0, noise_strength, frame.shape[:2] + (1,)
            )
            frame = _uint8(frame.astype(np.float32) + noise)

        return frame

    return transform


def _build_tracking_error(video, config):
    width, height = video.w, video.h
    band_height = min(height, max(1, round(height * config["band_ratio"])))
    max_shift = max(1, round(width * config["shift_ratio"]))
    columns = np.arange(width, dtype=np.int32)[None, :]

    def transform(get_frame, t):
        frame = _color_grade(get_frame(t), config)
        progress = _burst_progress(
            t,
            config["offset_seconds"],
            config["interval_seconds"],
            config["burst_seconds"],
        )

        if progress is None:
            return frame

        travel = height - band_height
        top = round(travel * (0.12 + 0.76 * progress))
        rows = np.arange(top, top + band_height)
        envelope = np.sin(np.pi * progress)

        row_offsets = np.rint(
            max_shift * envelope
            * np.sin(0.34 * rows + 32.0 * t)
        ).astype(np.int32)

        source_columns = np.clip(
            columns - row_offsets[:, None], 0, width - 1
        )

        result = frame.copy()
        result[rows] = frame[rows[:, None], source_columns]

        return result

    return transform


def _build_chroma_bleed(video, config):
    columns = np.arange(video.w)
    bleed_pixels = max(1, round(video.w * config["bleed_ratio"]))
    near = np.clip(columns - max(1, bleed_pixels // 3), 0, video.w - 1)
    far = np.clip(columns - bleed_pixels, 0, video.w - 1)
    strength = config["bleed_strength"]
    saturation = config["saturation"]

    def transform(get_frame, t):
        image = get_frame(t).astype(np.float32)

        luminance = (
            image[..., 0] * 0.299
            + image[..., 1] * 0.587
            + image[..., 2] * 0.114
        )[..., None]

        chroma = image - luminance
        trail = 0.65 * chroma[:, near] + 0.35 * chroma[:, far]
        smeared = chroma * (1.0 - strength) + trail * strength

        return _uint8(luminance + smeared * saturation)

    return transform


def _build_long_play(video, config):
    width, height = video.w, video.h
    scale = min(1.0, config["detail_short_side"] / min(width, height))

    low_width = max(1, round(width * scale * config["horizontal_detail"]))
    low_height = max(1, round(height * scale))
    low_size = (low_width, low_height)

    def transform(get_frame, t):
        frame = _color_grade(get_frame(t), config)
        image = Image.fromarray(frame)

        softened = image.resize(low_size, Image.Resampling.BOX).resize(
            (width, height),
            Image.Resampling.BILINEAR,
        )

        return np.asarray(softened)

    return transform


def _build_vertical_hold(video, config):
    height = video.h
    seam_half_height = max(1, round(height * config["seam_ratio"] / 2))

    def transform(get_frame, t):
        frame = _color_grade(get_frame(t), config)
        progress = _burst_progress(
            t,
            config["offset_seconds"],
            config["interval_seconds"],
            config["roll_seconds"],
        )

        if progress is None:
            return frame

        eased = progress * progress * (3.0 - 2.0 * progress)
        shift = int(eased * height)

        if shift == 0:
            return frame

        result = np.roll(frame, shift, axis=0)

        top = max(0, shift - seam_half_height)
        bottom = min(height, shift + seam_half_height)
        seam_gain = 1.0 - config["seam_strength"] * np.sin(np.pi * progress)
        result[top:bottom] = _uint8(
            result[top:bottom].astype(np.float32) * seam_gain
        )

        return result

    return transform


def _build_tape_leader(video, config):
    palette = np.array(
        [
            [194, 194, 194],
            [184, 178, 62],
            [67, 175, 176],
            [70, 173, 78],
            [175, 72, 171],
            [176, 65, 67],
            [66, 71, 175],
        ],
        dtype=np.float32,
    )

    band_indices = np.arange(video.w) * len(palette) // video.w
    bars = palette[band_indices][None, :, :]

    leader_end = min(
        config["leader_seconds"],
        video.duration * config["max_clip_share"],
    )
    fade_duration = min(config["fade_seconds"], leader_end)
    fade_start = leader_end - fade_duration

    def transform(get_frame, t):
        frame = _color_grade(get_frame(t), config)

        if t >= leader_end:
            return frame

        if t <= fade_start:
            bar_weight = 1.0
        else:
            bar_weight = (leader_end - t) / fade_duration

        return _uint8(frame * (1.0 - bar_weight) + bars * bar_weight)

    return transform


VHS_EFFECTS = {
    "classic_vhs": _build_classic_vhs,
    "vhs_tracking_error": _build_tracking_error,
    "vhs_chroma_bleed": _build_chroma_bleed,
    "vhs_long_play": _build_long_play,
    "vhs_vertical_hold": _build_vertical_hold,
    "vhs_tape_leader": _build_tape_leader,
}


def _position_watermark(watermark, video, position):
    max_width = max(1, int(video.w * 0.20))
    max_height = max(1, int(video.h * 0.20))
    scale = min(max_width / watermark.w, max_height / watermark.h, 1.0)

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
    right = video.w - watermark.w - margin
    bottom = video.h - watermark.h - margin

    positions = {
        "top-left": (margin, margin),
        "top-right": (right, margin),
        "bottom-left": (margin, bottom),
        "bottom-right": (right, bottom),
    }

    return watermark.with_duration(video.duration).with_position(
        positions.get(position, positions["top-right"])
    )


def process_vhs_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}
    effect_type = config.get("effect_type")
    build_effect = VHS_EFFECTS.get(effect_type)

    if build_effect is None:
        raise ValueError(f"Unknown VHS effect type: {effect_type}")

    with VideoFileClip(input_path) as original:
        visual = original.transform(build_effect(original, config))

        export_options = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": original.fps or 24,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as watermark_source:
                watermark = _position_watermark(
                    watermark_source,
                    visual,
                    choices.get("watermarkPosition", "top-right"),
                )

                with CompositeVideoClip(
                    [visual, watermark],
                    size=original.size,
                ) as output:
                    output.write_videofile(output_path, **export_options)
        else:
            visual.write_videofile(output_path, **export_options)

    return output_path