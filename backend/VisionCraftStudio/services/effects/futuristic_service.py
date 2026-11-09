
import numpy as np
from PIL import Image, ImageFilter


def apply_futuristic_color(frame, config):

    frame = frame.astype(np.float32)

    frame[:, :, 0] *= config.get("red", 1.0)
    frame[:, :, 1] *= config.get("green", 1.0)
    frame[:, :, 2] *= config.get("blue", 1.0)

    contrast = config.get("contrast", 1.0)
    brightness = config.get("brightness", 1.0)

    frame = (frame - 128) * contrast + 128
    frame *= brightness

    return np.clip(frame, 0, 255).astype(np.uint8)


def apply_futuristic_glow(frame, config):

    intensity = config.get("glow", 0)

    if intensity <= 0:
        return frame

    radius = config.get("glow_radius", 8)

    image = Image.fromarray(frame)

    blurred = image.filter(
        ImageFilter.GaussianBlur(radius=radius)
    )

    original = np.asarray(image).astype(np.float32)
    blurred = np.asarray(blurred).astype(np.float32)

    luminance = np.mean(original, axis=2, keepdims=True)

    mask = np.clip(
        (luminance - 90) / 120,
        0,
        1
    )

    result = original + blurred * intensity * mask

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_scan_lines(frame, config):

    intensity = config.get("scan_lines", 0)

    if intensity <= 0:
        return frame

    result = frame.astype(np.float32)

    line_strength = np.ones(frame.shape[0], dtype=np.float32)

    line_strength[::2] = 1.0 - intensity

    result *= line_strength[:, np.newaxis, np.newaxis]

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_rgb_shift(frame, config):

    shift = config.get("rgb_shift", 0)

    if shift <= 0:
        return frame

    height, width = frame.shape[:2]

    result = frame.copy()

    shift = min(int(shift), max(1, width // 20))

    result[:, :-shift, 0] = frame[:, shift:, 0]
    result[:, -shift:, 0] = frame[:, -1:, 0]

    result[:, shift:, 2] = frame[:, :-shift, 2]
    result[:, :shift, 2] = frame[:, :1, 2]

    return result



def apply_digital_glitch(frame, t, config):

    intensity = config.get("glitch_intensity", 0)

    if intensity <= 0:
        return frame

    glitch_duration = config.get("glitch_duration", 1.0)
    glitch_interval = config.get("glitch_interval", 5.0)
    glitch_offset = config.get("glitch_offset", 2.0)

    if glitch_interval <= 0:
        return frame

    elapsed = t - glitch_offset

    if elapsed < 0:
        return frame

    cycle_position = elapsed % glitch_interval

    if cycle_position >= glitch_duration:
        return frame

    height, width = frame.shape[:2]

    result = frame.copy()

    rng = np.random.default_rng(int(t * 12))

    band_count = max(1, int(intensity))
    max_shift = max(1, int(intensity * 2))

    for _ in range(band_count):

        band_height = int(
            rng.integers(
                2,
                max(3, min(15, height // 8))
            )
        )

        if height <= band_height:
            continue

        y = int(
            rng.integers(
                0,
                height - band_height
            )
        )

        shift = int(
            rng.integers(
                -max_shift,
                max_shift + 1
            )
        )

        result[y:y + band_height] = np.roll(
            result[y:y + band_height],
            shift,
            axis=1
        )

    return result


def apply_futuristic_effect(frame, t, config):

    frame = apply_futuristic_color(frame, config)

    frame = apply_futuristic_glow(frame, config)

    frame = apply_scan_lines(frame, config)

    frame = apply_rgb_shift(frame, config)

    frame = apply_digital_glitch(frame, t, config)

    return frame
