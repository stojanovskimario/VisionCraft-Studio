from django.shortcuts import render

# Create your views here.
import json
import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from VisionCraftStudio.processors.theme_processor import ThemeProcessor


def api_test(request):
    return JsonResponse({
        "message": "Django backend is connected!"
    })


@csrf_exempt
def process_video(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    video = request.FILES.get("video")
    theme = request.POST.get("theme")
    choices_json = request.POST.get("choices")

    if not video:
        return JsonResponse(
            {"error": "No video was uploaded."},
            status=400
        )

    if not theme:
        return JsonResponse(
            {"error": "No theme was provided."},
            status=400
        )

    if not choices_json:
        return JsonResponse(
            {"error": "No choices were provided."},
            status=400
        )

    try:
        choices = json.loads(choices_json)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid choices JSON."},
            status=400
        )

    if theme != "vintage":
        return JsonResponse(
            {"error": "Unsupported theme."},
            status=400
        )

    uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    processed_dir = os.path.join(settings.MEDIA_ROOT, "processed")

    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    file_id = uuid.uuid4().hex

    input_filename = f"{file_id}_{video.name}"
    output_filename = f"{file_id}_vintage.mp4"

    input_path = os.path.join(uploads_dir, input_filename)
    output_path = os.path.join(processed_dir, output_filename)

    with open(input_path, "wb+") as destination:
        for chunk in video.chunks():
            destination.write(chunk)

    processor = ThemeProcessor()

    result = processor.process_vintage(
        input_path,
        output_path,
        choices
    )

    return JsonResponse({
        "success": True,
        "video_url": settings.MEDIA_URL + "processed/" + output_filename,
        "result": result
    })