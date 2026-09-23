from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def api_test(request):
    return JsonResponse({
        "message": "Django backend is connected!"
    })