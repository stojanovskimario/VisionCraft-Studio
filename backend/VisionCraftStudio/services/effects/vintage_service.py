
import numpy as np

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from moviepy import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from moviepy.video.fx import MultiplySpeed


def apply_vintage_color(frame, config):
    image = Image.fromarray(frame).convert("RGB")

    color_mode = config.get("color_mode", "grayscale")

    if color_mode == "grayscale":
        image = image.convert("L").convert("RGB")

    elif color_mode == "sepia":
        gray = np.asarray(image.convert("L"), dtype=np.float32)
        sepia = np.stack(
            [
                gray * 1.08,
                gray * 0.88,
                gray * 0.65,
            ],
            axis=-1,
        )
        image = Image.fromarray(
            np.uint8(np.clip(sepia, 0, 255))
        )

    elif color_mode == "warm":
        frame_array = np.asarray(image, dtype=np.float32)
        frame_array[:, :, 0] *= 1.12
        frame_array[:, :, 1] *= 1.04
        frame_array[:, :, 2] *= 0.88

        image = Image.fromarray(
            np.uint8(np.clip(frame_array, 0, 255))
        )

    elif color_mode == "faded":
        image = ImageEnhance.Color(image).enhance(0.65)

        frame_array = np.asarray(image, dtype=np.float32)
        frame_array = frame_array * 0.82 + 38

        image = Image.fromarray(
            np.uint8(np.clip(frame_array, 0, 255))
        )

    elif color_mode == "golden":
        frame_array = np.asarray(image, dtype=np.float32)
        frame_array[:, :, 0] *= 1.16
        frame_array[:, :, 1] *= 1.06
        frame_array[:, :, 2] *= 0.82

        image = Image.fromarray(
            np.uint8(np.clip(frame_array, 0, 255))
        )

    contrast = config.get("contrast", 1.0)
    brightness = config.get("brightness", 1.0)

    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = ImageEnhance.Brightness(image).enhance(brightness)

    return np.asarray(image)


def apply_film_grain(frame, intensity, t):
    if intensity <= 0:
        return frame

    seed = int(t * 1000) % (2**32)
    rng = np.random.default_rng(seed)

    noise = rng.normal(
        0,
        intensity * 1.5,
        frame.shape[:2],
    )

    result = frame.astype(np.float32)
    result += noise[:, :, np.newaxis]

    return np.uint8(np.clip(result, 0, 255))


def apply_vignette(frame, intensity):
    if intensity <= 0:
        return frame

    height, width = frame.shape[:2]

    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)

    xx, yy = np.meshgrid(x, y)

    distance = np.sqrt(xx**2 + yy**2)

    mask = 1 - (distance * intensity * 0.12)
    mask = np.clip(mask, 0.3, 1.0)

    result = frame.astype(np.float32)
    result *= mask[:, :, np.newaxis]

    return np.uint8(np.clip(result, 0, 255))


def apply_flicker(frame, intensity, t):
    if intensity <= 0:
        return frame

    flicker = 1 + (
        np.sin(t * 18) * intensity * 0.015
    )

    result = frame.astype(np.float32) * flicker

    return np.uint8(np.clip(result, 0, 255))


def apply_dust(frame, intensity, t):
    if intensity <= 0:
        return frame

    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)

    height, width = frame.shape[:2]

    rng = np.random.default_rng(
        int(t * 1000) % (2**32)
    )

    number_of_dust_particles = int(intensity * 3)

    for _ in range(number_of_dust_particles):
        x = int(rng.integers(0, width))
        y = int(rng.integers(0, height))

        radius = int(rng.integers(1, 3))

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius,
            ),
            fill=(235, 225, 200),
        )

    return np.asarray(image)


