import numpy as np
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from PIL import Image, ImageFilter, ImageOps


def _uint8(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def _luminance(image):
    return (
        0.299 * image[..., 0]
        + 0.587 * image[..., 1]
        + 0.114 * image[..., 2]
    )


def _rgb(gray):
    return np.repeat(gray[..., None], 3, axis=2)


def _smoothstep(value):
    value = np.clip(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


def _add_grain(gray, t, fps, strength):
    if strength <= 0:
        return gray

    frame_number = max(0, round(t * fps))
    rng = np.random.default_rng(frame_number)
    return gray + rng.normal(0.0, strength, gray.shape)


def _build_classic_noir(video, config):
    contrast = config["contrast"]
    contrast_ramp = config["contrast_ramp_seconds"]
    vignette_strength = config["vignette_strength"]
    vignette_start = config["vignette_start_seconds"]
    vignette_end = config["vignette_end_seconds"]
    grain_strength = config["grain_strength"]
    fps = video.fps or 24

    if contrast_ramp <= 0:
        raise ValueError("Classic Noir contrast ramp must be positive.")

    distance = None

    if vignette_strength > 0:
        if vignette_end <= vignette_start:
            raise ValueError("Classic Noir vignette must end after it starts.")

        x = (np.arange(video.w, dtype=np.float32) - video.w / 2) / (video.w / 2)
        y = (np.arange(video.h, dtype=np.float32) - video.h / 2) / (video.h / 2)
        distance = np.sqrt(x[None, :] ** 2 + y[:, None] ** 2)

    def transform(get_frame, t):
        gray = get_frame(t)[..., 0].astype(np.float32)

        progress = np.clip(t / contrast_ramp, 0.0, 1.0)
        factor = 1.0 + (contrast - 1.0) * progress
        gray = np.clip((gray - 128.0) * factor + 128.0, 0, 255)

        if distance is not None:
            progress = np.clip(
                (t - vignette_start) / (vignette_end - vignette_start),
                0.0,
                1.0,
            )
            gray *= np.clip(
                1.0 - distance * vignette_strength * progress,
                0.3,
                1.0,
            )

        gray = _add_grain(gray, t, fps, grain_strength)
        return _uint8(_rgb(gray))

    return transform


def _build_midnight_blue(video, config):
    contrast = config["contrast"]
    tint_strength = config["tint_strength"]
    shadow_tint = np.array([-14.0, 4.0, 29.0], dtype=np.float32)

    def transform(get_frame, t):
        gray = _luminance(get_frame(t).astype(np.float32))
        gray = np.clip((gray - 128.0) * contrast + 128.0, 0, 255)

        shadow_weight = _smoothstep(1.0 - gray / 190.0) * tint_strength
        image = _rgb(gray) + shadow_weight[..., None] * shadow_tint
        return _uint8(image)

    return transform


def _build_red_evidence(video, config):
    hue_width = config["red_hue_width_degrees"]
    min_saturation = config["minimum_saturation"]

    if hue_width <= 0:
        raise ValueError("Red Evidence hue width must be positive.")

    def transform(get_frame, t):
        frame = get_frame(t)
        image = frame.astype(np.float32)
        gray = _rgb(_luminance(image))

        hsv = np.asarray(Image.fromarray(frame).convert("HSV"))
        hue = hsv[..., 0].astype(np.float32) * (360.0 / 256.0)
        saturation = hsv[..., 1].astype(np.float32) / 255.0

        red_distance = np.minimum(hue, 360.0 - hue)
        hue_weight = _smoothstep(1.0 - red_distance / hue_width)
        saturation_weight = _smoothstep((saturation - min_saturation) / 0.25)
        keep_color = (hue_weight * saturation_weight)[..., None]

        return _uint8(gray + (image - gray) * keep_color)

    return transform

def _build_focus_pull(video, config):
    sweep_seconds = config["sweep_seconds"]
    focus_width = config["focus_width"]
    feather_width = config["feather_width"]
    blur_radius = config["blur_radius"] * min(video.w, video.h) / 720.0

    x = np.linspace(0.0, 1.0, video.w, dtype=np.float32)
    blur = ImageFilter.GaussianBlur(radius=blur_radius)

    def transform(get_frame, t):
        gray = _luminance(get_frame(t).astype(np.float32))
        blurred = np.asarray(
            Image.fromarray(_uint8(gray)).filter(blur),
            dtype=np.float32,
        )

        phase = 0.5 - 0.5 * np.cos(2.0 * np.pi * t / sweep_seconds)
        center = 0.25 + 0.50 * phase
        distance = np.abs(x - center)

        sharpness = 1.0 - _smoothstep(
            (distance - focus_width / 2.0) / feather_width
        )
        result = blurred + (gray - blurred) * sharpness[None, :]

        return _uint8(_rgb(result))

    return transform


def _build_staccato_noir(video, config):
    motion_fps = float(config["motion_fps"])
    contrast = config["contrast"]

    if motion_fps <= 0:
        raise ValueError("Staccato Noir motion FPS must be positive.")

    motion_fps = min(motion_fps, video.fps or 24)

    def transform(get_frame, t):
        source_time = np.floor(t * motion_fps) / motion_fps
        frame = get_frame(source_time).astype(np.float32)

        gray = _luminance(frame)
        gray = (gray - 128.0) * contrast + 128.0

        return _uint8(_rgb(gray))

    return transform


def _build_evidence_triptych(video, config):
    width, height = video.w, video.h
    gutter = max(1, round(width * config["gutter_ratio"]))
    available_width = width - 2 * gutter

    if available_width < 3:
        def transform(get_frame, t):
            gray = _luminance(get_frame(t).astype(np.float32))
            return _uint8(_rgb(gray))

        return transform

    center_width = max(
        1,
        min(available_width - 2, round(available_width * config["center_share"])),
    )
    left_width = (available_width - center_width) // 2
    right_width = available_width - center_width - left_width

    center_x = left_width + gutter
    right_x = center_x + center_width + gutter
    background = config["background_level"]
    resampling = Image.Resampling.LANCZOS

    def transform(get_frame, t):
        gray = _luminance(get_frame(t).astype(np.float32))
        image = Image.fromarray(_uint8(gray))

        left = ImageOps.fit(
            image, (left_width, height),
            method=resampling, centering=(0.18, 0.5),
        )
        right = ImageOps.fit(
            image, (right_width, height),
            method=resampling, centering=(0.82, 0.5),
        )

        center = ImageOps.contain(
            image, (center_width, height), method=resampling,
        )

        canvas = Image.new("L", (width, height), color=background)
        canvas.paste(left, (0, 0))
        canvas.paste(
            center,
            (
                center_x + (center_width - center.width) // 2,
                (height - center.height) // 2,
            ),
        )
        canvas.paste(right, (right_x, 0))

        return _rgb(np.asarray(canvas))

    return transform


NOIR_EFFECTS = {
    "classic_noir": _build_classic_noir,
    "focus_pull": _build_focus_pull,
    "staccato_noir": _build_staccato_noir,
    "midnight_blue": _build_midnight_blue,
    "evidence_triptych": _build_evidence_triptych,
    "red_evidence": _build_red_evidence,
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


def process_noir_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}
    effect_type = config.get("effect_type")
    build_effect = NOIR_EFFECTS.get(effect_type)

    if build_effect is None:
        raise ValueError(f"Unknown Noir effect type: {effect_type}")

    with VideoFileClip(input_path) as original:
        source = original
        if effect_type == "classic_noir":
            source = original.with_effects([BlackAndWhite()])

        visual = source.transform(build_effect(original, config))

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