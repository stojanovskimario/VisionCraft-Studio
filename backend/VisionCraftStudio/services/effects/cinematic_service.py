
import math

import numpy as np
from PIL import Image, ImageFilter
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


def _to_float(frame):
    return frame.astype(np.float32)


def _to_uint8(frame):
    return np.clip(frame, 0, 255).astype(np.uint8)


def _color_grade(frame, config):
    image = _to_float(frame)

    image[:, :, 0] *= config.get("red", 1.0)
    image[:, :, 1] *= config.get("green", 1.0)
    image[:, :, 2] *= config.get("blue", 1.0)

    contrast = config.get("contrast", 1.0)
    brightness = config.get("brightness", 1.0)

    image = (image - 128) * contrast + 128
    image *= brightness

    return _to_uint8(image)


def _adjust_saturation(frame, saturation):
    image = _to_float(frame)

    gray = (
        image[:, :, 0] * 0.299
        + image[:, :, 1] * 0.587
        + image[:, :, 2] * 0.114
    )

    image = gray[..., None] + (
        image - gray[..., None]
    ) * saturation

    return _to_uint8(image)


def _apply_vignette(frame, strength):
    if strength <= 0:
        return frame

    height, width = frame.shape[:2]

    y, x = np.ogrid[-1:1:complex(height), -1:1:complex(width)]

    distance = x ** 2 + y ** 2
    mask = np.clip(1 - distance * strength, 0.2, 1.0)

    return _to_uint8(
        _to_float(frame) * mask[..., None]
    )


def _apply_bloom(frame, radius, intensity, threshold=170):
    if intensity <= 0 or radius <= 0:
        return frame

    image = _to_float(frame)

    luminance = (
        image[:, :, 0] * 0.299
        + image[:, :, 1] * 0.587
        + image[:, :, 2] * 0.114
    )

    highlight_mask = np.clip(
        (luminance - threshold) / max(1, 255 - threshold),
        0,
        1,
    )

    highlights = image * highlight_mask[..., None]

    blurred = np.asarray(
        Image.fromarray(_to_uint8(highlights)).filter(
            ImageFilter.GaussianBlur(radius)
        ),
        dtype=np.float32,
    )

    return _to_uint8(image + blurred * intensity)


def _apply_grain(frame, t, strength):
    if strength <= 0:
        return frame

    rng = np.random.default_rng(int(t * 24))
    noise = rng.normal(0, strength, frame.shape)

    return _to_uint8(_to_float(frame) + noise)


def _apply_split_toning(frame, shadows, highlights, strength):
    if strength <= 0:
        return frame

    image = _to_float(frame)

    luminance = (
        image[:, :, 0] * 0.299
        + image[:, :, 1] * 0.587
        + image[:, :, 2] * 0.114
    ) / 255.0

    shadow_weight = np.clip(
        (0.55 - luminance) / 0.55, 0, 1
    ) * strength

    highlight_weight = np.clip(
        (luminance - 0.45) / 0.55, 0, 1
    ) * strength

    shadow_color = np.asarray(shadows, dtype=np.float32)
    highlight_color = np.asarray(highlights, dtype=np.float32)

    image += shadow_weight[..., None] * shadow_color
    image += highlight_weight[..., None] * highlight_color

    return _to_uint8(image)


def apply_hollywood_blockbuster(frame, t, config):
    image = _color_grade(frame, config)

    image = _apply_split_toning(
        image,
        shadows=(-12, 5, 13),
        highlights=(14, 6, -8),
        strength=config.get("split_strength", 0.9),
    )

    image = _adjust_saturation(
        image, config.get("saturation", 1.08)
    )

    image = _apply_vignette(
        image, config.get("vignette", 0.16)
    )

    return image


def apply_dark_moody(frame, t, config):
    image = _color_grade(frame, config)

    image = _adjust_saturation(
        image, config.get("saturation", 0.70)
    )

    image = _apply_split_toning(
        image,
        shadows=(-8, 0, 12),
        highlights=(3, 1, -2),
        strength=config.get("split_strength", 0.85),
    )

    image = _apply_vignette(
        image, config.get("vignette", 0.26)
    )

    return _apply_grain(
        image, t, config.get("grain", 3.0)
    )


def apply_golden_hour(frame, t, config):
    image = _color_grade(frame, config)

    image = _apply_split_toning(
        image,
        shadows=(4, 0, -5),
        highlights=(18, 10, -12),
        strength=config.get("split_strength", 0.9),
    )

    image = _adjust_saturation(
        image, config.get("saturation", 1.12)
    )

    image = _apply_bloom(
        image,
        radius=config.get("bloom_radius", 10),
        intensity=config.get("bloom_intensity", 0.35),
        threshold=config.get("bloom_threshold", 155),
    )

    return image


