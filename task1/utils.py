import logging


def min_temp(forecast) -> (float, str):
    try:
        min_t = forecast[0]["main"]["temp"]
        for city in forecast:
            if min_t > city["main"]["temp"]:
                min_t = city["main"]["temp"]
        return min_t, city["name"]
    except (KeyError, TypeError):
        logging.error(f"Error: missing or invalid data for this city: {city}")


def avg_temp(forecast) -> float():
    try:
        return sum(city["main"]["temp"] for city in forecast) / len(forecast)
    except (KeyError, TypeError):
        logging.error(f"Error: missing or invalid data for this city: {city}")


def print_forecast(forecast):
    for city in forecast:
        print('-' * 30)
        try:
            print(f"{city['name']}:")
            print(f"description: {city['weather'][0]['description']}")
            print(f"temp: {city['main']['temp']} °F")
            print(f"humidity: {city['main']['humidity']}")
        except (KeyError, TypeError):
            logging.error(f"Error: missing or invalid data for this city: {city}")
