from moviepy.video.fx.MirrorX import MirrorX
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from moviepy import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from PIL import Image, ImageFilter
import numpy as np
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

def trim_video(input_path, output_path, start_time, end_time):
    clip = VideoFileClip(input_path)

    trimmed = clip.subclipped(start_time, end_time)

    trimmed.write_videofile(output_path)

    clip.close()
    trimmed.close()


def rotate_video(input_path, output_path, angle):
    clip = VideoFileClip(input_path)

    rotated = clip.rotated(angle)

    rotated.write_videofile(output_path)

    clip.close()
    rotated.close()


def resize_video(input_path, output_path, width, height):
    clip = VideoFileClip(input_path)

    resized = clip.resized((width, height))

    resized.write_videofile(output_path)

    clip.close()
    resized.close()


def mirror_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    mirrored = clip.with_effects([MirrorX()])

    mirrored.write_videofile(output_path)

    clip.close()
    mirrored.close()


def speed_up(input_path, output_path, factor):
    clip = VideoFileClip(input_path)

    faster = clip.with_effects([MultiplySpeed(factor)])

    faster.write_videofile(output_path)

    clip.close()
    faster.close()


def grayscale_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    gray = clip.with_effects([BlackAndWhite()])

    gray.write_videofile(output_path)

    clip.close()
    gray.close()


