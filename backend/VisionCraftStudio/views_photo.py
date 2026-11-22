from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from PIL import Image, UnidentifiedImageError

from VisionCraftStudio.processors.photo_effect_processor import (
    run_photo_effect,
)


@csrf_exempt
@require_POST
def process_photo_effect(request):

    photo = request.FILES.get("photo")
    effect_id = request.POST.get("effect_id", "").strip()

    if photo is None:
        return JsonResponse(
            {"error": "Please upload a photo."},
            status=400,
        )

    if not effect_id:
        return JsonResponse(
            {"error": "Please select an effect."},
            status=400,
        )

    if photo.size > 10 * 1024 * 1024:
        return JsonResponse(
            {"error": "Maximum upload size is 10 MB."},
            status=400,
        )

    try:
        with Image.open(photo) as image:

            if image.format not in (
                "JPEG",
                "PNG",
                "WEBP",
            ):
                return JsonResponse(
                    {"error": "Use JPG, PNG or WebP."},
                    status=400,
                )

            if image.width * image.height > 25_000_000:
                return JsonResponse(
                    {"error": "Image dimensions are too large."},
                    status=400,
                )

            image.load()

            result = run_photo_effect(
                image,
                effect_id,
            )

        output = BytesIO()

        result.save(
            output,
            format="JPEG",
            quality=92,
            optimize=True,
        )

        response = HttpResponse(
            output.getvalue(),
            content_type="image/jpeg",
        )

        response["Content-Disposition"] = (
            f'inline; filename="{effect_id}.jpg"'
        )

        return response

    except (UnidentifiedImageError, OSError):
        return JsonResponse(
            {"error": "Unable to read this image."},
            status=400,
        )

    except ValueError as error:
        return JsonResponse(
            {"error": str(error)},
            status=400,
        )