from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.MirrorX import MirrorX
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from PIL import Image
import numpy as np

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


def process_vintage_video(input_path, output_path, choices):
    clip = VideoFileClip(input_path)

    first_part = clip.subclipped(0, 2)

    if choices.get("grayscale"):
        first_part = first_part.with_effects([BlackAndWhite()])

    rotation_angle = choices.get("rotate", 0)
    rotation_duration = choices.get("rotationDuration", 1)

    rotation_start = 2
    rotation_in_end = rotation_start + 1
    rotation_hold_end = rotation_in_end + rotation_duration
    rotation_out_end = rotation_hold_end + 1

    if rotation_angle != 0:

        # 0° → selected angle
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

        # Stay at selected angle
        rotation_hold = clip.subclipped(
            rotation_in_end,
            rotation_hold_end
        )

        def rotate_hold(get_frame, t):
            frame = get_frame(t)

            image = Image.fromarray(frame)
            image = image.rotate(rotation_angle, expand=True)

            return np.array(image)

        rotation_hold = rotation_hold.transform(rotate_hold)

        # Selected angle → 0°
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

        third_part = clip.subclipped(rotation_out_end)

        parts = [
            first_part,
            rotation_in,
            rotation_hold,
            rotation_out,
            third_part
        ]

    else:
        third_part = clip.subclipped(2)

        parts = [
            first_part,
            third_part
        ]

    speed_factor = choices.get("speed", 1)

    if speed_factor != 1:
        parts[-1] = parts[-1].with_effects([
            MultiplySpeed(speed_factor)
        ])

    final_video = concatenate_videoclips(
        parts,
        method="compose"
    )

    final_video.write_videofile(output_path)

    clip.close()

    for part in parts:
        part.close()

    final_video.close()

    return output_path