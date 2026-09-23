from VisionCraftStudio.processors.theme_processor import ThemeProcessor


input_video = "VisionCraftStudio/test_videos/sample.mp4"
output_video = "VisionCraftStudio/test_videos/vintage_final.mp4"


choices = {
    "grayscale": False,
    "rotate": 180,
    "speed": 0.5,
    "watermark": False
}


processor = ThemeProcessor()

result = processor.process_vintage(
    input_video,
    output_video,
    choices
)

print("Finished:", result)