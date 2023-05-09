from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forecast import WeatherService
from .config import get_config
from tabulate import tabulate
import logging
import os
import sys
import pandas as pd
import json

config = get_config()

weather_service = WeatherService(
    api_key= config['API_KEY'],
    url = config["URL"],
)

try:
    filepath = os.path.join(
        os.path.dirname(__file__), "city_name.csv"
    )
    weather_service.load_available_cities(filepath)
except Exception as exc:
    print(
        "Sorry, could not load cities from file: ",
        "city_name.csv",
        "\nPlease, try to edit config file. Error:",
        str(exc),
    )
    sys.exit(1)


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def random_forecast(request):
    if request.method == 'GET':
        cities = weather_service.get_random_cities(5)
        forecast, errors = weather_service.get_forecast(cities)

        agg_field = "Temperature (C)"
        aggregated = weather_service.calculate_stats(forecast, agg_field)

        return JsonResponse({'forecast': forecast.T.to_dict(),'aggregated': aggregated, 'errors': errors})

@csrf_exempt
def forecast(request, city):
    if request.method == 'GET':
        if not weather_service.validate_city(city):
            return JsonResponse({'errors': ['Not valid city']})
        forecast, errors = weather_service.get_forecast([city])
        for error in errors:
            logging.info(error)
        return JsonResponse({'forecast': forecast.to_dict(), 'errors': errors})

@csrf_exempt
def healthcheck(request):
    return JsonResponse({"status": "healthy"})