def process_futuristic_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def futuristic_color(get_frame, t):
        frame = get_frame(t)

        image = Image.fromarray(frame).convert("RGB")
        array = np.array(image).astype(np.float32)

        array[:, :, 0] *= 0.75
        array[:, :, 2] *= 1.25

        array = (array - 128) * 1.1 + 128

        array = np.clip(
            array,
            0,
            255
        ).astype(np.uint8)

        return array

    clip = clip.transform(futuristic_color)

    glitch_start = 2
    glitch_duration = 2
    glitch_intensity = 5
    glitch_end = min(
        glitch_start + glitch_duration,
        clip.duration
    )

    def futuristic_glitch(get_frame, t):
        frame = get_frame(t)

        if t < glitch_start or t >= glitch_end:
            return frame

        result = frame.copy()
        height, width, _ = result.shape

        shift = max(
            1,
            int(width * 0.01 * glitch_intensity)
        )

        result[:, :, 0] = np.roll(
            result[:, :, 0],
            shift,
            axis=1
        )

        result[:, :, 2] = np.roll(
            result[:, :, 2],
            -shift,
            axis=1
        )

        slice_height = max(
            2,
            height // (20 - glitch_intensity)
        )

        for y in range(0, height, slice_height):
            if np.random.random() < 0.35:
                slice_end = min(
                    y + slice_height,
                    height
                )

                slice_shift = np.random.randint(
                    -shift,
                    shift + 1
                )

                result[y:slice_end] = np.roll(
                    result[y:slice_end],
                    slice_shift,
                    axis=1
                )

        return result

    clip = clip.transform(futuristic_glitch)

    speed_factor = 1.3
    speed_start = 5
    speed_end = min(7, clip.duration)

    parts = []

    if speed_start > 0:
        parts.append(
            clip.subclipped(0, speed_start)
        )

    if speed_end > speed_start:
        speed_part = clip.subclipped(
            speed_start,
            speed_end
        )

        speed_part = speed_part.with_effects([
            MultiplySpeed(speed_factor)
        ])

        parts.append(speed_part)

    if speed_end < clip.duration:
        parts.append(
            clip.subclipped(speed_end)
        )

    final_video = concatenate_videoclips(
        parts,
        method="compose"
    )

    video_to_write = final_video
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(final_video.w * 0.2)
        max_height = int(final_video.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (margin, margin)

        elif position == "top-right":
            watermark_position = (
                final_video.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                final_video.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                final_video.w - watermark_clip.w - margin,
                final_video.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            final_video.duration
        )

        watermark_clip = watermark_clip.with_position(
            watermark_position
        )

        video_to_write = CompositeVideoClip([
            final_video,
            watermark_clip
        ])

    video_to_write.write_videofile(output_path)

    clip.close()

    for part in parts:
        part.close()

    if watermark_clip:
        watermark_clip.close()

    if video_to_write is not final_video:
        video_to_write.close()

    final_video.close()

    return output_path


def process_vintage_video(input_path, output_path, choices,watermark_path=None):
    clip = VideoFileClip(input_path)

    clip = clip.with_effects([BlackAndWhite()])

    parts = []

    rotation_start = 2
    rotation_duration = 1
    rotation_angle = 90

    rotation_in_end = rotation_start + 1
    rotation_hold_end = rotation_in_end + rotation_duration
    rotation_out_end = rotation_hold_end + 1


    if rotation_start > 0:
        before_rotation = clip.subclipped(
            0,
            rotation_start
        )
        parts.append(before_rotation)


    if rotation_angle != 0:

        rotation_in = clip.subclipped(
            rotation_start,
            rotation_in_end
        )

        def rotate_in(get_frame, t):
            angle = rotation_angle * t
            frame = get_frame(t)

            image = Image.fromarray(frame)
            image = image.rotate(angle, expand=True)

            return np.array(image)

        rotation_in = rotation_in.transform(rotate_in)

        rotation_hold = clip.subclipped(
            rotation_in_end,
            rotation_hold_end
        )

        def rotate_hold(get_frame, t):
            frame = get_frame(t)

            image = Image.fromarray(frame)
            image = image.rotate(
                rotation_angle,
                expand=True
            )

            return np.array(image)

        rotation_hold = rotation_hold.transform(rotate_hold)

        rotation_out = clip.subclipped(
            rotation_hold_end,
            rotation_out_end
        )

        def rotate_out(get_frame, t):
            angle = rotation_angle * (1 - t)
            frame = get_frame(t)

            image = Image.fromarray(frame)
            image = image.rotate(angle, expand=True)

            return np.array(image)

        rotation_out = rotation_out.transform(rotate_out)

        parts.extend([
            rotation_in,
            rotation_hold,
            rotation_out
        ])

        video_after_rotation = rotation_out_end

    else:
        video_after_rotation = rotation_start

    speed_factor = 1.5
    speed_start = 5
    speed_end = 7

    speed_start = max(
        speed_start,
        video_after_rotation
    )

    if speed_factor != 1 and speed_end > speed_start:

        if speed_start > video_after_rotation:
            before_speed = clip.subclipped(
                video_after_rotation,
                speed_start
            )
            parts.append(before_speed)

        speed_part = clip.subclipped(
            speed_start,
            speed_end
        )

        speed_part = speed_part.with_effects([
            MultiplySpeed(speed_factor)
        ])

        parts.append(speed_part)

        if speed_end < clip.duration:
            after_speed = clip.subclipped(
                speed_end
            )
            parts.append(after_speed)

    else:
        if video_after_rotation < clip.duration:
            after_rotation = clip.subclipped(
                video_after_rotation
            )
            parts.append(after_rotation)

    final_video = concatenate_videoclips(
        parts,
        method="compose"
    )

    video_to_write = final_video
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(final_video.w * 0.2)
        max_height = int(final_video.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (
                margin,
                margin
            )

        elif position == "top-right":
            watermark_position = (
                final_video.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                final_video.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                final_video.w - watermark_clip.w - margin,
                final_video.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            final_video.duration
        )

        watermark_clip = watermark_clip.with_position(
            watermark_position
        )

        video_to_write = CompositeVideoClip([
            final_video,
            watermark_clip
        ])

    video_to_write.write_videofile(
        output_path
    )

    clip.close()

    for part in parts:
        part.close()

    if watermark_clip:
        watermark_clip.close()

    if video_to_write is not final_video:
        video_to_write.close()

    final_video.close()

    return output_path


def process_retro_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def retro_color(get_frame, t):
        frame = get_frame(t)

        image = Image.fromarray(frame).convert("RGB")

        array = np.array(
            image
        ).astype(np.float32)

        array[:, :, 0] *= 1.12
        array[:, :, 1] *= 0.98
        array[:, :, 2] *= 0.82

        array = (
            (array - 128) * 0.9
        ) + 128

        array = np.clip(
            array,
            0,
            255
        ).astype(np.uint8)

        return array

    clip = clip.transform(retro_color)

    grain_intensity = 5

    def add_film_grain(get_frame, t):
        frame = get_frame(t)

        noise_strength = grain_intensity * 2.5

        noise = np.random.normal(
            0,
            noise_strength,
            frame.shape
        )

        result = frame.astype(
            np.float32
        ) + noise

        result = np.clip(
            result,
            0,
            255
        ).astype(np.uint8)

        return result

    clip = clip.transform(add_film_grain)

    vignette_intensity = 1

    def add_vignette(get_frame, t):
        frame = get_frame(t)

        height, width = frame.shape[:2]

        y, x = np.ogrid[:height, :width]

        center_x = width / 2
        center_y = height / 2

        distance = np.sqrt(
            ((x - center_x) / center_x) ** 2
            + ((y - center_y) / center_y) ** 2
        )

        mask = 1 - (
            distance * 0.35 * vignette_intensity
        )

        mask = np.clip(
            mask,
            0.2,
            1
        )

        result = frame.astype(
            np.float32
        ) * mask[..., None]

        return np.clip(
            result,
            0,
            255
        ).astype(np.uint8)

    clip = clip.transform(add_vignette)

    video_to_write = clip
    watermark_clip = None

    if choices.get("watermark") and watermark_path:
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (
                margin,
                margin
            )

        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                clip.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        )

        watermark_clip = watermark_clip.with_position(
            watermark_position
        )

        video_to_write = CompositeVideoClip([
            clip,
            watermark_clip
        ])

    video_to_write.write_videofile(output_path)

    if video_to_write is not clip:
        video_to_write.close()

    if watermark_clip:
        watermark_clip.close()

    clip.close()

    return output_path


def process_cinematic_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def cinematic_color(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max(t / 2, 0), 1)

        brightness = np.mean(frame, axis=2) / 255.0
        shadows = (1 - brightness)[..., None]
        highlights = brightness[..., None]

        graded = frame.copy()

        graded[:, :, 0] += (highlights[:, :, 0] * 20)
        graded[:, :, 1] += (highlights[:, :, 0] * 5)
        graded[:, :, 1] -= (shadows[:, :, 0] * 5)
        graded[:, :, 2] += (shadows[:, :, 0] * 20)
        graded[:, :, 2] -= (highlights[:, :, 0] * 8)

        result = (
            frame * (1 - strength)
            + graded * strength
        )

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cinematic_color)

    def cinematic_vignette(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max((t - 2) / 2, 0), 1)

        height, width = frame.shape[:2]

        y, x = np.ogrid[:height, :width]

        center_x = width / 2
        center_y = height / 2

        distance = np.sqrt(
            ((x - center_x) / center_x) ** 2
            + ((y - center_y) / center_y) ** 2
        )

        mask = 1 - (distance * 0.25 * strength)
        mask = np.clip(mask, 0.55, 1)

        result = frame * mask[..., None]

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cinematic_vignette)

    def cinematic_contrast(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max((t - 4) / 2, 0), 1)
        contrast_factor = 1 + (0.2 * strength)

        result = (frame - 128) * contrast_factor + 128

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cinematic_contrast)

    def cinematic_letterbox(get_frame, t):
        frame = get_frame(t).copy()

        height = frame.shape[0]
        bar_height = max(1, int(height * 0.08))

        frame[:bar_height, :, :] = 0
        frame[-bar_height:, :, :] = 0

        return frame

    clip = clip.transform(cinematic_letterbox)

    video_to_write = clip
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (margin, margin)

        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                clip.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        )

        watermark_clip = watermark_clip.with_position(
            watermark_position
        )

        video_to_write = CompositeVideoClip([
            clip,
            watermark_clip
        ])

    try:
        video_to_write.write_videofile(output_path)
    finally:
        if video_to_write is not clip:
            video_to_write.close()

        if watermark_clip is not None:
            watermark_clip.close()

        clip.close()

    return output_path


