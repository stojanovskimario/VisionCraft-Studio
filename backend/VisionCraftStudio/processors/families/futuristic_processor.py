
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

from VisionCraftStudio.services.effects.futuristic_service import (
    apply_futuristic_effect
)


def process_futuristic_effect(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None
):

    choices = choices or {}

    video = VideoFileClip(input_path)

    watermark_clip = None
    final_clip = None

    try:
        duration = video.duration
        fps = video.fps or 24

        processed_clip = video.transform(
            lambda get_frame, t: apply_futuristic_effect(
                get_frame(t),
                t,
                config
            )
        )

        final_clip = processed_clip

        if choices.get("watermark") and watermark_path:
            watermark_clip = ImageClip(watermark_path)

            watermark_width = max(1, int(video.w * 0.15))

            watermark_height = int(
                watermark_clip.h * watermark_width / watermark_clip.w
            )

            watermark_clip = (
                watermark_clip
                .resized(width=watermark_width)
                .with_duration(duration)
                .with_position(
                    _get_watermark_position(
                        choices.get("watermarkPosition", "top-right"),
                        video.w,
                        video.h,
                        watermark_width,
                        watermark_height
                    )
                )
            )

            final_clip = CompositeVideoClip(
                [processed_clip, watermark_clip],
                size=video.size
            ).with_duration(duration)

        if video.audio is not None:
            final_clip = final_clip.with_audio(video.audio)

        final_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=fps
        )

        return output_path

    finally:
        if final_clip is not None and final_clip is not video:
            final_clip.close()

        if watermark_clip is not None:
            watermark_clip.close()

        video.close()


def _get_watermark_position(
    position,
    video_width,
    video_height,
    watermark_width,
    watermark_height
):

    margin = 20

    positions = {
        "top-left": (margin, margin),
        "top-right": (
            video_width - watermark_width - margin,
            margin
        ),
        "bottom-left": (
            margin,
            video_height - watermark_height - margin
        ),
        "bottom-right": (
            video_width - watermark_width - margin,
            video_height - watermark_height - margin
        )
    }

    return positions.get(position, positions["top-right"])
