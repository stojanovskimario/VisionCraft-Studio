
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from moviepy import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from moviepy.video.fx import MultiplySpeed


def _to_float(frame):
    return frame.astype(np.float32)


def _to_uint8(frame):
    return np.clip(frame, 0, 255).astype(np.uint8)


def _apply_color_grade(frame, config):
    image = _to_float(frame)

    image[:, :, 0] *= config.get("red", 1.0)
    image[:, :, 1] *= config.get("green", 1.0)
    image[:, :, 2] *= config.get("blue", 1.0)

    contrast = config.get("contrast", 1.0)
    image = (image - 128) * contrast + 128

    brightness = config.get("brightness", 1.0)
    image *= brightness

    return _to_uint8(image)


def apply_analog_memories(frame, t, config):
    image = _to_float(frame)

    image[:, :, 0] *= config.get("red", 1.12)
    image[:, :, 1] *= config.get("green", 0.98)
    image[:, :, 2] *= config.get("blue", 0.82)

    contrast = config.get("contrast", 0.9)
    image = (image - 128) * contrast + 128

    image = _to_uint8(image)

    grain_intensity = config.get("grain_intensity", 5)
    noise_strength = grain_intensity * 2.5

    rng = np.random.default_rng(int(t * 24))

    noise = rng.normal(
        0,
        noise_strength,
        image.shape
    )

    image = _to_uint8(
        image.astype(np.float32) + noise
    )

    height, width = image.shape[:2]

    y, x = np.ogrid[:height, :width]

    center_x = width / 2
    center_y = height / 2

    distance = np.sqrt(
        ((x - center_x) / center_x) ** 2
        + ((y - center_y) / center_y) ** 2
    )

    vignette_intensity = config.get(
        "vignette_intensity",
        1.0
    )

    mask = 1 - (
        distance * 0.35 * vignette_intensity
    )

    mask = np.clip(mask, 0.2, 1)

    image = image.astype(np.float32) * mask[..., None]

    return _to_uint8(image)


def apply_crt_television(frame, t, config):
    image = _apply_color_grade(frame, config)

    height, width = image.shape[:2]

    y, x = np.indices((height, width), dtype=np.float32)

    center_x = width / 2
    center_y = height / 2

    normalized_x = (x - center_x) / center_x
    normalized_y = (y - center_y) / center_y

    radius_squared = (
        normalized_x ** 2 + normalized_y ** 2
    )

    curvature = config.get("curvature", 0.06)

    source_x = x + (
        normalized_x * radius_squared * center_x * curvature
    )

    source_y = y + (
        normalized_y * radius_squared * center_y * curvature
    )

    source_x = np.clip(
        source_x.astype(np.int32),
        0,
        width - 1
    )

    source_y = np.clip(
        source_y.astype(np.int32),
        0,
        height - 1
    )

    image = image[source_y, source_x]

    scanline_strength = config.get(
        "scanline_strength",
        0.18
    )

    rows = np.arange(height)

    scanlines = 1 - (
        (rows % 2) * scanline_strength
    )

    image = image.astype(np.float32) * scanlines[:, None, None]

    rgb_shift = config.get("rgb_shift", 1)

    if rgb_shift > 0:
        red = np.roll(
            image[:, :, 0],
            rgb_shift,
            axis=1
        )

        blue = np.roll(
            image[:, :, 2],
            -rgb_shift,
            axis=1
        )

        image[:, :, 0] = red
        image[:, :, 2] = blue

    image = _to_uint8(image)

    glow_radius = config.get("glow_radius", 2)
    glow_intensity = config.get("glow_intensity", 0.18)

    if glow_radius > 0 and glow_intensity > 0:
        blurred = np.array(
            Image.fromarray(image).filter(
                ImageFilter.GaussianBlur(glow_radius)
            )
        ).astype(np.float32)

        image = _to_uint8(
            image.astype(np.float32) * (1 - glow_intensity)
            + blurred * glow_intensity
        )

    flicker = config.get("flicker", 0.025)

    brightness = 1 - (
        flicker * (0.5 + 0.5 * math.sin(t * 12))
    )

    return _to_uint8(
        image.astype(np.float32) * brightness
    )