def process_noir_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    clip = clip.with_effects([BlackAndWhite()])

    def noir_contrast(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max(t / 3, 0), 1)
        contrast_factor = 1 + (0.4 * strength)

        result = (frame - 128) * contrast_factor + 128

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(noir_contrast)

    def noir_vignette(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max((t - 2) / 2, 0), 1)

        height, width = frame.shape[:2]
        y, x = np.ogrid[:height, :width]

        center_x = width / 2
        center_y = height / 2

        distance = np.sqrt(
            ((x - center_x) / center_x) ** 2
            + ((y - center_y) / center_y) ** 2
        )

        mask = 1 - (distance * 0.45 * strength)
        mask = np.clip(mask, 0.3, 1)

        result = frame * mask[..., None]

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(noir_vignette)

    def noir_grain(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        noise = np.random.normal(
            0,
            7,
            frame.shape[:2] + (1,)
        )

        result = frame + noise

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(noir_grain)

    video_to_write = clip
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (margin, margin)

        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                clip.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        ).with_position(watermark_position)

        video_to_write = CompositeVideoClip([
            clip,
            watermark_clip
        ])

    try:
        video_to_write.write_videofile(output_path)
    finally:
        if video_to_write is not clip:
            video_to_write.close()

        if watermark_clip is not None:
            watermark_clip.close()

        clip.close()

    return output_path


