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

    second_part = clip.subclipped(2, 3)

    rotation_angle = choices.get("rotate", 0)

    if rotation_angle != 0:

        def animated_rotate(get_frame, t):
            angle = rotation_angle * t
            frame = get_frame(t)

            image = Image.fromarray(frame)
            image = image.rotate(angle, expand=True)

            return np.array(image)

        second_part = second_part.transform(animated_rotate)

    third_part = clip.subclipped(3)

    speed_factor = choices.get("speed", 1)

    if speed_factor != 1:
        third_part = third_part.with_effects([
            MultiplySpeed(speed_factor)
        ])

    final_video = concatenate_videoclips(
        [first_part, second_part, third_part],
        method="compose"
    )

    final_video.write_videofile(output_path)

    clip.close()
    first_part.close()
    second_part.close()
    third_part.close()
    final_video.close()

    return output_path