
import numpy as np
from PIL import Image, ImageFilter
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


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
