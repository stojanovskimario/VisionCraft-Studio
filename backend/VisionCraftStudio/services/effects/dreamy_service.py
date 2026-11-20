import numpy as np
from PIL import Image, ImageFilter


_LUMA = np.array([0.299, 0.587, 0.114], dtype=np.float32)
_TONE_POINTS = np.array([0.0, 0.12, 0.28, 0.50, 0.72, 0.90, 1.0])


def _luma(rgb):
    return np.einsum("...c,c->...", rgb, _LUMA)[..., None]


def _smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def _tint(value):
    rgb = np.asarray(value, dtype=np.float32)
    return rgb - np.dot(rgb, _LUMA)


def _restore_chroma(tone, chroma):
    positive = np.maximum(chroma.max(axis=2, keepdims=True), 1e-6)
    negative = np.maximum(-chroma.min(axis=2, keepdims=True), 1e-6)
    limit = np.minimum(
        1.0,
        np.minimum((1.0 - tone) / positive, tone / negative),
    )
    return tone + chroma * limit


def make_dreamy_grade(width, height, config):
    curve = np.asarray(config["tone_curve"], dtype=np.float32)

    if (
        curve.shape != _TONE_POINTS.shape
        or not np.isfinite(curve).all()
        or np.any((curve < 0.0) | (curve > 1.0))
        or np.any(np.diff(curve) < 0.0)
    ):
        raise ValueError(
            "Dreamy tone_curve must have seven ordered values in [0, 1]."
        )

    saturation = float(config.get("saturation", 1.0))
    vibrance = float(config.get("vibrance", 0.0))
    clarity = float(config.get("clarity", 0.0))

    shadow_color = _tint(config.get("shadow_tint", [0.0, 0.0, 0.0]))
    highlight_color = _tint(config.get("highlight_tint", [0.0, 0.0, 0.0]))
    has_shadows = np.any(shadow_color)
    has_highlights = np.any(highlight_color)

    accents = [
        (np.deg2rad(center), np.cos(np.deg2rad(radius)), float(boost))
        for center, radius, boost in config.get("hue_accents", [])
    ]

    window_strength = float(config.get("window_strength", 0.0))
    window = None

    if window_strength > 0.0:
        x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :]
        y = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]

        if config.get("window_side", "left") == "right":
            x = 1.0 - x

        distance = np.sqrt((x / 0.82) ** 2 + ((y - 0.30) / 1.05) ** 2)
        window = (1.0 - _smoothstep(distance))[..., None]

    sunbreak_strength = float(config.get("sunbreak_strength", 0.0))
    sunbreak_start = float(config.get("sunbreak_start_seconds", 0.4))
    sunbreak_end = float(config.get("sunbreak_end_seconds", 2.2))
    sunbreak_duration = sunbreak_end - sunbreak_start

    if sunbreak_strength > 0.0 and sunbreak_duration <= 0.0:
        raise ValueError("Sunbreak must end after it starts.")

    blur = ImageFilter.GaussianBlur(
        max(0.65, 1.35 * min(width, height) / 720.0)
    )

    def apply_grade(frame, t=0.0):
        rgb = frame.astype(np.float32) / 255.0
        luma = np.clip(_luma(rgb), 0.0, 1.0)
        tone = np.interp(luma, _TONE_POINTS, curve).astype(np.float32)

        if window is not None:
            mids = 4.0 * luma * (1.0 - luma)
            tone += window_strength * window * mids * (1.0 - tone)

        if sunbreak_strength > 0.0:
            progress = _smoothstep((t - sunbreak_start) / sunbreak_duration)

            mids = 4.0 * luma * (1.0 - luma)
            tone += sunbreak_strength * progress * mids * (1.0 - tone)

        if clarity > 0.0:
            gray = Image.fromarray(
                np.rint(luma[..., 0] * 255.0).astype(np.uint8)
            )
            soft = np.asarray(
                gray.filter(blur), dtype=np.float32
            )[..., None] / 255.0

            detail = np.clip(luma - soft, -0.05, 0.05)

            confidence = _smoothstep((np.abs(detail) - 0.004) / 0.022)
            exposed = _smoothstep((luma - 0.07) / 0.20)
            tone += clarity * detail * confidence * exposed

        np.clip(tone, 0.0, 1.0, out=tone)

        red, green, blue = np.moveaxis(rgb, -1, 0)
        color_range = (rgb.max(axis=2) - rgb.min(axis=2))[..., None]
        gain = saturation + vibrance * (1.0 - color_range) ** 2

        if accents:
            hue = np.arctan2(
                np.sqrt(3.0) * (green - blue),
                2.0 * red - green - blue,
            )
            colorful = _smoothstep((color_range[..., 0] - 0.035) / 0.13)

            for center, edge, boost in accents:
                match = _smoothstep(
                    (np.cos(hue - center) - edge) / (1.0 - edge)
                )
                gain += (boost * match * colorful)[..., None]

        chroma = (rgb - luma) * gain

        if has_shadows:
            weight = (
                _smoothstep((0.67 - luma) / 0.46)
                * _smoothstep(luma / 0.14)
            )
            chroma += weight * shadow_color

        if has_highlights:
            weight = _smoothstep((luma - 0.34) / 0.37)
            weight *= 1.0 - 0.80 * _smoothstep((luma - 0.86) / 0.14)
            chroma += weight * highlight_color

        result = _restore_chroma(tone, chroma)
        return np.rint(np.clip(result, 0.0, 1.0) * 255.0).astype(np.uint8)

    return apply_grade


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


def process_dreamy_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    from moviepy import CompositeVideoClip, ImageClip, VideoFileClip

    if config.get("effect_type") != "dreamy_grade":
        raise ValueError(
            f"Unknown Dreamy effect type: {config.get('effect_type')}"
        )

    choices = choices or {}

    with VideoFileClip(input_path) as original:
        apply_grade = make_dreamy_grade(original.w, original.h, config)

        if float(config.get("sunbreak_strength", 0.0)) > 0.0:
            visual = original.transform(
                lambda get_frame, t: apply_grade(get_frame(t), t)
            )
        else:
            visual = original.image_transform(apply_grade)

        export = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": original.fps or 24,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as source:
                watermark = _position_watermark(
                    source,
                    visual,
                    choices.get("watermarkPosition", "top-right"),
                )

                with CompositeVideoClip(
                    [visual, watermark],
                    size=original.size,
                ) as output:
                    output.write_videofile(output_path, **export)
        else:
            visual.write_videofile(output_path, **export)

    return output_path