
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


def apply_thermal_vision(frame, config):

    frame = frame.astype(np.float32)

    gray = (
        frame[:, :, 0] * 0.299 +
        frame[:, :, 1] * 0.587 +
        frame[:, :, 2] * 0.114
    )

    contrast = config.get("thermal_contrast", 1.15)
    brightness = config.get("thermal_brightness", 1.0)

    gray = (gray - 128) * contrast + 128
    gray *= brightness

    gray = np.clip(gray, 0, 255)

    color_points = np.array([
        [0, 0, 0],
        [30, 0, 70],
        [70, 0, 160],
        [150, 0, 100],
        [220, 0, 20],
        [255, 70, 0],
        [255, 180, 0],
        [255, 255, 120],
        [255, 255, 255]
    ], dtype=np.float32)

    positions = np.linspace(0, 255, len(color_points))

    result = np.zeros((*gray.shape, 3), dtype=np.float32)

    for channel in range(3):
        result[:, :, channel] = np.interp(
            gray,
            positions,
            color_points[:, channel]
        )

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_cybernetic_vision(frame, t, config):

    frame_float = frame.astype(np.float32)

    frame_float[:, :, 0] *= config.get("red", 0.72)
    frame_float[:, :, 1] *= config.get("green", 0.95)
    frame_float[:, :, 2] *= config.get("blue", 1.25)

    contrast = config.get("contrast", 1.18)
    brightness = config.get("brightness", 0.88)

    frame_float = (frame_float - 128) * contrast + 128
    frame_float *= brightness

    base = np.clip(frame_float, 0, 255).astype(np.uint8)

    gray = (
        frame[:, :, 0] * 0.299 +
        frame[:, :, 1] * 0.587 +
        frame[:, :, 2] * 0.114
    ).astype(np.uint8)

    gray_image = Image.fromarray(gray)

    edges = gray_image.filter(
        ImageFilter.FIND_EDGES
    )

    threshold = config.get("edge_threshold", 18)
    strength = config.get("edge_strength", 4.0)

    edge_array = np.asarray(edges).astype(np.float32)

    edge_array = np.clip(
        (edge_array - threshold) * strength,
        0,
        255
    )

    edge_image = Image.fromarray(
        edge_array.astype(np.uint8)
    )

    edge_image = edge_image.filter(
        ImageFilter.MaxFilter(5)
    )

    sharp_edges = (
        np.asarray(edge_image).astype(np.float32) / 255.0
    )

    glow_radius = config.get("edge_glow_radius", 5)

    blurred_edges = edge_image.filter(
        ImageFilter.GaussianBlur(radius=glow_radius)
    )

    glow_edges = (
        np.asarray(blurred_edges).astype(np.float32) / 255.0
    )

    edge_color = np.array(
        config.get("edge_color", [25, 220, 255]),
        dtype=np.float32
    )

    glow_color = np.array(
        config.get("glow_color", [0, 110, 255]),
        dtype=np.float32
    )

    result = base.astype(np.float32)

    result += (
        sharp_edges[:, :, np.newaxis]
        * edge_color
        * config.get("edge_brightness", 1.5)
    )

    result += (
        glow_edges[:, :, np.newaxis]
        * glow_color
        * config.get("edge_glow_intensity", 0.9)
    )

    height, width = frame.shape[:2]

    pulse_period = max(
        1.0,
        config.get("pulse_period", 4.0)
    )

    pulse_position = (t % pulse_period) / pulse_period
    pulse_y = int(pulse_position * height)

    pulse_width = max(1, int(height * 0.025))

    y = np.arange(height).reshape(-1, 1)

    pulse_strength = np.clip(
        1.0 - np.abs(y - pulse_y) / pulse_width,
        0,
        1
    )

    pulse_intensity = config.get("pulse_intensity", 0.12)

    result[:, :, 1] += pulse_strength * 90 * pulse_intensity
    result[:, :, 2] += pulse_strength * 130 * pulse_intensity

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_time_rift(frame, t, config, get_frame):

    original = frame.astype(np.float32)

    result = apply_futuristic_color(
        frame,
        {
            "red": config.get("red", 0.92),
            "green": config.get("green", 0.96),
            "blue": config.get("blue", 1.12),
            "contrast": config.get("contrast", 1.08),
            "brightness": config.get("brightness", 1.0)
        }
    ).astype(np.float32)

    delays = config.get(
        "echo_delays",
        [0.08, 0.16, 0.24]
    )

    echo_strengths = config.get(
        "echo_strengths",
        [0.38, 0.27, 0.17]
    )

    motion_threshold = config.get("motion_threshold", 14)
    motion_range = max(1, config.get("motion_range", 45))
    motion_blur = config.get("motion_blur", 3)

    echo_colors = [
        np.array([0.65, 0.95, 1.25], dtype=np.float32),
        np.array([1.15, 0.72, 1.20], dtype=np.float32),
        np.array([0.75, 0.78, 1.30], dtype=np.float32)
    ]

    for index, delay in enumerate(delays):

        if t < delay:
            continue

        previous_frame = get_frame(t - delay).astype(np.float32)

        difference = np.max(
            np.abs(original - previous_frame),
            axis=2
        )

        motion_mask = np.clip(
            (difference - motion_threshold) / motion_range,
            0,
            1
        )

        mask_image = Image.fromarray(
            (motion_mask * 255).astype(np.uint8)
        )

        mask_image = mask_image.filter(
            ImageFilter.GaussianBlur(radius=motion_blur)
        )

        motion_mask = (
            np.asarray(mask_image).astype(np.float32) / 255.0
        )

        color = echo_colors[
            min(index, len(echo_colors) - 1)
        ]

        tinted_echo = previous_frame * color

        strength = echo_strengths[
            min(index, len(echo_strengths) - 1)
        ]

        alpha = motion_mask[:, :, np.newaxis] * strength

        result = (
            result * (1.0 - alpha) +
            tinted_echo * alpha
        )

    pulse_period = max(
        1.0,
        config.get("pulse_period", 3.5)
    )

    pulse = 0.5 + 0.5 * np.sin(
        2 * np.pi * t / pulse_period
    )

    pulse_intensity = config.get("pulse_intensity", 0.035)

    result[:, :, 1] += pulse * 12 * pulse_intensity * 10
    result[:, :, 2] += pulse * 20 * pulse_intensity * 10

    return np.clip(result, 0, 255).astype(np.uint8)



