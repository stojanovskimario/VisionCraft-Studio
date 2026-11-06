
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def apply_underwater_color(frame, config):

    frame = frame.astype(np.float32)

    frame[:, :, 0] *= config.get("red", 0.88)
    frame[:, :, 1] *= config.get("green", 1.04)
    frame[:, :, 2] *= config.get("blue", 1.18)

    contrast = config.get("contrast", 0.94)
    frame = (frame - 128) * contrast + 128

    return np.clip(frame, 0, 255).astype(np.uint8)


def apply_water_distortion(frame, t, duration, config):

    intensity = config.get("distortion", 0)

    if intensity <= 0:
        return frame

    height, width = frame.shape[:2]

    y, x = np.indices((height, width), dtype=np.float32)

    progress = min(1.0, t / max(duration * 0.15, 0.1))

    wave_x = np.sin(
        y * 0.025 + t * 2.0
    ) * intensity * progress

    wave_y = np.sin(
        x * 0.018 + t * 1.5
    ) * intensity * 0.5 * progress

    map_x = np.clip(
        x + wave_x, 0, width - 1
    ).astype(np.int32)

    map_y = np.clip(
        y + wave_y, 0, height - 1
    ).astype(np.int32)

    return frame[map_y, map_x]


def apply_underwater_light_rays(frame, t, config):

    if not config.get("light_rays", False):
        return frame

    height, width = frame.shape[:2]

    intensity = config.get("light_ray_intensity", 0.12)

    x = np.arange(width, dtype=np.float32)
    y = np.arange(height, dtype=np.float32)

    horizontal = np.sin(
        x * 0.012 + t * 0.4
    )

    vertical = np.cos(
        y * 0.008 - t * 0.25
    )

    rays = np.outer(vertical, horizontal)

    brightness = np.maximum(rays, 0) * intensity

    result = frame.astype(np.float32)

    result[:, :, 0] += brightness * 15
    result[:, :, 1] += brightness * 35
    result[:, :, 2] += brightness * 45

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_underwater_bubbles(frame, t, config):

    if not config.get("bubbles", False):
        return frame

    height, width = frame.shape[:2]

    image = Image.fromarray(frame)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    rng = np.random.default_rng(42)

    bubble_count = config.get("bubble_count", 24)
    speed = config.get("bubble_speed", 25)
    opacity = config.get("bubble_opacity", 85)

    for _ in range(bubble_count):
        x = int(rng.uniform(0, width))
        start_y = rng.uniform(0, height)
        radius = int(rng.uniform(3, 9))

        y = (start_y - t * speed) % height

        x = int(x)
        y = int(y)

        color = (170, 225, 255, opacity)

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            outline=color,
            width=1
        )

        draw.ellipse(
            (
                x - radius // 2,
                y - radius // 2,
                x - radius // 4,
                y - radius // 4
            ),
            fill=(235, 250, 255, min(180, opacity + 50))
        )

    image = Image.alpha_composite(image.convert("RGBA"), overlay)

    return np.array(image.convert("RGB"))


def apply_underwater_soft_focus(frame, config):

    radius = config.get("soft_focus", 0)

    if radius <= 0:
        return frame

    original = Image.fromarray(frame)
    blurred = original.filter(
        ImageFilter.GaussianBlur(radius=radius)
    )

    result = Image.blend(original, blurred, 0.15)

    return np.array(result)


def apply_underwater_effect(frame, t, duration, config):

    frame = apply_underwater_color(frame, config)

    frame = apply_water_distortion(
        frame, t, duration, config
    )

    frame = apply_underwater_light_rays(
        frame, t, config
    )

    frame = apply_underwater_bubbles(
        frame, t, config
    )

    frame = apply_underwater_soft_focus(
        frame, config
    )

    return frame
