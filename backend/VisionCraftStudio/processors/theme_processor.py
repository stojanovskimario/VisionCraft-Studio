from VisionCraftStudio.services.video_service import (
    process_vintage_video,
    process_futuristic_video,
    process_retro_video,
    process_cinematic_video,
    process_noir_video,
    process_vhs_video,
    process_dreamy_video,
    process_action_video
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


    def process_cinematic(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_cinematic_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    def process_noir(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_noir_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    def process_vhs(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_vhs_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    def process_dreamy(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_dreamy_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )


    def process_action(
        self,
        input_path,
        output_path,
        choices,
        watermark_path=None
    ):
        return process_action_video(
            input_path,
            output_path,
            choices,
            watermark_path
        )

