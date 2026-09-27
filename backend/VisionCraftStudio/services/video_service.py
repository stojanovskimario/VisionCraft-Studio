from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.MirrorX import MirrorX
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from PIL import Image
import numpy as np
from moviepy import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip

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


    if choices.get("colorEffect"):

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

        clip = clip.transform(
            futuristic_color
        )


    glitch_start = choices.get(
        "glitchStart",
        0
    )

    glitch_duration = choices.get(
        "glitchDuration",
        2
    )

    glitch_intensity = choices.get(
        "glitchIntensity",
        5
    )

    glitch_end = min(
        glitch_start + glitch_duration,
        clip.duration
    )

    glitch_intensity = max(
        1,
        min(glitch_intensity, 10)
    )

    if choices.get("glitch"):

        def futuristic_glitch(
            get_frame,
            t
        ):
            frame = get_frame(t)

            if (
                t < glitch_start
                or t > glitch_end
            ):
                return frame

            result = frame.copy()

            height, width, _ = result.shape

            shift = max(
                1,
                int(
                    width
                    * 0.01
                    * glitch_intensity
                )
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
                height // (
                    20 - glitch_intensity
                )
            )

            for y in range(
                0,
                height,
                slice_height
            ):

                if np.random.random() < 0.35:

                    slice_end = min(
                        y + slice_height,
                        height
                    )

                    slice_shift = np.random.randint(
                        -shift,
                        shift + 1
                    )

                    result[
                        y:slice_end
                    ] = np.roll(
                        result[
                            y:slice_end
                        ],
                        slice_shift,
                        axis=1
                    )

            return result

        clip = clip.transform(
            futuristic_glitch
        )


    speed_factor = choices.get(
        "speed",
        1
    )

    if speed_factor != 1:

        speed_start = choices.get(
            "speedStart",
            0
        )

        speed_end = choices.get(
            "speedEnd",
            speed_start + 2
        )

        speed_start = max(
            0,
            speed_start
        )

        speed_end = min(
            clip.duration,
            speed_end
        )

        if speed_end > speed_start:

            parts = []

            if speed_start > 0:
                before_speed = clip.subclipped(
                    0,
                    speed_start
                )

                parts.append(
                    before_speed
                )

            speed_part = clip.subclipped(
                speed_start,
                speed_end
            )

            speed_part = speed_part.with_effects([
                MultiplySpeed(
                    speed_factor
                )
            ])

            parts.append(
                speed_part
            )

            if speed_end < clip.duration:
                after_speed = clip.subclipped(
                    speed_end
                )

                parts.append(
                    after_speed
                )

            clip = concatenate_videoclips(parts, method="compose")

    video_to_write = clip
    watermark_clip = None

    if (
        watermark_path
        and choices.get("watermark")
    ):

        watermark_clip = ImageClip(
            watermark_path
        )

        max_width = int(
            clip.w * 0.2
        )

        max_height = int(
            clip.h * 0.2
        )

        scale = min(
            max_width / watermark_clip.w,
            max_height / watermark_clip.h,
            1
        )

        if scale < 1:
            watermark_clip = watermark_clip.resized(
                width=int(
                    watermark_clip.w * scale
                )
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
                clip.w
                - watermark_clip.w
                - margin,
                margin
            )

        elif position == "bottom-left":

            watermark_position = (
                margin,
                clip.h
                - watermark_clip.h
                - margin
            )

        else:

            watermark_position = (
                clip.w
                - watermark_clip.w
                - margin,
                clip.h
                - watermark_clip.h
                - margin
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


    video_to_write.write_videofile(
        output_path
    )

    clip.close()

    if watermark_clip:
        watermark_clip.close()

    if video_to_write is not clip:
        video_to_write.close()

    return output_path


def process_vintage_video(input_path, output_path, choices,watermark_path=None):
    clip = VideoFileClip(input_path)

    if choices.get("grayscale"):
        clip = clip.with_effects([BlackAndWhite()])

    parts = []

    rotation_start = choices.get("rotationStart", 2)
    rotation_duration = choices.get("rotationDuration", 1)
    rotation_angle = choices.get("rotate", 0)

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


    speed_factor = choices.get("speed", 1)
    speed_start = choices.get(
        "speedStart",
        video_after_rotation
    )
    speed_end = choices.get(
        "speedEnd",
        speed_start + 2
    )

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

        # Keep watermark reasonably small
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