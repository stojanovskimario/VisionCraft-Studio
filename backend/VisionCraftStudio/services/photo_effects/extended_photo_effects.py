
import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageOps,
)

RESAMPLE = Image.Resampling.LANCZOS


def _rgb(array):
    return Image.fromarray(
        np.uint8(np.clip(array, 0, 255))
    )


def _tone(image, red=1.0, green=1.0, blue=1.0,
          contrast=1.0, brightness=1.0, saturation=1.0):

    image = ImageEnhance.Color(image).enhance(saturation)

    array = np.asarray(image, dtype=np.float32).copy()
    array *= np.array([red, green, blue], dtype=np.float32)

    result = _rgb(array)
    result = ImageEnhance.Contrast(result).enhance(contrast)

    return ImageEnhance.Brightness(result).enhance(brightness)


def _vignette(image, strength=0.4):
    array = np.asarray(image, dtype=np.float32)
    h, w = array.shape[:2]

    xx = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    yy = np.linspace(-1, 1, h, dtype=np.float32)[:, None]

    mask = np.clip(
        1.0 - strength * (xx * xx + yy * yy) / 2.0,
        0.25,
        1.0,
    )

    return _rgb(array * mask[..., None])


def _grain(image, amount=4.0, seed=72):
    rng = np.random.default_rng(seed)
    array = np.asarray(image, dtype=np.float32)

    noise = rng.normal(
        0,
        amount,
        array.shape[:2],
    ).astype(np.float32)

    return _rgb(array + noise[..., None])


