
import numpy as np

from PIL import (
    Image,
    ImageChops,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageOps,
)


RESAMPLE = Image.Resampling.LANCZOS


def apply_photo_effect(image, effect_id, config):

    image = ImageOps.exif_transpose(image).convert("RGB")

    image.thumbnail((2048, 2048), RESAMPLE)

    w, h = image.size

    if effect_id == "pixel_art":
        block = max(
            2,
            int(config.get("pixel_size", 12)),
        )

        small = image.resize(
            (
                max(1, w // block),
                max(1, h // block),
            ),
            Image.Resampling.BOX,
        )

        small = ImageOps.posterize(
            small,
            int(config.get("color_bits", 5)),
        )

        return small.resize(
            (w, h),
            Image.Resampling.NEAREST,
        )

    if effect_id == "mosaic":
        tile = max(
            5,
            int(config.get("tile_size", 18)),
        )

        grout = max(
            1,
            int(config.get("grout_width", 2)),
        )

        cols = (w + tile - 1) // tile
        rows = (h + tile - 1) // tile

        samples = image.resize(
            (cols, rows),
            Image.Resampling.BOX,
        )

        result = Image.new(
            "RGB",
            (w, h),
            (35, 37, 42),
        )

        draw = ImageDraw.Draw(result)

        for row in range(rows):
            for col in range(cols):

                x0 = col * tile + grout
                y0 = row * tile + grout

                x1 = min(
                    w - 1,
                    (col + 1) * tile - 1,
                )

                y1 = min(
                    h - 1,
                    (row + 1) * tile - 1,
                )

                if x1 >= x0 and y1 >= y0:
                    draw.rounded_rectangle(
                        (x0, y0, x1, y1),
                        radius=min(3, tile // 5),
                        fill=samples.getpixel(
                            (col, row)
                        ),
                    )

        return result

    if effect_id == "comic_book":

        bright = ImageEnhance.Color(
            image
        ).enhance(1.75)

        bright = ImageEnhance.Contrast(
            bright
        ).enhance(1.2)

        poster = ImageOps.posterize(
            bright,
            int(config.get("color_bits", 4)),
        )

        edges = ImageOps.grayscale(image)

        edges = edges.filter(
            ImageFilter.GaussianBlur(0.5)
        )

        edges = edges.filter(
            ImageFilter.FIND_EDGES
        )

        threshold = int(
            config.get("edge_threshold", 65)
        )

        ink = edges.point(
            lambda value: (
                0 if value > threshold else 255
            )
        )

        return ImageChops.multiply(
            poster,
            ink.convert("RGB"),
        )


    if effect_id == "classic_noir":

        gray = ImageOps.grayscale(image)

        gray = ImageEnhance.Contrast(
            gray
        ).enhance(1.75)

        pixels = np.asarray(
            gray,
            dtype=np.float32,
        )

        xx = np.linspace(
            -1, 1, w, dtype=np.float32
        )[None, :]

        yy = np.linspace(
            -1, 1, h, dtype=np.float32
        )[:, None]

        vignette = np.clip(
            1.0 - 0.40 * (
                xx * xx + yy * yy
            ),
            0.48,
            1.0,
        )

        pixels *= vignette

        return Image.fromarray(
            np.uint8(
                np.clip(pixels, 0, 255)
            )
        ).convert("RGB")


    if effect_id == "vintage_sepia":

        gray = np.asarray(
            ImageOps.grayscale(image),
            dtype=np.float32,
        )

        sepia = np.stack(
            (
                gray * 1.13 + 10,
                gray * 0.96 + 5,
                gray * 0.73,
            ),
            axis=-1,
        )

        result = Image.fromarray(
            np.uint8(
                np.clip(sepia, 0, 255)
            )
        )

        return ImageEnhance.Contrast(
            result
        ).enhance(0.95)


    if effect_id == "cyberpunk_neon":

        luminance = np.asarray(
            ImageOps.grayscale(image),
            dtype=np.float32,
        ) / 255.0

        dark = np.array(
            [9, 13, 35],
            dtype=np.float32,
        )

        mid = np.array(
            [0, 185, 221],
            dtype=np.float32,
        )

        bright = np.array(
            [255, 57, 190],
            dtype=np.float32,
        )

        ratio = np.where(
            luminance < 0.5,
            luminance * 2,
            (luminance - 0.5) * 2,
        )[..., None]

        first = np.where(
            luminance[..., None] < 0.5,
            dark,
            mid,
        )

        second = np.where(
            luminance[..., None] < 0.5,
            mid,
            bright,
        )

        color = (
            first * (1.0 - ratio)
            + second * ratio
        )

        original = np.asarray(
            image,
            dtype=np.float32,
        )

        color = (
            color * 0.82
            + original * 0.18
        )

        edges = ImageOps.grayscale(
            image
        ).filter(
            ImageFilter.FIND_EDGES
        )

        glow = np.asarray(
            edges.filter(
                ImageFilter.GaussianBlur(4)
            ),
            dtype=np.float32,
        ) / 255.0

        color += (
            glow[..., None]
            * np.array(
                [18, 55, 90],
                dtype=np.float32,
            )
        )

        return Image.fromarray(
            np.uint8(
                np.clip(color, 0, 255)
            )
        )

    raise ValueError(
        f"Unknown photo effect: {effect_id}"
    )