from VisionCraftStudio.processors.theme_processor import ThemeProcessor


input_video = "VisionCraftStudio/test_videos/sample.mp4"
output_video = "VisionCraftStudio/test_videos/vintage_final.mp4"


choices = {
    "grayscale": True,
    "rotate": 90,
    "rotationDuration": 2,
    "speed": 1.2,
    "watermark": False
}


processor = ThemeProcessor()

result = processor.process_vintage(
    input_video,
    output_video,
    choices
)

print("Finished:", result)