def apply_wireframe(frame, t, config):

    height, width = frame.shape[:2]

    original = frame.astype(np.float32)

    gray = (
        original[:, :, 0] * 0.299 +
        original[:, :, 1] * 0.587 +
        original[:, :, 2] * 0.114
    )

    saturation = config.get("base_saturation", 0.72)

    base = (
        gray[:, :, np.newaxis] * (1.0 - saturation) +
        original * saturation
    )

    base[:, :, 0] *= config.get("base_red", 0.92)
    base[:, :, 1] *= config.get("base_green", 0.72)
    base[:, :, 2] *= config.get("base_blue", 1.12)

    base *= config.get("base_brightness", 0.68)

    gray_image = Image.fromarray(
        np.clip(gray, 0, 255).astype(np.uint8)
    )

    edges = gray_image.filter(ImageFilter.FIND_EDGES)

    edge_array = np.asarray(edges).astype(np.float32)

    threshold = config.get("edge_threshold", 22)
    strength = config.get("edge_strength", 3.2)

    edge_array = np.clip(
        (edge_array - threshold) * strength,
        0,
        255
    )

    edge_image = Image.fromarray(
        edge_array.astype(np.uint8)
    )

    thickness = max(3, int(config.get("edge_thickness", 3)))

    if thickness % 2 == 0:
        thickness += 1

    edge_image = edge_image.filter(
        ImageFilter.MaxFilter(thickness)
    )

    sharp_edges = (
        np.asarray(edge_image).astype(np.float32) / 255.0
    )

    glow_radius = config.get("glow_radius", 7)

    blurred_edges = edge_image.filter(
        ImageFilter.GaussianBlur(radius=glow_radius)
    )

    glow_edges = (
        np.asarray(blurred_edges).astype(np.float32) / 255.0
    )

    edge_color = np.array(
        config.get("edge_color", [185, 75, 255]),
        dtype=np.float32
    )

    glow_color = np.array(
        config.get("glow_color", [105, 25, 220]),
        dtype=np.float32
    )

    highlight_color = np.array(
        config.get("highlight_color", [255, 45, 170]),
        dtype=np.float32
    )

    result = base.copy()

    result += (
        sharp_edges[:, :, np.newaxis] *
        edge_color *
        config.get("edge_intensity", 1.15)
    )

    result += (
        glow_edges[:, :, np.newaxis] *
        glow_color *
        config.get("glow_intensity", 0.75)
    )

    highlight_threshold = config.get(
        "highlight_threshold", 110
    )

    highlight_mask = np.clip(
        (edge_array - highlight_threshold) / 100.0,
        0,
        1
    )

    result += (
        highlight_mask[:, :, np.newaxis] *
        highlight_color *
        config.get("highlight_intensity", 0.55)
    )

    grid_spacing = config.get("grid_spacing", 48)

    scale = min(height, width) / 720.0

    spacing = max(
        12,
        int(grid_spacing * scale)
    )

    y_coords, x_coords = np.indices((height, width))

    distance_x = np.minimum(
        x_coords % spacing,
        spacing - (x_coords % spacing)
    )

    distance_y = np.minimum(
        y_coords % spacing,
        spacing - (y_coords % spacing)
    )

    vertical_lines = np.clip(
        1.0 - distance_x / 1.5,
        0,
        1
    )

    horizontal_lines = np.clip(
        1.0 - distance_y / 1.5,
        0,
        1
    )

    grid_mask = np.maximum(
        vertical_lines,
        horizontal_lines
    )

    perspective = (
        0.45 + 0.55 * (y_coords / max(1, height - 1))
    )

    grid_mask *= perspective

    grid_color = np.array(
        config.get("grid_color", [95, 35, 160]),
        dtype=np.float32
    )

    result += (
        grid_mask[:, :, np.newaxis] *
        grid_color *
        config.get("grid_intensity", 0.30)
    )

    pulse_period = max(
        1.0,
        config.get("pulse_period", 4.0)
    )

    pulse_position = (t % pulse_period) / pulse_period
    pulse_y = int(pulse_position * height)

    pulse_width = max(1, int(height * 0.025))

    pulse_strength = np.clip(
        1.0 - np.abs(y_coords - pulse_y) / pulse_width,
        0,
        1
    )

    pulse_intensity = config.get("pulse_intensity", 0.10)

    result[:, :, 0] += pulse_strength * 110 * pulse_intensity
    result[:, :, 2] += pulse_strength * 140 * pulse_intensity

    return np.clip(result, 0, 255).astype(np.uint8)



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



def apply_futuristic_effect(frame, t, config, get_frame=None):

    if config.get("effect_type") == "thermal":
        frame = apply_thermal_vision(frame, config)
        frame = apply_futuristic_glow(frame, config)
        return frame

    if config.get("effect_type") == "cybernetic":
        frame = apply_cybernetic_vision(frame, t, config)
        frame = apply_futuristic_glow(frame, config)
        return frame

    if config.get("effect_type") == "wireframe":
        return apply_wireframe(frame, t, config)

    if config.get("effect_type") == "time_rift":

        if get_frame is None:
            return apply_futuristic_color(frame, config)

        return apply_time_rift(
            frame,
            t,
            config,
            get_frame
        )

    frame = apply_futuristic_color(frame, config)

    frame = apply_futuristic_glow(frame, config)

    frame = apply_scan_lines(frame, config)

    frame = apply_rgb_shift(frame, config)

    frame = apply_digital_glitch(frame, t, config)

    return frame

