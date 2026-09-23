from VisionCraftStudio.services.video_service import process_vintage_video


class ThemeProcessor:

    def process_vintage(self, input_path, output_path, choices):
        return process_vintage_video(
            input_path,
            output_path,
            choices
        )