def process_vhs_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def vhs_color(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        gray = np.mean(frame, axis=2, keepdims=True)
        frame = gray + (frame - gray) * 0.75

        frame[:, :, 0] *= 1.08
        frame[:, :, 1] *= 1.02
        frame[:, :, 2] *= 0.92

        frame = (frame - 128) * 0.9 + 128

        return np.clip(frame, 0, 255).astype(np.uint8)

    clip = clip.transform(vhs_color)

    def vhs_scanlines(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        frame[::3, :, :] *= 0.82

        return np.clip(frame, 0, 255).astype(np.uint8)

    clip = clip.transform(vhs_scanlines)

    glitch_start = 2
    glitch_end = min(4, clip.duration)
    glitch_intensity = 5

    def vhs_glitch(get_frame, t):
        frame = get_frame(t)

        if t < glitch_start or t >= glitch_end:
            return frame

        result = frame.copy()
        height, width, _ = result.shape

        shift = max(1, int(width * 0.01 * glitch_intensity))

        result[:, :, 0] = np.roll(
            result[:, :, 0], shift, axis=1
        )

        result[:, :, 2] = np.roll(
            result[:, :, 2], -shift, axis=1
        )

        slice_height = max(2, height // 15)

        for y in range(0, height, slice_height):
            if np.random.random() < 0.25:
                end_y = min(y + slice_height, height)

                slice_shift = np.random.randint(
                    -shift, shift + 1
                )

                result[y:end_y] = np.roll(
                    result[y:end_y],
                    slice_shift,
                    axis=1
                )

        return result

    clip = clip.transform(vhs_glitch)

    def vhs_noise(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        noise = np.random.normal(
            0,
            4,
            frame.shape[:2] + (1,)
        )

        result = frame + noise

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(vhs_noise)

    video_to_write = clip
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20

        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (margin, margin)

        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                margin
            )

        elif position == "bottom-left":
            watermark_position = (
                margin,
                clip.h - watermark_clip.h - margin
            )

        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        ).with_position(watermark_position)

        video_to_write = CompositeVideoClip([
            clip,
            watermark_clip
        ])

    try:
        video_to_write.write_videofile(output_path)
    finally:
        if video_to_write is not clip:
            video_to_write.close()

        if watermark_clip is not None:
            watermark_clip.close()

        clip.close()

    return output_path


def process_dreamy_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def dreamy_brightness(get_frame, t):
        frame = get_frame(t).astype(np.float32)

        strength = min(max(t / 2, 0), 1)
        result = frame + (20 * strength)

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(dreamy_brightness)

    def dreamy_soft_focus(get_frame, t):
        frame = get_frame(t)

        strength = min(max((t - 2) / 2, 0), 1)

        if strength <= 0:
            return frame

        original = Image.fromarray(frame).convert("RGB")
        blurred = original.filter(
            ImageFilter.GaussianBlur(radius=3)
        )

        original_array = np.array(original).astype(np.float32)
        blurred_array = np.array(blurred).astype(np.float32)

        result = (
            original_array * (1 - strength * 0.45)
            + blurred_array * (strength * 0.45)
        )

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(dreamy_soft_focus)

    def dreamy_saturation(get_frame, t):
        frame = get_frame(t)

        strength = min(max((t - 4) / 2, 0), 1)

        if strength <= 0:
            return frame

        image = Image.fromarray(frame).convert("RGB")
        gray = np.array(
            image.convert("L")
        ).astype(np.float32)[..., None]

        color = np.array(image).astype(np.float32)

        result = gray + (color - gray) * (1 + 0.25 * strength)

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(dreamy_saturation)

    def dreamy_glow(get_frame, t):
        frame = get_frame(t)
        image = Image.fromarray(frame).convert("RGB")

        blurred = image.filter(ImageFilter.GaussianBlur(radius=8))

        original_array = np.array(image).astype(np.float32)
        blurred_array = np.array(blurred).astype(np.float32)

        brightness = np.mean(original_array, axis=2, keepdims=True)
        mask = np.clip((brightness - 130) / 125, 0, 1)

        result = original_array + blurred_array * mask * 0.18

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(dreamy_glow)

    video_to_write = clip
    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20
        position = choices.get(
            "watermarkPosition",
            "top-right"
        )

        if position == "top-left":
            watermark_position = (margin, margin)
        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                margin
            )
        elif position == "bottom-left":
            watermark_position = (
                margin,
                clip.h - watermark_clip.h - margin
            )
        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        ).with_position(watermark_position)

        video_to_write = CompositeVideoClip([
            clip,
            watermark_clip
        ])

    try:
        video_to_write.write_videofile(output_path)
    finally:
        if video_to_write is not clip:
            video_to_write.close()

        if watermark_clip is not None:
            watermark_clip.close()

        clip.close()

    return output_path


