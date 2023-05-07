"""UI controller."""
import argparse
import sys
import os

from .config import get_config
from .forecast import WeatherService


class CLI(object):
    """CLI Controller"""

    def __init__(self):
        """Init controller"""
        self.config = get_config()
        self.weather_service = WeatherService(
            self.config["url"],
            self.config["apikey"],
        )
        try:
            filepath = os.path.join(
                os.path.dirname(__file__), self.config["cities_csv"]
            )
            self.weather_service.load_available_cities(filepath)
        except Exception as exc:
            print(
                "Sorry, could not load cities from file: ",
                self.config["cities_csv"],
                "\nPlease, try to edit config file. Error:",
                str(exc),
            )
            sys.exit(1)

    def run(self):
        """Main program loop."""
        parser = argparse.ArgumentParser(
            prog="Get Cities Weather",
            description="Skip empty for 5 random cities or "
            'enter CUSTOM city name with ARG "--city"',
        )
        parser.add_argument("--city", dest="city", required=False, default=None)

        custom_city = parser.parse_args().city
        if custom_city and self.weather_service.validate_city(custom_city):
            print("Custom city name is specified, processing:")
            cities = [custom_city]
        elif custom_city:
            print("Validation of city name '{}' failed.".format(custom_city))
            print("This city is not supported by OpenWeatherAPI.")
            print("Please consider other city name or leave empty for random.")
            sys.exit(1)
        else:
            print("Getting 5 random cities and their weather forecast:")
            cities = self.weather_service.get_random_cities(5)

        forecast, errors = self.weather_service.get_forecast(cities)
        for error in errors:
            print(error)

        print(
            forecast
            if not forecast.empty
            else "Unfortunately, no weather data available."
        )

        if forecast.shape[0] > 1:
            agg_field = "Temperature (C)"
            aggregated = self.weather_service.calculate_stats(forecast, agg_field)
            print("\nAggregated values for cities by {}".format(agg_field))
            for title, measure in aggregated.items():
                print("{} : {}".format(title, measure))


if __name__ == "__main__":
    CLI().run()
