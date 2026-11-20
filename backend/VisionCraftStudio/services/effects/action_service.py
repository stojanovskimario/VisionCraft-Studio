import math

import numpy as np
from moviepy import (
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from PIL import Image, ImageFilter


ACTION_ACCENTS_ENABLED = True


def _accents(config):
    if not ACTION_ACCENTS_ENABLED:
        return {}
    return config.get("action_accents", {})


def _uint8(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def _ease(value):
    value = min(max(value, 0.0), 1.0)
    return value * value * (3.0 - 2.0 * value)


def _pulse(t, start, end, peak=0.5):
    if end <= start or not start < t < end:
        return 0.0

    position = (t - start) / (end - start)

    if position < peak:
        return _ease(position / peak)

    return _ease((1.0 - position) / (1.0 - peak))


def _contrast(frame, factor):
    if factor == 1.0:
        return frame

    image = (frame.astype(np.float32) - 128.0) * factor + 128.0
    return _uint8(image)


def _center_zoom(frame, factor, resample=Image.Resampling.LANCZOS):
    if factor <= 1.0:
        return frame

    height, width = frame.shape[:2]
    larger_width = max(width, int(width * factor))
    larger_height = max(height, int(height * factor))

    image = Image.fromarray(frame).resize(
        (larger_width, larger_height),
        resample,
    )

    left = (larger_width - width) // 2
    top = (larger_height - height) // 2

    return np.asarray(
        image.crop((left, top, left + width, top + height))
    )


def _build_classic_action(video, config):
    zoom_seconds = config["zoom_seconds"]
    zoom_amount = config["zoom_amount"]
    shake_start = config["shake_start_seconds"]
    shake_end = config["shake_end_seconds"]
    shake_x = config["shake_x_pixels"]
    shake_y = config["shake_y_pixels"]
    contrast = config["contrast"]
    taper_seconds = _accents(config).get("shake_taper_seconds", 0.0)

    def transform(get_frame, t):
        frame = get_frame(t)

        zoom_progress = min(max(t / zoom_seconds, 0.0), 1.0)
        frame = _center_zoom(frame, 1.0 + zoom_amount * zoom_progress)

        if shake_start <= t <= shake_end:
            height, width = frame.shape[:2]
            strength = 1.0

            if taper_seconds > 0.0:
                strength = _ease((shake_end - t) / taper_seconds)

            offset_x = int(shake_x * strength * math.sin(t * 35.0))
            offset_y = int(shake_y * strength * math.sin(t * 29.0))

            margin_x = max(
                abs(offset_x),
                round(max(10, math.ceil(abs(shake_x))) * strength),
            )
            margin_y = max(
                abs(offset_y),
                round(max(10, math.ceil(abs(shake_y))) * strength),
            )

            if margin_x or margin_y:
                expanded = Image.fromarray(frame).resize(
                    (width + 2 * margin_x, height + 2 * margin_y),
                    Image.Resampling.LANCZOS,
                )

                left = margin_x + offset_x
                top = margin_y + offset_y
                frame = np.asarray(
                    expanded.crop((left, top, left + width, top + height))
                )

        return _contrast(frame, contrast)

    return transform


def _build_impact_zoom(video, config):
    start = video.duration * config["start_fraction"]
    end = video.duration * config["end_fraction"]
    peak = 0.22
    peak_time = start + (end - start) * peak

    zoom_amount = config["zoom_amount"]
    contrast = config["contrast"]

    accents = _accents(config)
    recoil_amount = accents.get("recoil_amount", 0.0)
    recoil_end = min(
        end,
        peak_time + accents.get("recoil_seconds", 0.0),
    )

    def transform(get_frame, t):
        frame = get_frame(t)
        zoom = zoom_amount * _pulse(t, start, end, peak=peak)

        if recoil_amount > 0.0:
            zoom -= recoil_amount * _pulse(
                t, peak_time, recoil_end, peak=0.40
            )

        return _contrast(_center_zoom(frame, 1.0 + zoom), contrast)

    return transform


def _build_whip_tilt(video, config):
    width, height = video.w, video.h
    center_x = width / 2.0
    center_y = height / 2.0

    start = video.duration * config["start_fraction"]
    end = video.duration * config["end_fraction"]
    max_angle = config["max_angle_degrees"]
    contrast = config["contrast"]

    accents = _accents(config)
    blur_mix = accents.get("whip_blur_mix", 0.0)
    blur_angle = math.radians(accents.get("whip_blur_degrees", 0.0))

    def render_angle(frame, angle):
        if abs(angle) < 1e-5:
            return frame

        cosine = math.cos(angle)
        sine = math.sin(angle)

        zoom = max(
            abs(cosine) + abs(sine) * height / width,
            abs(cosine) + abs(sine) * width / height,
        )

        a = cosine / zoom
        b = sine / zoom
        d = -sine / zoom
        e = cosine / zoom

        matrix = (
            a,
            b,
            center_x - a * center_x - b * center_y,
            d,
            e,
            center_y - d * center_x - e * center_y,
        )

        tilted = Image.fromarray(frame).transform(
            (width, height),
            Image.Transform.AFFINE,
            matrix,
            resample=Image.Resampling.BICUBIC,
        )

        return np.asarray(tilted)

    def transform(get_frame, t):
        frame = get_frame(t)

        if not start < t < end:
            return _contrast(frame, contrast)

        progress = (t - start) / (end - start)
        phase = math.pi * progress

        angle = math.radians(
            max_angle * math.sin(2.0 * phase) * math.sin(phase)
        )
        tilted = render_angle(frame, angle)

        if blur_mix > 0.0 and blur_angle > 0.0:
            turn_rate = (
                math.cos(2.0 * phase) * math.sin(phase)
                + 0.5 * math.sin(2.0 * phase) * math.cos(phase)
            )
            mix = blur_mix * _ease((abs(turn_rate) - 0.45) / 0.55)

            if mix > 0.0:
                trail_angle = angle - math.copysign(
                    blur_angle * min(abs(turn_rate), 1.0),
                    turn_rate * max_angle,
                )
                trail = render_angle(frame, trail_angle).astype(np.float32)
                base = tilted.astype(np.float32)
                tilted = _uint8(base + (trail - base) * mix)

        return _contrast(tilted, contrast)

    return transform


def _build_velocity_streak(video, config):
    start = video.duration * config["start_fraction"]
    end = video.duration * config["end_fraction"]
    peak = 0.32
    peak_time = start + (end - start) * peak

    zoom_amount = config["streak_zoom"]
    opacity = config["streak_mix"]
    contrast = config["contrast"]

    accents = _accents(config)
    edge_release = accents.get("edge_release", 0.0)
    center_clarity = accents.get("center_clarity", 0.0)
    settle_end = min(
        video.duration,
        end + accents.get("settle_seconds", 0.0),
    )

    x = np.linspace(-1.0, 1.0, video.w, dtype=np.float32)[None, :]
    y = np.linspace(-1.0, 1.0, video.h, dtype=np.float32)[:, None]
    distance = np.sqrt(x * x + y * y)

    edge_mask = np.clip((distance - 0.28) / 0.85, 0.0, 1.0)[..., None]
    center_mask = np.clip(1.0 - distance / 0.68, 0.0, 1.0)[..., None]
    blur = ImageFilter.GaussianBlur(
        max(0.6, 1.2 * min(video.w, video.h) / 720.0)
    )

    def transform(get_frame, t):
        frame = get_frame(t)
        strength = _pulse(t, start, end, peak=peak)

        if strength > 0.0:
            base = frame.astype(np.float32)
            samples = base.copy()

            for tap in (0.35, 0.70, 1.0):
                samples += _center_zoom(
                    frame,
                    1.0 + zoom_amount * strength * tap,
                    resample=Image.Resampling.BILINEAR,
                )

            streak = samples / 4.0
            mix = opacity * strength * edge_mask

            if edge_release > 0.0 and t > peak_time:
                release = _ease((t - peak_time) / (end - peak_time))
                mix *= 1.0 - edge_release * release * edge_mask

            frame = _uint8(base + (streak - base) * mix)

        frame = _contrast(frame, contrast)

        settle = _pulse(t, end, settle_end, peak=0.30)
        if center_clarity > 0.0 and settle > 0.0:
            gray = Image.fromarray(frame).convert("L")
            sharp = np.asarray(gray, dtype=np.float32)
            soft = np.asarray(gray.filter(blur), dtype=np.float32)
            detail = np.clip(sharp - soft, -18.0, 18.0)[..., None]

            frame = _uint8(
                frame.astype(np.float32)
                + detail * center_mask * center_clarity * settle
            )

        return frame

    return transform


def _speed_windows_in_seconds(video, config):
    duration = video.duration
    scale = duration if config.get("speed_unit") == "fraction" else 1.0
    cursor = 0.0

    windows = sorted(
        config.get("speed_windows", []),
        key=lambda window: window[0],
    )

    for start, end, factor in windows:
        if factor <= 0.0:
            raise ValueError("Action speed factors must be positive.")
        if factor == 1.0:
            continue

        start = max(cursor, min(duration, start * scale))
        end = min(duration, end * scale)

        if end > start:
            yield start, end, factor
            cursor = end


def _build_contrast_only(video, config):
    contrast = config["contrast"]
    accents = _accents(config)
    highlight_softness = accents.get("slow_highlight_softness", 0.0)
    nudge_amounts = accents.get("rush_zoom_amounts", [])

    if not highlight_softness and not nudge_amounts:
        def transform(get_frame, t):
            return _contrast(get_frame(t), contrast)

        return transform

    windows = tuple(_speed_windows_in_seconds(video, config))

    def transform(get_frame, t):
        frame = get_frame(t)

        for index, (start, end, factor) in enumerate(windows):
            if not start <= t < end:
                continue

            if factor > 1.0 and index < len(nudge_amounts):
                nudge_end = min(
                    end,
                    start + accents.get("rush_nudge_seconds", 0.0) * factor,
                )
                nudge = nudge_amounts[index] * _pulse(
                    t, start, nudge_end, peak=0.23
                )
                frame = _center_zoom(frame, 1.0 + nudge)

            frame = _contrast(frame, contrast)

            if factor < 1.0 and highlight_softness > 0.0:
                fade = min(
                    accents.get("slow_highlight_fade_seconds", 0.16),
                    (end - start) / 2.0,
                )

                if fade > 0.0:
                    mix = _ease(min(t - start, end - t) / fade)
                else:
                    mix = 1.0

                image = frame.astype(np.float32)
                luma = (
                    0.299 * image[..., 0]
                    + 0.587 * image[..., 1]
                    + 0.114 * image[..., 2]
                )
                highlights = np.clip((luma - 170.0) / 85.0, 0.0, 1.0) ** 2
                frame = _uint8(
                    image - 255.0 * highlight_softness * mix * highlights[..., None]
                )

            return frame

        return _contrast(frame, contrast)

    return transform


ACTION_EFFECTS = {
    "classic_action": _build_classic_action,
    "action_impact_zoom": _build_impact_zoom,
    "action_slow_mo": _build_contrast_only,
    "action_whip_tilt": _build_whip_tilt,
    "action_velocity_streak": _build_velocity_streak,
    "action_double_rush": _build_contrast_only,
}


def _apply_speed_windows(video, config):
    parts = []
    cursor = 0.0

    for start, end, factor in _speed_windows_in_seconds(video, config):
        if start > cursor:
            parts.append(video.subclipped(cursor, start))

        segment = video.subclipped(start, end)
        parts.append(segment.with_effects([MultiplySpeed(factor)]))
        cursor = end

    if not parts:
        return video

    if cursor < video.duration:
        parts.append(video.subclipped(cursor, video.duration))

    if len(parts) == 1:
        return parts[0]

    return concatenate_videoclips(parts, method="chain")


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


def process_action_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}
    effect_type = config.get("effect_type")
    build_effect = ACTION_EFFECTS.get(effect_type)

    if build_effect is None:
        raise ValueError(f"Unknown Action effect type: {effect_type}")

    with VideoFileClip(input_path) as original:
        visual = original.transform(build_effect(original, config))
        retimed = _apply_speed_windows(visual, config)

        export_options = {
            "codec": "libx264",
            "audio_codec": "aac",
            "fps": original.fps or 24,
        }

        if watermark_path and choices.get("watermark"):
            with ImageClip(watermark_path) as watermark_source:
                watermark = _position_watermark(
                    watermark_source,
                    retimed,
                    choices.get("watermarkPosition", "top-right"),
                )

                with CompositeVideoClip(
                    [retimed, watermark],
                    size=original.size,
                ) as output:
                    output.write_videofile(output_path, **export_options)
        else:
            retimed.write_videofile(output_path, **export_options)

    return output_path