def apply_anamorphic(frame, t, config):
    image = _color_grade(frame, config)

    image = _apply_split_toning(
        image,
        shadows=(-5, 2, 10),
        highlights=(5, 4, 7),
        strength=config.get("split_strength", 0.65),
    )

    image = _apply_bloom(
        image,
        radius=config.get("bloom_radius", 9),
        intensity=config.get("bloom_intensity", 0.30),
    )

    height, width = image.shape[:2]

    flare_strength = config.get("flare_strength", 0.28)
    flare_threshold = config.get("flare_threshold", 225)

    if flare_strength > 0:
        luminance = (
            image[:, :, 0] * 0.299
            + image[:, :, 1] * 0.587
            + image[:, :, 2] * 0.114
        )

        bright_mask = luminance > flare_threshold

        if np.any(bright_mask):
            weights = np.maximum(
                luminance - flare_threshold, 0
            )

            row_energy = weights.sum(axis=1)

            peak_row = int(np.argmax(row_energy))

            if row_energy[peak_row] > 0:
                y = np.arange(height, dtype=np.float32)

                vertical_falloff = np.exp(
                    -0.5 * (
                        (y - peak_row) /
                        max(1, height * 0.006)
                    ) ** 2
                )

                row_strength = min(
                    1.0,
                    row_energy[peak_row] /
                    max(1, width * 20),
                )

                x = np.arange(width, dtype=np.float32)
                center_x = width / 2

                horizontal_falloff = np.exp(
                    -0.5 * (
                        (x - center_x) /
                        max(1, width * 0.45)
                    ) ** 2
                )

                flare = (
                    vertical_falloff[:, None]
                    * horizontal_falloff[None, :]
                    * flare_strength
                    * row_strength
                )

                image_float = _to_float(image)
                image_float += (
                    flare[..., None]
                    * np.array([40, 100, 210], dtype=np.float32)
                )

                image = _to_uint8(image_float)

    if config.get("letterbox", True):
        bar_ratio = config.get("bar_ratio", 0.12)
        bar_height = int(height * bar_ratio)
        bar_height = max(0, min(bar_height, height // 2))

        image[:bar_height, :, :] = 0
        image[height - bar_height:, :, :] = 0

    return image


def apply_indie_film(frame, t, config):
    image = _color_grade(frame, config)

    image = _to_float(image)

    lift = config.get("black_lift", 12)
    image = image * (1 - lift / 255.0) + lift

    image = _to_uint8(image)

    image = _adjust_saturation(
        image, config.get("saturation", 0.82)
    )

    image = _apply_split_toning(
        image,
        shadows=(3, 2, 5),
        highlights=(9, 5, -3),
        strength=config.get("split_strength", 0.55),
    )

    image = _apply_grain(
        image, t, config.get("grain", 2.5)
    )

    return image


def apply_technicolor_pop(frame, t, config):
    image = _to_float(frame)

    luminance = (
        image[:, :, 0] * 0.299
        + image[:, :, 1] * 0.587
        + image[:, :, 2] * 0.114
    )[..., None]

    hsv = np.asarray(Image.fromarray(frame).convert("HSV"))
    hue = hsv[:, :, 0].astype(np.float32) * (360.0 / 256.0)
    saturation = hsv[:, :, 1].astype(np.float32) / 255.0

    red = config.get("red_boost", 0.36)

    boost = np.interp(
        hue,
        [0, 30, 60, 120, 180, 240, 300, 360],
        [
            red,
            config.get("orange_boost", 0.06),
            0.16,
            config.get("green_boost", 0.30),
            0.20,
            config.get("blue_boost", 0.32),
            0.24,
            red,
        ],
    ).astype(np.float32)

    color_weight = np.clip((saturation - 0.05) / 0.20, 0, 1)
    chroma = image - luminance
    graded = luminance + chroma * (1 + (boost * color_weight)[..., None])

    contrast = config.get("contrast", 1.06)
    graded = (graded - 128) * contrast + 128

    highlight_protection = np.clip((luminance - 185) / 70, 0, 1)
    result = graded * (1 - highlight_protection) + image * highlight_protection

    return _to_uint8(np.rint(result))


CINEMATIC_EFFECTS = {
    "hollywood_blockbuster": apply_hollywood_blockbuster,
    "dark_moody": apply_dark_moody,
    "golden_hour": apply_golden_hour,
    "anamorphic": apply_anamorphic,
    "indie_film": apply_indie_film,
    "technicolor_pop": apply_technicolor_pop,
}


def apply_cinematic_effect(frame, t, config):
    effect_type = config.get("effect_type")
    processor = CINEMATIC_EFFECTS.get(effect_type)

    if processor is None:
        raise ValueError(
            f"Unknown Cinematic effect type: {effect_type}"
        )

    return processor(frame, t, config)


def add_watermark(video, watermark_path, choices):
    watermark = ImageClip(watermark_path)

    max_width = int(video.w * 0.2)
    max_height = int(video.h * 0.2)

    scale = min(
        max_width / watermark.w,
        max_height / watermark.h,
        1,
    )

    if scale < 1:
        watermark = watermark.resized(
            width=max(1, int(watermark.w * scale))
        )

    margin = 20
    position = choices.get(
        "watermarkPosition", "top-right"
    )

    positions = {
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

    watermark = watermark.with_duration(video.duration)
    watermark = watermark.with_position(
        positions.get(position, positions["top-right"])
    )

    return CompositeVideoClip([video, watermark]), watermark


def process_cinematic_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}

    original_clip = VideoFileClip(input_path)

    visual_clip = None
    video_to_write = None
    watermark_clip = None

    try:
        fps = original_clip.fps or 24

        visual_clip = original_clip.transform(
            lambda get_frame, t: apply_cinematic_effect(
                get_frame(t),
                t,
                config,
            )
        )

        video_to_write = visual_clip

        if watermark_path and choices.get("watermark"):
            video_to_write, watermark_clip = add_watermark(
                visual_clip,
                watermark_path,
                choices,
            )

        video_to_write.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=fps,
        )

        return output_path

    finally:
        if watermark_clip is not None:
            watermark_clip.close()

        if video_to_write is not None and video_to_write is not visual_clip:
            video_to_write.close()

        if visual_clip is not None:
            visual_clip.close()

        original_clip.close()
