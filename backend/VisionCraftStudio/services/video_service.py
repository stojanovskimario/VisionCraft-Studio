from moviepy import VideoFileClip
from moviepy.video.fx.BlackAndWhite import BlackAndWhite

def trim_video(input_path, output_path, start_time, end_time):
    clip = VideoFileClip(input_path)

    trimmed = clip.subclipped(start_time, end_time)

    trimmed.write_videofile(output_path)

trim_video(
    "../test_videos/sample.mp4",
    "../test_videos/sample_trimmed.mp4",
    0,
    3
)

def rotate_video(input_path, output_path, angle):
    clip = VideoFileClip(input_path)

    rotated = clip.rotated(angle)

    rotated.write_videofile(output_path)

rotate_video(
    "../test_videos/sample.mp4",
    "../test_videos/sample_rotated.mp4",
    90
)

def resize_video(input_path, output_path, width, height):
    clip = VideoFileClip(input_path)

    resized = clip.resized((width, height))

    resized.write_videofile(output_path)

resize_video(
    "../test_videos/sample.mp4",
    "../test_videos/sample_resized.mp4",
    640,
    480
)

from moviepy.video.fx.MirrorX import MirrorX

def mirror_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    mirrored = clip.with_effects([MirrorX()])

    mirrored.write_videofile(output_path)

mirror_video(
    "../test_videos/sample.mp4",
    "../test_videos/sample_mirror.mp4"
)

from moviepy.video.fx.MultiplySpeed import MultiplySpeed

def speed_up(input_path, output_path, factor):
    clip = VideoFileClip(input_path)

    faster = clip.with_effects([MultiplySpeed(factor)])

    faster.write_videofile(output_path)

speed_up(
    "../test_videos/sample.mp4",
    "../test_videos/sample_faster.mp4",
    1.2
)

def grayscale_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    gray = clip.with_effects([BlackAndWhite()])

    gray.write_videofile(output_path)

grayscale_video(
    "../test_videos/sample.mp4",
    "../test_videos/sample_gray.mp4",
)

def remove_audio(input_path, output_path):
    clip = VideoFileClip(input_path)

    muted = clip.without_audio()

    muted.write_videofile(output_path)

remove_audio(
    "../test_videos/sample.mp4",
    "../test_videos/sample_noaudio.mp4"
)