def _channel_shift(image, pixels=4):
    array = np.asarray(image, dtype=np.uint8)
    h, w = array.shape[:2]

    shift = max(1, min(int(pixels), max(1, w // 8)))
    x = np.arange(w)

    result = array.copy()

    result[:, :, 0] = array[
        :,
        np.clip(x + shift, 0, w - 1),
        0,
    ]

    result[:, :, 2] = array[
        :,
        np.clip(x - shift, 0, w - 1),
        2,
    ]

    return Image.fromarray(result)


def _bloom(image, radius=9, strength=0.15):
    blurred = image.filter(
        ImageFilter.GaussianBlur(radius)
    )

    return Image.blend(
        image,
        blurred,
        min(1.0, max(0.0, strength)),
    )


def _paper_background(size):
    w, h = size

    top = np.array([244, 235, 216], dtype=np.float32)
    bottom = np.array([209, 192, 167], dtype=np.float32)

    gradient = np.linspace(
        0, 1, h, dtype=np.float32
    )[:, None, None]

    pixels = top * (1 - gradient) + bottom * gradient

    return _rgb(
        np.broadcast_to(pixels, (h, w, 3))
    )


def _polaroid(image, size, caption):
    cw, ch = size

    card = Image.new(
        "RGBA",
        (cw, ch),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(card)

    draw.rounded_rectangle(
        (0, 0, cw - 1, ch - 1),
        radius=max(4, cw // 45),
        fill=(250, 248, 241, 255),
    )

    border = max(5, cw // 25)
    bottom = max(border * 3, ch // 6)

    photo = ImageOps.fit(
        image,
        (
            cw - 2 * border,
            ch - border - bottom,
        ),
        method=RESAMPLE,
    )

    card.paste(photo, (border, border))

    draw.text(
        (border + 3, ch - bottom + bottom // 4),
        caption,
        fill=(80, 73, 65, 255),
    )

    return card


def apply_extended_photo_effect(image, effect_id, config=None):
    image = image.convert("RGB")
    w, h = image.size


    if effect_id == "deep_ocean":
        result = _tone(
            image,
            red=0.62,
            green=1.10,
            blue=1.34,
            contrast=1.12,
            brightness=0.94,
            saturation=1.05,
        )

        array = np.asarray(
            result, dtype=np.float32
        ).copy()

        x = np.linspace(
            0, 1, w, dtype=np.float32
        )[None, :]

        y = np.linspace(
            0, 1, h, dtype=np.float32
        )[:, None]

        ray = np.maximum(
            0,
            np.cos((x - 0.18 - 0.35 * y) * 17),
        ) ** 14

        ray *= np.maximum(0, 1 - y) * 22

        array += ray[..., None] * np.array(
            [0.48, 0.82, 1.0]
        )

        return _vignette(_rgb(array), 0.24)


    if effect_id == "abyss":
        result = _tone(
            image,
            red=0.38,
            green=0.82,
            blue=1.27,
            contrast=1.30,
            brightness=0.72,
            saturation=0.86,
        )

        result = _vignette(result, 0.75)

        draw = ImageDraw.Draw(result)
        rng = np.random.default_rng(129)

        for _ in range(max(14, (w * h) // 28000)):
            x = int(rng.integers(w))
            y = int(rng.integers(h))
            r = max(1, round(min(w, h) / 300))

            draw.ellipse(
                (x-r, y-r, x+r, y+r),
                fill=(48, 158, 176),
            )

        return _bloom(
            result,
            max(2, min(w, h) // 110),
            0.10,
        )


    if effect_id == "faded_memories":
        result = _tone(
            image,
            red=1.07,
            green=1.01,
            blue=0.93,
            contrast=0.77,
            brightness=1.08,
            saturation=0.56,
        )

        array = np.asarray(
            result, dtype=np.float32
        )

        return _grain(
            _rgb(array * 0.90 + 20),
            4.0,
        )


    if effect_id == "wireframe_reality":
        base = np.asarray(
            _tone(image, 0.43, 0.63, 0.92, 1.2, 0.34, 0.52),
            dtype=np.float32,
        )

        edges = np.asarray(
            ImageOps.grayscale(image).filter(
                ImageFilter.FIND_EDGES
            ),
            dtype=np.float32,
        )

        edges = np.clip(
            (edges - 25) / 80,
            0,
            1,
        )[..., None]

        color = base + edges * np.array(
            [20, 220, 240],
            dtype=np.float32,
        )

        result = _rgb(color)
        draw = ImageDraw.Draw(result)

        spacing = max(35, w // 16)

        for x in range(0, w, spacing):
            draw.line(
                (x, 0, x, h),
                fill=(12, 52, 65),
                width=1,
            )

        for y in range(0, h, spacing):
            draw.line(
                (0, y, w, y),
                fill=(12, 52, 65),
                width=1,
            )

        return result


    if effect_id == "synthwave":
        array = np.asarray(
            image, dtype=np.float32
        )

        lum = np.asarray(
            ImageOps.grayscale(image),
            dtype=np.float32,
        ) / 255

        low = np.array(
            [34, 16, 85], dtype=np.float32
        )

        high = np.array(
            [255, 116, 173], dtype=np.float32
        )

        graded = low + lum[..., None] * (high - low)

        result = _rgb(
            array * 0.33 + graded * 0.67
        )

        draw = ImageDraw.Draw(result)
        horizon = int(h * 0.73)

        for y in np.linspace(
            horizon, h - 1, 6, dtype=int
        ):
            draw.line(
                (0, int(y), w, int(y)),
                fill=(150, 65, 169),
                width=1,
            )

        for x in np.linspace(-w, 2*w, 19):
            draw.line(
                (w//2, horizon, int(x), h),
                fill=(126, 45, 151),
                width=1,
            )

        return result

    if effect_id == "camcorder_90s":
        result = _tone(
            image,
            1.04, 1.03, 0.93,
            0.93, 1.03, 0.82,
        )

        result = _channel_shift(
            result,
            max(1, w // 350),
        )

        result = _grain(result, 4.5, 90)

        array = np.asarray(
            result, dtype=np.float32
        ).copy()

        array[::3, :, :] *= 0.95

        result = _rgb(array)
        draw = ImageDraw.Draw(result)

        pad = max(9, w // 45)

        draw.ellipse(
            (pad, pad, pad+9, pad+9),
            fill=(240, 42, 46),
        )

        draw.text(
            (pad+17, pad-2),
            "REC",
            fill=(245, 239, 223),
        )

        draw.text(
            (pad, h-pad-15),
            "00:00:00",
            fill=(243, 238, 226),
        )

        return result


    if effect_id == "golden_hour_cinema":
        result = _tone(
            image,
            red=1.22,
            green=1.10,
            blue=0.78,
            contrast=1.08,
            brightness=1.05,
            saturation=1.14,
        )

        return _vignette(
            _bloom(result, 14, 0.16),
            0.16,
        )


    if effect_id == "dark_moody":
        result = _tone(
            image,
            red=0.91,
            green=0.94,
            blue=1.04,
            contrast=1.36,
            brightness=0.76,
            saturation=0.67,
        )

        return _vignette(result, 0.53)


    if effect_id == "midnight_blue":
        gray = np.asarray(
            ImageOps.grayscale(image),
            dtype=np.float32,
        ) / 255

        shadows = np.array(
            [6, 13, 37],
            dtype=np.float32,
        )

        highlights = np.array(
            [95, 151, 207],
            dtype=np.float32,
        )

        result = _rgb(
            shadows
            + (gray ** 1.15)[..., None]
            * (highlights - shadows)
        )

        return _vignette(result, 0.47)


    if effect_id == "evidence_triptych":
        canvas = Image.new(
            "RGB",
            (w, h),
            (17, 20, 24),
        )

        draw = ImageDraw.Draw(canvas)

        border = max(5, w // 80)
        gap = max(3, w // 120)

        pane_w = max(
            1,
            (w - 2*border - 2*gap) // 3,
        )

        pane_h = max(
            1,
            h - 2*border,
        )

        variants = [
            ImageEnhance.Contrast(
                ImageOps.grayscale(image).convert("RGB")
            ).enhance(1.45),

            _tone(
                image, 0.68, 1.04, 1.18,
                1.25, 0.9, 0.68,
            ),

            _tone(
                image, 1.28, 0.71, 0.68,
                1.30, 0.8, 0.55,
            ),
        ]

        for index, source in enumerate(variants):
            x0 = border + index * (pane_w + gap)

            pane = ImageOps.fit(
                source,
                (pane_w, pane_h),
                method=RESAMPLE,
            )

            canvas.paste(pane, (x0, border))

            draw.rectangle(
                (
                    x0, border,
                    x0 + pane_w - 1,
                    border + pane_h - 1,
                ),
                outline=(195, 195, 191),
                width=max(1, border // 4),
            )

            draw.rectangle(
                (x0+5, border+5, x0+40, border+19),
                fill=(17, 20, 24),
            )

            draw.text(
                (x0+9, border+6),
                f"0{index+1}",
                fill=(240, 234, 219),
            )

        return canvas


    if effect_id == "chroma_bleed":
        result = _tone(
            image,
            1.09, 0.99, 1.09,
            1.07, 1.0, 1.14,
        )

        shifted = _channel_shift(
            result,
            max(2, w // 180),
        )

        result = Image.blend(
            result,
            shifted,
            0.78,
        )

        return _bloom(
            result,
            max(2, w // 450),
            0.10,
        )


    if effect_id == "window_light":
        array = np.asarray(
            _tone(
                image,
                1.04, 1.02, 0.96,
                0.95, 1.0, 0.91,
            ),
            dtype=np.float32,
        ).copy()

        xx = np.linspace(
            0, 1, w, dtype=np.float32
        )[None, :]

        yy = np.linspace(
            0, 1, h, dtype=np.float32
        )[:, None]

        beam = np.exp(
            -(
                (
                    xx - (0.10 + 0.55 * yy)
                ) / 0.21
            ) ** 2
        ) * (1 - 0.38 * yy)

        light = 0.87 + 0.45 * beam

        array *= light[..., None]

        array += beam[..., None] * np.array(
            [17, 12, 3],
            dtype=np.float32,
        )

        return _bloom(
            _rgb(array),
            11,
            0.10,
        )


    if effect_id == "wildflower":
        result = _tone(
            image,
            1.12, 1.13, 1.04,
            0.84, 1.10, 0.82,
        )

        result = Image.blend(
            result,
            Image.new("RGB", (w, h), (255, 239, 233)),
            0.09,
        )

        overlay = Image.new(
            "RGBA",
            (w, h),
            (0, 0, 0, 0),
        )

        draw = ImageDraw.Draw(overlay)
        rng = np.random.default_rng(81)

        for _ in range(max(10, (w*h)//70000)):
            x = int(rng.integers(w))
            y = int(rng.integers(h))

            r = int(
                rng.integers(
                    max(2, h//160),
                    max(3, h//45),
                )
            )

            color = (
                (251, 211, 190, 36)
                if rng.random() < 0.5
                else (207, 234, 176, 29)
            )

            draw.ellipse(
                (x-r, y-r, x+r, y+r),
                fill=color,
            )

        overlay = overlay.filter(
            ImageFilter.GaussianBlur(
                max(4, h//100)
            )
        )

        return Image.alpha_composite(
            result.convert("RGBA"),
            overlay,
        ).convert("RGB")


    if effect_id == "miniature_world":
        sharp = _tone(
            image,
            1.07, 1.05, 1.05,
            1.14, 1.06, 1.27,
        )

        blur = sharp.filter(
            ImageFilter.GaussianBlur(
                max(3, h * 0.016)
            )
        )

        xx = np.linspace(
            -1, 1, w, dtype=np.float32
        )[None, :]

        yy = np.linspace(
            -1, 1, h, dtype=np.float32
        )[:, None]

        ellipse = (
            (xx / 0.88)**2
            + ((yy + 0.03) / 0.47)**2
        )

        alpha = np.clip(
            (ellipse - 0.60) / 0.85,
            0,
            1,
        )

        alpha = alpha * alpha * (3 - 2 * alpha)

        result = (
            np.asarray(sharp, dtype=np.float32)
            * (1 - alpha[..., None])
            + np.asarray(blur, dtype=np.float32)
            * alpha[..., None]
        )

        return _rgb(result)


    if effect_id == "pencil_sketch":
        gray = np.asarray(
            ImageOps.grayscale(image),
            dtype=np.float32,
        )

        inverted = Image.fromarray(
            np.uint8(255 - gray)
        ).filter(
            ImageFilter.GaussianBlur(
                max(3, min(w, h) * 0.014)
            )
        )

        invblur = np.asarray(
            inverted,
            dtype=np.float32,
        )

        sketch = np.clip(
            gray * 255
            / np.maximum(255 - invblur, 6),
            0,
            255,
        )

        return _rgb(
            np.repeat(
                sketch[..., None],
                3,
                axis=2,
            )
        )


    if effect_id == "oil_painting":
        saturated = ImageEnhance.Color(
            image
        ).enhance(1.35)

        reduced = ImageOps.posterize(
            saturated,
            5,
        )

        return ImageEnhance.Contrast(
            reduced.filter(
                ImageFilter.ModeFilter(5)
            )
        ).enhance(1.13)


    if effect_id == "watercolor":
        smooth = image.filter(
            ImageFilter.ModeFilter(5)
        ).filter(
            ImageFilter.SMOOTH_MORE
        )

        smooth = ImageEnhance.Color(
            smooth
        ).enhance(0.82)

        smooth = ImageEnhance.Contrast(
            smooth
        ).enhance(0.88)

        result = Image.blend(
            smooth,
            Image.new("RGB", (w, h), "white"),
            0.12,
        )

        rng = np.random.default_rng(44)

        paper = rng.normal(
            0,
            2.6,
            (h, w, 1),
        ).astype(np.float32)

        return _rgb(
            np.asarray(result, dtype=np.float32)
            + paper
        )

    if effect_id == "photo_stack":
        canvas = _paper_background(
            (w, h)
        ).convert("RGBA")

        card_size = (
            max(70, int(w * 0.49)),
            max(90, int(h * 0.76)),
        )

        frames = [
            _tone(
                image,
                1.10, 1.04, 0.92,
                0.96, 1.05, 0.78,
            ),
            _tone(
                image,
                0.96, 1.04, 1.12,
                1.0, 0.98, 0.91,
            ),
            image,
        ]

        angles = [14, -12, 2]
        offsets = [-0.18, 0.18, 0.0]
        labels = ["MEMORY 01", "MEMORY 02", "TODAY"]

        for i in range(3):
            card = _polaroid(
                frames[i],
                card_size,
                labels[i],
            )

            rotated = card.rotate(
                angles[i],
                resample=Image.Resampling.BICUBIC,
                expand=True,
            )

            x = int(
                (w - rotated.width) / 2
                + w * offsets[i]
            )

            y = int(
                (h - rotated.height) / 2
                + (i % 2) * h * 0.018
            )

            shadow = Image.new(
                "RGBA",
                rotated.size,
                (16, 13, 12, 0),
            )

            shadow.putalpha(
                rotated.getchannel("A").filter(
                    ImageFilter.GaussianBlur(
                        max(2, h * 0.013)
                    )
                ).point(
                    lambda a: int(a * 0.36)
                )
            )

            canvas.alpha_composite(
                shadow,
                (
                    x + max(2, w//110),
                    y + max(2, h//90),
                ),
            )

            canvas.alpha_composite(
                rotated,
                (x, y),
            )

        return canvas.convert("RGB")

    raise ValueError(
        f"Unknown extended photo effect: {effect_id}"
    )
