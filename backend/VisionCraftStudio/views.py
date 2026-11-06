from django.shortcuts import render

# Create your views here.
import json
import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from VisionCraftStudio.config.effects import EFFECTS
from VisionCraftStudio.processors.effect_processor import (
    process_effect as run_effect
)

import logging

from VisionCraftStudio.processors.theme_processor import ThemeProcessor

logger = logging.getLogger(__name__)


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
    watermark = request.FILES.get("watermark")

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

    if theme not in ["vintage", "futuristic", "retro", "cinematic", "noir", "vhs", "dreamy", "action",
                     "cyberpunk", "travel", "silent_film", "underwater"]:
        return JsonResponse(
            {"error": "Unsupported theme."},
            status=400
        )

    if choices.get("watermark") and not watermark:
        return JsonResponse(
            {"error": "Watermark was selected but no image was uploaded."},
            status=400
        )

    uploads_dir = os.path.join(
        settings.MEDIA_ROOT,
        "uploads"
    )

    processed_dir = os.path.join(
        settings.MEDIA_ROOT,
        "processed"
    )

    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    file_id = uuid.uuid4().hex

    input_filename = f"{file_id}_{os.path.basename(video.name)}"
    output_filename = f"{file_id}_{theme}.mp4"

    input_path = os.path.join(
        uploads_dir,
        input_filename
    )

    output_path = os.path.join(
        processed_dir,
        output_filename
    )

    with open(input_path, "wb+") as destination:
        for chunk in video.chunks():
            destination.write(chunk)

    watermark_path = None

    if watermark:
        watermark_filename = (
            f"{file_id}_watermark_"
            f"{os.path.basename(watermark.name)}"
        )

        watermark_path = os.path.join(
            uploads_dir,
            watermark_filename
        )

        with open(watermark_path, "wb+") as destination:
            for chunk in watermark.chunks():
                destination.write(chunk)

    processor = ThemeProcessor()

    if theme == "vintage":
        result = processor.process_vintage(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "futuristic":
        result = processor.process_futuristic(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "retro":
        result = processor.process_retro(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "cinematic":
        result = processor.process_cinematic(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "noir":
        result = processor.process_noir(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "vhs":
        result = processor.process_vhs(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "dreamy":
        result = processor.process_dreamy(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "action":
        result = processor.process_action(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "cyberpunk":
        result = processor.process_cyberpunk(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "travel":
        result = processor.process_travel(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "silent_film":
        result = processor.process_silent_film(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    elif theme == "underwater":
        result = processor.process_underwater(
            input_path,
            output_path,
            choices,
            watermark_path
        )

    return JsonResponse({
        "success": True,
        "video_url": settings.MEDIA_URL + "processed/" + output_filename,
        "result": result
    })



@csrf_exempt
def process_effect(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    video = request.FILES.get("video")
    watermark = request.FILES.get("watermark")

    effect_id = request.POST.get("effect_id")
    choices_json = request.POST.get("choices", "{}")

    if not video:
        return JsonResponse(
            {"error": "No video was uploaded."},
            status=400
        )

    if not effect_id:
        return JsonResponse(
            {"error": "No effect ID was provided."},
            status=400
        )

    allowed_extensions = {
        ".mp4", ".mov", ".avi", ".mkv", ".webm"
    }

    extension = os.path.splitext(video.name)[1].lower()

    if extension not in allowed_extensions:
        return JsonResponse(
            {"error": "Unsupported video file extension."},
            status=400
        )

    effect = EFFECTS.get(effect_id)

    if effect is None:
        return JsonResponse(
            {"error": "Unsupported effect."},
            status=400
        )

    try:
        choices = json.loads(choices_json)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid choices JSON."},
            status=400
        )

    if not isinstance(choices, dict):
        return JsonResponse(
            {"error": "Choices must be a JSON object."},
            status=400
        )

    if choices.get("watermark") and not watermark:
        return JsonResponse(
            {
                "error": (
                    "Watermark was selected but no image was uploaded."
                )
            },
            status=400
        )

    uploads_dir = os.path.join(
        settings.MEDIA_ROOT,
        "uploads"
    )

    processed_dir = os.path.join(
        settings.MEDIA_ROOT,
        "processed"
    )

    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    file_id = uuid.uuid4().hex

    input_filename = (
        f"{file_id}_{os.path.basename(video.name)}"
    )

    output_filename = f"{file_id}_{effect_id}.mp4"

    input_path = os.path.join(
        uploads_dir,
        input_filename
    )

    output_path = os.path.join(
        processed_dir,
        output_filename
    )

    watermark_path = None

    try:
        with open(input_path, "wb+") as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        if watermark:
            watermark_filename = (
                f"{file_id}_watermark_"
                f"{os.path.basename(watermark.name)}"
            )

            watermark_path = os.path.join(
                uploads_dir,
                watermark_filename
            )

            with open(watermark_path, "wb+") as destination:
                for chunk in watermark.chunks():
                    destination.write(chunk)

        result = run_effect(
            effect_id=effect_id,
            input_path=input_path,
            output_path=output_path,
            choices=choices,
            watermark_path=watermark_path
        )

        return JsonResponse({
            "success": True,
            "effect_id": effect_id,
            "effect_name": effect["name"],
            "video_url": (
                settings.MEDIA_URL
                + "processed/"
                + output_filename
            ),
            "result": result
        })

    except Exception:
        logger.exception(
            "Failed to process effect '%s'.",
            effect_id
        )

        if os.path.exists(output_path):
            os.remove(output_path)

        return JsonResponse(
            {"error": "Video processing failed. Check the backend logs."},
            status=500
        )