def apply_camcorder_90s(frame, t, config):
    image = _apply_color_grade(frame, config)

    image = _to_float(image)

    image[:, :, 0] *= config.get("warmth", 1.05)
    image[:, :, 1] *= config.get("green_tint", 1.04)
    image[:, :, 2] *= config.get("blue_tint", 0.88)

    image = _to_uint8(image)

    shift = config.get("color_bleed", 2)

    if shift > 0:
        image[:, :, 0] = np.roll(
            image[:, :, 0],
            shift,
            axis=1
        )

    noise_strength = config.get("noise_intensity", 4)

    rng = np.random.default_rng(int(t * 24))

    noise = rng.normal(
        0,
        noise_strength,
        image.shape
    )

    image = _to_uint8(
        image.astype(np.float32) + noise
    )

    if config.get("show_timestamp", True):
        height, width = image.shape[:2]

        overlay = Image.fromarray(image)
        draw = ImageDraw.Draw(overlay)

        seconds = max(0, int(t))

        timestamp = (
            f"{seconds // 3600:02}:"
            f"{(seconds // 60) % 60:02}:"
            f"{seconds % 60:02}"
        )

        margin = max(12, width // 50)

        draw.text(
            (margin, height - margin - 16),
            f"PLAY  {timestamp}",
            fill=(235, 235, 210)
        )

        image = np.array(overlay)

    return image


def apply_y2k_digital(frame, t, config):
    image = _apply_color_grade(frame, config)

    image = _to_float(image)

    contrast = config.get("contrast_boost", 1.12)

    image = (image - 128) * contrast + 128

    image[:, :, 2] *= config.get("blue_highlights", 1.10)

    image = _to_uint8(image)

    noise_strength = config.get("noise_intensity", 3)

    rng = np.random.default_rng(int(t * 24))

    noise = rng.normal(
        0,
        noise_strength,
        image.shape
    )

    image = _to_uint8(
        image.astype(np.float32) + noise
    )

    glow_radius = config.get("glow_radius", 3)
    glow_intensity = config.get("glow_intensity", 0.20)

    if glow_intensity > 0:
        blurred = np.array(
            Image.fromarray(image).filter(
                ImageFilter.GaussianBlur(glow_radius)
            )
        ).astype(np.float32)

        image = _to_uint8(
            image.astype(np.float32)
            + blurred * glow_intensity
        )

    return image

def apply_synthwave(frame, t, config):
    image = _to_float(frame)

    image[:, :, 0] *= config.get("red", 1.15)
    image[:, :, 1] *= config.get("green", 0.78)
    image[:, :, 2] *= config.get("blue", 1.30)

    contrast = config.get("contrast", 1.12)

    image = (image - 128) * contrast + 128

    image = _to_uint8(image)

    glow_radius = config.get("glow_radius", 8)
    glow_intensity = config.get("glow_intensity", 0.30)

    if glow_intensity > 0:
        blurred = np.array(
            Image.fromarray(image).filter(
                ImageFilter.GaussianBlur(glow_radius)
            )
        ).astype(np.float32)

        image = _to_uint8(
            image.astype(np.float32) * (1 - glow_intensity)
            + blurred * glow_intensity
        )

    pulse_strength = config.get("pulse_intensity", 0.06)
    pulse = 1 + (
        pulse_strength * math.sin(t * 2)
    )

    image = _to_uint8(
        image.astype(np.float32) * pulse
    )

    return image

def apply_comic_book(frame, t, config):
    image = _apply_color_grade(frame, config)

    pil_image = Image.fromarray(image).convert("RGB")

    smoothing = config.get("smoothing", 0.6)

    if smoothing > 0:
        pil_image = pil_image.filter(
            ImageFilter.GaussianBlur(smoothing)
        )

    saturation = config.get("saturation", 1.25)

    pil_image = ImageEnhance.Color(
        pil_image
    ).enhance(saturation)

    palette_colors = config.get("palette_colors", 12)

    pil_image = pil_image.quantize(
        colors=palette_colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    ).convert("RGB")

    image = np.array(pil_image).astype(np.float32)

    height, width = image.shape[:2]

    grayscale = Image.fromarray(
        _to_uint8(image)
    ).convert("L")

    edges = np.array(
        grayscale.filter(ImageFilter.FIND_EDGES)
    ).astype(np.float32)

    edge_threshold = config.get("edge_threshold", 45)
    outline_strength = config.get("outline_strength", 0.85)

    edge_mask = np.clip(
        (edges - edge_threshold) / 80,
        0,
        1,
    )

    image *= (
        1 - edge_mask[..., None] * outline_strength
    )

    image = _to_uint8(image)

    y, x = np.indices((height, width))

    dot_size = max(
        3,
        config.get("dot_size", 6)
    )

    pattern = (
        np.sin(x * (math.pi / dot_size))
        * np.sin(y * (math.pi / dot_size))
    )

    luminance = (
        0.299 * image[:, :, 0]
        + 0.587 * image[:, :, 1]
        + 0.114 * image[:, :, 2]
    )

    darkness = 1 - luminance / 255

    dots = pattern > (
        1 - darkness * 2
    )

    dot_intensity = config.get("dot_intensity", 0.25)

    image = image.astype(np.float32) * (
        1 - dots[..., None] * dot_intensity
    )

    return _to_uint8(image)

RETRO_EFFECTS = {
    "analog_memories": apply_analog_memories,
    "crt_television": apply_crt_television,
    "camcorder_90s": apply_camcorder_90s,
    "y2k_digital": apply_y2k_digital,
    "synthwave": apply_synthwave,
    "comic_book": apply_comic_book,
}


def apply_retro_effect(frame, t, config):
    effect_type = config.get("effect_type")

    processor = RETRO_EFFECTS.get(effect_type)

    if processor is None:
        raise ValueError(
            f"Unknown Retro effect type: {effect_type}"
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
            width=int(watermark.w * scale)
        )

    margin = 20

    position = choices.get(
        "watermarkPosition",
        "top-right",
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


def process_retro_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}

    original_clip = VideoFileClip(input_path)

    parts = []
    watermark_clip = None
    final_video = None
    video_to_write = None
    visual_clip = None

    try:
        duration = original_clip.duration
        fps = original_clip.fps or 24

        visual_clip = original_clip.transform(
            lambda get_frame, t: apply_retro_effect(
                get_frame(t),
                t,
                config,
            )
        )

        speed_config = config.get("speed", {})
        speed_factor = speed_config.get("factor", 1.0)

        speed_start = duration * (
            speed_config.get("start_percent", 55) / 100
        )

        speed_end = duration * (
            speed_config.get("end_percent", 75) / 100
        )

        speed_start = max(
            0,
            min(speed_start, duration),
        )

        speed_end = max(
            speed_start,
            min(speed_end, duration),
        )

        if speed_factor == 1.0 or speed_end <= speed_start:
            parts.append(visual_clip)

        else:
            if speed_start > 0:
                parts.append(
                    visual_clip.subclipped(0, speed_start)
                )

            speed_part = visual_clip.subclipped(
                speed_start,
                speed_end,
            )

            speed_part = speed_part.with_effects(
                [MultiplySpeed(speed_factor)]
            )

            parts.append(speed_part)

            if speed_end < duration:
                parts.append(
                    visual_clip.subclipped(
                        speed_end,
                        duration,
                    )
                )

        if len(parts) == 1:
            final_video = parts[0]
        else:
            final_video = concatenate_videoclips(
                parts,
                method="compose",
            )

        video_to_write = final_video

        if watermark_path and choices.get("watermark"):
            video_to_write, watermark_clip = add_watermark(
                final_video,
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

        if video_to_write is not None and video_to_write is not final_video:
            video_to_write.close()

        if final_video is not None and final_video is not visual_clip:
            final_video.close()

        for part in parts:
            if part is not visual_clip:
                part.close()

        if visual_clip is not None:
            visual_clip.close()

        original_clip.close()