def process_action_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def action_zoom(get_frame, t):
        frame = get_frame(t)

        strength = min(max(t / 2, 0), 1)
        zoom_factor = 1 + 0.12 * strength

        height, width = frame.shape[:2]
        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)

        image = Image.fromarray(frame).resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        left = (new_width - width) // 2
        top = (new_height - height) // 2

        return np.array(
            image.crop((left, top, left + width, top + height))
        )

    clip = clip.transform(action_zoom)

    def action_shake(get_frame, t):
        frame = get_frame(t)

        if not 2 <= t <= 4:
            return frame

        height, width = frame.shape[:2]

        offset_x = int(5 * np.sin(t * 35))
        offset_y = int(4 * np.sin(t * 29))

        image = Image.fromarray(frame)

        expanded = image.resize(
            (width + 20, height + 20),
            Image.Resampling.LANCZOS
        )

        left = 10 + offset_x
        top = 10 + offset_y

        return np.array(
            expanded.crop((left, top, left + width, top + height))
        )

    clip = clip.transform(action_shake)

    def action_contrast(get_frame, t):
        frame = get_frame(t).astype(np.float32)
        contrast = 1.15

        result = (frame - 128) * contrast + 128

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(action_contrast)

    start = 4
    end = min(6, clip.duration)

    if end > start:
        before = clip.subclipped(0, start)
        action_section = clip.subclipped(start, end).with_effects(
            [MultiplySpeed(1.5)]
        )

        if end < clip.duration:
            after = clip.subclipped(end, clip.duration)
            video_clips = [before, action_section, after]
        else:
            video_clips = [before, action_section]

        video_to_write = concatenate_videoclips(
            video_clips,
            method="compose"
        )
    else:
        video_clips = [clip]
        video_to_write = clip

    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(video_to_write.w * 0.2)
        max_height = int(video_to_write.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20
        position = choices.get("watermarkPosition", "top-right")

        if position == "top-left":
            watermark_position = (margin, margin)
        elif position == "top-right":
            watermark_position = (
                video_to_write.w - watermark_clip.w - margin,
                margin
            )
        elif position == "bottom-left":
            watermark_position = (
                margin,
                video_to_write.h - watermark_clip.h - margin
            )
        else:
            watermark_position = (
                video_to_write.w - watermark_clip.w - margin,
                video_to_write.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            video_to_write.duration
        ).with_position(watermark_position)

        final_clip = CompositeVideoClip(
            [video_to_write, watermark_clip]
        )
    else:
        final_clip = video_to_write

    try:
        final_clip.write_videofile(output_path)
    finally:
        if final_clip is not video_to_write:
            final_clip.close()

        if watermark_clip is not None:
            watermark_clip.close()

        if video_to_write is not clip:
            video_to_write.close()

        for part in video_clips:
            if part is not clip:
                part.close()

        clip.close()

    return output_path


def process_cyberpunk_video(
    input_path,
    output_path,
    choices,
    watermark_path=None
):
    clip = VideoFileClip(input_path)

    def cyberpunk_colors(get_frame, t):
        frame = get_frame(t).astype(np.float32)
        strength = min(max(t / 2, 0), 1)

        red = frame[:, :, 0]
        green = frame[:, :, 1]
        blue = frame[:, :, 2]

        result = frame.copy()
        result[:, :, 0] = red * (1 + 0.12 * strength)
        result[:, :, 1] = green * (1 - 0.08 * strength)
        result[:, :, 2] = blue * (1 + 0.30 * strength)

        cyan_mask = np.minimum(green, blue) / 255.0
        result[:, :, 1] += cyan_mask * 18 * strength
        result[:, :, 2] += cyan_mask * 18 * strength

        luminance = (
            0.299 * result[:, :, 0]
            + 0.587 * result[:, :, 1]
            + 0.114 * result[:, :, 2]
        )
        shadow_mask = np.clip((100 - luminance) / 100, 0, 1)
        result *= (1 - 0.28 * shadow_mask[:, :, None])

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cyberpunk_colors)

    def cyberpunk_contrast(get_frame, t):
        frame = get_frame(t).astype(np.float32)
        strength = min(max((t - 2) / 2, 0), 1)
        contrast = 1 + 0.35 * strength

        result = (frame - 128) * contrast + 128
        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cyberpunk_contrast)

    def cyberpunk_glitch(get_frame, t):
        frame = get_frame(t).copy()

        if not 4 <= t <= 5:
            return frame

        height, width = frame.shape[:2]
        result = frame.copy()

        shift = 6
        result[:, shift:, 0] = frame[:, :-shift, 0]
        result[:, :-shift, 2] = frame[:, shift:, 2]

        band_y = int((t * 137) % max(height - 12, 1))
        band_height = min(8, height - band_y)

        if band_height > 0:
            band = result[band_y:band_y + band_height].copy()
            result[band_y:band_y + band_height] = np.roll(
                band, int(12 * np.sin(t * 90)), axis=1
            )

        return result

    clip = clip.transform(cyberpunk_glitch)

    def cyberpunk_glow(get_frame, t):
        frame = get_frame(t)

        if t < 5:
            return frame

        strength = min(max((t - 5) / 2, 0), 1)

        image = Image.fromarray(frame).convert("RGB")
        blurred = image.filter(ImageFilter.GaussianBlur(radius=8))

        original_array = np.array(image).astype(np.float32)
        blurred_array = np.array(blurred).astype(np.float32)

        brightness = np.mean(original_array, axis=2, keepdims=True)
        mask = np.clip((brightness - 100) / 155, 0, 1)

        result = original_array + blurred_array * mask * 0.22 * strength

        return np.clip(result, 0, 255).astype(np.uint8)

    clip = clip.transform(cyberpunk_glow)

    watermark_clip = None

    if watermark_path and choices.get("watermark"):
        watermark_clip = ImageClip(watermark_path)

        max_width = int(clip.w * 0.2)
        max_height = int(clip.h * 0.2)

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(watermark_clip.w * scale)
            )

        margin = 20
        position = choices.get("watermarkPosition", "top-right")

        if position == "top-left":
            watermark_position = (margin, margin)
        elif position == "top-right":
            watermark_position = (
                clip.w - watermark_clip.w - margin, margin
            )
        elif position == "bottom-left":
            watermark_position = (
                margin, clip.h - watermark_clip.h - margin
            )
        else:
            watermark_position = (
                clip.w - watermark_clip.w - margin,
                clip.h - watermark_clip.h - margin
            )

        watermark_clip = watermark_clip.with_duration(
            clip.duration
        ).with_position(watermark_position)

        final_clip = CompositeVideoClip([clip, watermark_clip])
    else:
        final_clip = clip

    try:
        final_clip.write_videofile(output_path)
    finally:
        if final_clip is not clip:
            final_clip.close()

        if watermark_clip is not None:
            watermark_clip.close()

        clip.close()

    return output_path


