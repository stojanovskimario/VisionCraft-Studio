import math
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


def apply_bioluminescent_lagoon(frame, t, config):

    height, width = frame.shape[:2]

    original = frame.astype(np.float32)

    # Create a deep navy and teal nighttime color grade.
    gray = (
        original[:, :, 0] * 0.299 +
        original[:, :, 1] * 0.587 +
        original[:, :, 2] * 0.114
    )

    result = original.copy()

    result[:, :, 0] *= config.get("red", 0.52)
    result[:, :, 1] *= config.get("green", 0.82)
    result[:, :, 2] *= config.get("blue", 1.18)

    contrast = config.get("contrast", 1.08)
    brightness = config.get("brightness", 0.72)

    result = (result - 128) * contrast + 128
    result *= brightness

    # Identify brighter details that will appear bioluminescent.
    threshold = config.get("glow_threshold", 75)
    glow_range = max(1, config.get("glow_range", 100))

    glow_mask = np.clip(
        (gray - threshold) / glow_range,
        0,
        1
    )

    mask_image = Image.fromarray(
        (glow_mask * 255).astype(np.uint8)
    )

    blurred_mask = mask_image.filter(
        ImageFilter.GaussianBlur(
            radius=config.get("glow_radius", 12)
        )
    )

    glow = (
        np.asarray(blurred_mask).astype(np.float32) / 255.0
    )

    # Add turquoise and emerald light.
    glow_color = np.array(
        config.get("glow_color", [15, 230, 175]),
        dtype=np.float32
    )

    result += (
        glow[:, :, np.newaxis] *
        glow_color *
        config.get("glow_intensity", 1.0)
    )

    # Add subtle violet accents to brighter areas.
    violet_mask = np.clip(
        (glow_mask - 0.45) * 1.8,
        0,
        1
    )

    violet_color = np.array(
        config.get("violet_color", [125, 45, 210]),
        dtype=np.float32
    )

    result += (
        violet_mask[:, :, np.newaxis] *
        violet_color *
        config.get("violet_intensity", 0.30)
    )

    result = np.clip(result, 0, 255).astype(np.uint8)

    # Create small floating bioluminescent particles.
    particle_count = config.get("particle_count", 35)
    particle_speed = config.get("particle_speed", 18)

    rng = np.random.default_rng(42)

    particle_x = rng.uniform(0, width, particle_count)
    particle_y = rng.uniform(0, height, particle_count)

    particle_sizes = rng.integers(
        2, 5, particle_count
    )

    particle_phases = rng.uniform(
        0, 2 * np.pi, particle_count
    )

    glow_layer = Image.new(
        "RGBA", (width, height), (0, 0, 0, 0)
    )

    sharp_layer = Image.new(
        "RGBA", (width, height), (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow_layer)
    sharp_draw = ImageDraw.Draw(sharp_layer)

    for index in range(particle_count):

        x = int(
            particle_x[index] +
            math.sin(t * 0.6 + particle_phases[index]) * 8
        ) % width

        y = int(
            particle_y[index] -
            t * particle_speed *
            (0.5 + particle_phases[index] / (2 * np.pi))
        ) % height

        radius = int(particle_sizes[index])

        glow_draw.ellipse(
            (
                x - radius * 2,
                y - radius * 2,
                x + radius * 2,
                y + radius * 2
            ),
            fill=(20, 255, 195, 100)
        )

        sharp_draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(125, 255, 225, 175)
        )

    # Add soft halos first, followed by sharper particles.
    base_image = Image.fromarray(result).convert("RGBA")

    glow_layer = glow_layer.filter(
        ImageFilter.GaussianBlur(
            radius=config.get("particle_glow_radius", 5)
        )
    )

    result_image = Image.alpha_composite(
        base_image,
        glow_layer
    )

    result_image = Image.alpha_composite(
        result_image,
        sharp_layer
    )

    return np.array(result_image.convert("RGB"))



def apply_underwater_effect(frame, t, duration, config):

    if config.get("effect_type") == "bioluminescent":
        return apply_bioluminescent_lagoon(
            frame,
            t,
            config
        )

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