def apply_scratches(frame, intensity, t):
    if intensity <= 0:
        return frame

    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)

    height, width = frame.shape[:2]

    rng = np.random.default_rng(
        int(t * 1000 + 17) % (2**32)
    )

    number_of_scratches = max(1, int(intensity / 2))

    for _ in range(number_of_scratches):
        x = int(rng.integers(0, width))

        y_start = int(rng.integers(0, height))
        y_end = min(
            height,
            y_start + int(rng.integers(height // 8, height // 2 + 1)),
        )

        draw.line(
            (x, y_start, x, y_end),
            fill=(210, 205, 185),
            width=1,
        )

    return np.asarray(image)


def apply_soft_focus(frame, intensity):
    if intensity <= 0:
        return frame

    image = Image.fromarray(frame)

    image = image.filter(
        ImageFilter.GaussianBlur(radius=intensity)
    )

    return np.asarray(image)


def apply_light_leak(frame, intensity, t):
    if intensity <= 0:
        return frame

    height, width = frame.shape[:2]

    image = Image.fromarray(frame).convert("RGB")
    overlay = Image.new("RGB", (width, height), (0, 0, 0))
    pixels = np.zeros((height, width, 3), dtype=np.float32)

    center_x = int(
        width * (0.15 + 0.7 * ((t * 0.12) % 1))
    )

    center_y = int(height * 0.2)

    y, x = np.ogrid[:height, :width]

    distance = np.sqrt(
        ((x - center_x) / max(width * 0.65, 1)) ** 2
        + ((y - center_y) / max(height * 0.8, 1)) ** 2
    )

    strength = np.clip(1 - distance, 0, 1)

    strength *= intensity * 0.045

    pixels[:, :, 0] = 255 * strength
    pixels[:, :, 1] = 165 * strength
    pixels[:, :, 2] = 55 * strength

    overlay = Image.fromarray(
        np.uint8(np.clip(pixels, 0, 255))
    )

    return np.asarray(
        Image.blend(image, overlay, 0.65)
    )


def apply_rotation(frame, t, duration, rotation):
    if not rotation:
        return frame

    start = duration * rotation.get("start_percent", 20) / 100
    rotate_in = duration * rotation.get("rotate_in_percent", 5) / 100
    hold = duration * rotation.get("hold_percent", 15) / 100
    rotate_out = duration * rotation.get("rotate_out_percent", 5) / 100

    angle = rotation.get("angle", 90)

    if t < start or t > start + rotate_in + hold + rotate_out:
        current_angle = 0

    elif t < start + rotate_in:
        progress = (t - start) / rotate_in
        current_angle = angle * progress

    elif t < start + rotate_in + hold:
        current_angle = angle

    else:
        progress = (t - start - rotate_in - hold) / rotate_out
        current_angle = angle * (1 - progress)

    image = Image.fromarray(frame).convert("RGB")

    original_width, original_height = image.size

    rotated = image.rotate(
        current_angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
    )

    scale = min(
        original_width / rotated.width,
        original_height / rotated.height,
    )

    new_width = int(rotated.width * scale)
    new_height = int(rotated.height * scale)

    rotated = rotated.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new(
        "RGB",
        (original_width, original_height),
        (0, 0, 0),
    )

    x = (original_width - new_width) // 2
    y = (original_height - new_height) // 2

    canvas.paste(rotated, (x, y))

    return np.asarray(canvas)


def apply_vintage_effect(frame, t, duration, config):
    frame = apply_vintage_color(frame, config)

    frame = apply_rotation(
        frame,
        t,
        duration,
        config.get("rotation"),
    )

    frame = apply_film_grain(
        frame,
        config.get("film_grain", 0),
        t,
    )

    frame = apply_vignette(
        frame,
        config.get("vignette", 0),
    )

    frame = apply_flicker(
        frame,
        config.get("flicker", 0),
        t,
    )

    frame = apply_dust(
        frame,
        config.get("dust", 0),
        t,
    )

    frame = apply_scratches(
        frame,
        config.get("scratches", 0),
        t,
    )

    frame = apply_soft_focus(
        frame,
        config.get("soft_focus", 0),
    )

    frame = apply_light_leak(
        frame,
        config.get("light_leak", 0),
        t,
    )

    return frame


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


def process_vintage_effect(
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

    try:
        duration = original_clip.duration

        visual_clip = original_clip.transform(
            lambda get_frame, t: apply_vintage_effect(
                get_frame(t),
                t,
                duration,
                config,
            )
        )

        rotation_config = config.get("rotation", {})
        rotation_angle = rotation_config.get("angle", 0)

        rotation_config = config.get("rotation", {})

        rotation_end = duration * (
                (
                        rotation_config.get("start_percent", 20)
                        + rotation_config.get("rotate_in_percent", 5)
                        + rotation_config.get("hold_percent", 15)
                        + rotation_config.get("rotate_out_percent", 5)
                ) / 100
        )

        if rotation_angle != 0:
            rotation_start = duration * (
                rotation_config.get("start_percent", 20) / 100
            )

            rotation_start = max(0, min(rotation_start, duration))
            rotation_end = max(
                rotation_start,
                min(rotation_end, duration),
            )
        else:
            rotation_end = 0

        speed_config = config.get("speed", {})

        speed_factor = speed_config.get("factor", 1.0)

        speed_start = duration * (
            speed_config.get("start_percent", 55) / 100
        )

        speed_end = duration * (
            speed_config.get("end_percent", 75) / 100
        )

        speed_start = max(
            rotation_end,
            min(speed_start, duration),
        )

        speed_end = max(
            speed_start,
            min(speed_end, duration),
        )

        if speed_start > 0:
            parts.append(
                visual_clip.subclipped(0, speed_start)
            )

        if speed_factor != 1.0 and speed_end > speed_start:
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
                visual_clip.subclipped(speed_end, duration)
            )

        if not parts:
            parts.append(visual_clip)

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
        )

        return output_path

    finally:
        if watermark_clip:
            watermark_clip.close()

        if video_to_write and video_to_write is not final_video:
            video_to_write.close()

        if final_video:
            final_video.close()

        for part in parts:
            part.close()

        original_clip.close()
