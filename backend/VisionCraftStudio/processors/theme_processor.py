from VisionCraftStudio.services.video_service import (
    process_vintage_video,
    process_futuristic_video,
    process_retro_video
)


class ThemeProcessor:

    def process_vintage(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_vintage_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    def process_futuristic(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_futuristic_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    def process_retro(
            self,
            input_path,
            output_path,
            choices,
            watermark_path=None
    ):
        return process_retro_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )