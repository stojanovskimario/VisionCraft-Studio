import json
import requests

url = "http://127.0.0.1:8000/api/process-video/"

video_path = "VisionCraftStudio/test_videos/sample.mp4"

choices = {
    "grayscale": True,
    "rotate": 90,
    "rotationDuration": 2,
    "speed": 1.2
}

with open(video_path, "rb") as video:
    files = {
        "video": video
    }

    data = {
        "theme": "vintage",
        "choices": json.dumps(choices)
    }

    response = requests.post(
        url,
        files=files,
        data=data
    )

print("Status:", response.status_code)
print("Response:", response.text)