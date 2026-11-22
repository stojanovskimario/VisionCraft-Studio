
import math

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


def _uint8(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def _luma(frame):
    image = frame.astype(np.float32)
    return (
        image[..., 0] * 0.299
        + image[..., 1] * 0.587
        + image[..., 2] * 0.114
    )


def _edge_strength(gray):
    dx = np.zeros_like(gray)
    dy = np.zeros_like(gray)

    dx[:, 1:] = np.abs(gray[:, 1:] - gray[:, :-1])
    dy[1:, :] = np.abs(gray[1:, :] - gray[:-1, :])

    return dx + dy

def _build_watercolor(video, config):
    radius = max(
        0.3,
        config["wash_radius"] * min(video.w, video.h) / 720.0,
    )

    rng = np.random.default_rng(config["paper_seed"])

    paper_texture = rng.normal(
        0.0,
        config["paper_grain"],
        (video.h, video.w, 1),
    ).astype(np.float32)

    def transform(frame):
        image = Image.fromarray(frame).convert("RGB")

        wash = image.filter(
            ImageFilter.MedianFilter(size=3)
        )

        wash = wash.filter(
            ImageFilter.GaussianBlur(radius)
        )

        wash = ImageEnhance.Color(wash).enhance(
            config["saturation"]
        )

        colors = np.asarray(wash, dtype=np.float32)

        step = max(2, config["color_step"])
        flattened = np.floor(
            colors / step + 0.5
        ) * step

        blend = config["wash_mix"]

        colors = (
            colors * (1.0 - blend)
            + flattened * blend
        )

        paper = np.asarray(
            config["paper_color"],
            dtype=np.float32,
        )

        opacity = config["paper_opacity"]

        colors = (
            colors * (1.0 - opacity)
            + paper * opacity
        )

        colors += paper_texture

        return _uint8(colors)

    return transform

def _build_pencil_sketch(video, config):
    paper = np.asarray(
        config["paper_color"],
        dtype=np.float32,
    )

    ink = np.asarray(
        config["graphite_color"],
        dtype=np.float32,
    )

    def transform(frame):
        gray = _luma(frame)
        edges = _edge_strength(gray)

        shading = (
            (255.0 - gray) / 255.0
        ) * config["shading_strength"]

        outlines = np.clip(
            edges / config["edge_range"],
            0.0,
            1.0,
        ) * config["line_strength"]

        darkness = np.clip(
            shading + outlines,
            0.0,
            1.0,
        )

        image = (
            paper
            + darkness[..., None] * (ink - paper)
        )

        return _uint8(image)

    return transform

def _build_oil_painting(video, config):
    short_side = min(video.w, video.h)

    scale = min(
        1.0,
        config["working_short_side"] / short_side,
    )

    work_size = (
        max(1, round(video.w * scale)),
        max(1, round(video.h * scale)),
    )

    def transform(frame):
        image = Image.fromarray(frame).convert("RGB")

        reduced = image.resize(
            work_size,
            Image.Resampling.BILINEAR,
        )

        painted = reduced.filter(
            ImageFilter.MedianFilter(size=5)
        )

        painted = painted.filter(
            ImageFilter.SMOOTH_MORE
        )

        painted = ImageEnhance.Color(painted).enhance(
            config["saturation"]
        )

        painted = ImageEnhance.Contrast(painted).enhance(
            config["contrast"]
        )

        colors = np.asarray(
            painted,
            dtype=np.float32,
        )

        step = max(2, config["color_step"])

        colors = np.round(
            colors / step
        ) * step

        painted = Image.fromarray(
            _uint8(colors)
        )

        painted = painted.filter(
            ImageFilter.UnsharpMask(
                radius=config["brush_radius"],
                percent=config["brush_definition"],
                threshold=3,
            )
        )

        painted = painted.resize(
            (video.w, video.h),
            Image.Resampling.BICUBIC,
        )

        return np.asarray(painted)

    return transform

def _build_pixel_art(video, config):
    block_size = max(
        2,
        round(
            min(video.w, video.h)
            * config["block_ratio"]
        ),
    )

    size = (
        max(1, round(video.w / block_size)),
        max(1, round(video.h / block_size)),
    )

    levels = max(
        2,
        int(config["color_levels"]),
    )

    def transform(frame):
        image = Image.fromarray(frame).convert("RGB")

        image = image.resize(
            size,
            Image.Resampling.BILINEAR,
        )

        colors = np.asarray(
            image,
            dtype=np.float32,
        )

        colors = (
            np.round(
                colors * ((levels - 1) / 255.0)
            ) * (255.0 / (levels - 1))
        )

        pixelated = Image.fromarray(
            _uint8(colors)
        )

        return np.asarray(
            pixelated.resize(
                (video.w, video.h),
                Image.Resampling.NEAREST,
            )
        )

    return transform

def _build_ink_illustration(video, config):
    paper = np.asarray(
        config["paper_color"],
        dtype=np.float32,
    )

    ink = np.asarray(
        config["ink_color"],
        dtype=np.float32,
    )

    yy, xx = np.indices(
        (video.h, video.w)
    )

    hatch = (
        (xx + yy * 2) % config["hatch_spacing"]
    ) < config["hatch_width"]

    def transform(frame):
        gray = _luma(frame)
        edge = _edge_strength(gray)

        outline = np.clip(
            edge / config["edge_range"],
            0.0,
            1.0,
        )

        shadow = np.clip(
            (config["shadow_cutoff"] - gray) / 150.0,
            0.0,
            1.0,
        )

        ink_amount = np.maximum(
            outline,
            shadow * config["shadow_ink"],
        )

        hatch_strength = (
            hatch
            * shadow
            * config["hatch_strength"]
        )

        ink_amount = np.maximum(
            ink_amount,
            hatch_strength,
        )

        ink_amount = np.clip(
            ink_amount,
            0.0,
            1.0,
        )

        return _uint8(
            paper + ink_amount[..., None] * (ink - paper)
        )

    return transform

def _build_mosaic(video, config):
    width, height = video.w, video.h

    radius = max(
        5,
        min(width, height) * config["tile_radius_ratio"],
    )

    horizontal = math.sqrt(3.0) * radius
    vertical = 1.5 * radius

    interior = radius * (
        1.0 - config["grout_ratio"]
    )

    angles = [
        math.radians(i * 60 - 90)
        for i in range(6)
    ]

    tiles = []

    for row in range(
        -1,
        math.ceil(height / vertical) + 2,
    ):
        cy = row * vertical

        for column in range(
            -2,
            math.ceil(width / horizontal) + 3,
        ):
            cx = (
                column + 0.5 * (row % 2)
            ) * horizontal

            if cx < -radius or cx > width + radius:
                continue

            polygon = [
                (
                    round(cx + interior * math.cos(angle)),
                    round(cy + interior * math.sin(angle)),
                )
                for angle in angles
            ]

            sample_x = max(
                0,
                min(width - 1, round(cx)),
            )

            sample_y = max(
                0,
                min(height - 1, round(cy)),
            )

            tiles.append(
                (polygon, sample_x, sample_y)
            )

    grout = tuple(config["grout_color"])

    smoothing = ImageFilter.GaussianBlur(
        max(
            0.5,
            radius * config["sample_blur_ratio"],
        )
    )

    def transform(frame):
        source = Image.fromarray(frame).convert("RGB")

        source = ImageEnhance.Color(source).enhance(
            config["saturation"]
        )

        smooth = np.asarray(
            source.filter(smoothing)
        )

        result = Image.new(
            "RGB",
            (width, height),
            grout,
        )

        draw = ImageDraw.Draw(result)

        for polygon, x, y in tiles:
            color = tuple(
                int(value)
                for value in smooth[y, x]
            )

            draw.polygon(
                polygon,
                fill=color,
            )

        return np.asarray(result)

    return transform


ARTISTIC_EFFECTS = {
    "art_watercolor": _build_watercolor,
    "art_pencil_sketch": _build_pencil_sketch,
    "art_oil_painting": _build_oil_painting,
    "art_pixel_art": _build_pixel_art,
    "art_ink_illustration": _build_ink_illustration,
    "art_mosaic": _build_mosaic,
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

    right = video.w - watermark.w - margin
    bottom = video.h - watermark.h - margin

    positions = {
        "top-left": (margin, margin),
        "top-right": (right, margin),
        "bottom-left": (margin, bottom),
        "bottom-right": (right, bottom),
    }

    return watermark.with_duration(
        video.duration
    ).with_position(
        positions.get(position, positions["top-right"])
    )


def process_artistic_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    choices = choices or {}
    effect_type = config.get("effect_type")

    build_effect = ARTISTIC_EFFECTS.get(effect_type)

    if build_effect is None:
        raise ValueError(
            f"Unknown Artistic effect type: {effect_type}"
        )

    with VideoFileClip(input_path) as original:
        apply_effect = build_effect(
            original,
            config,
        )

        visual = original.image_transform(
            apply_effect
        )

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
                        **export_options,
                    )

        else:
            visual.write_videofile(
                output_path,
                **export_options,
            )

    return output_path
