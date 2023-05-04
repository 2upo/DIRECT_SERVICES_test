import logging
from forecast import forecast
from utils import avg_temp, min_temp, print_forecast
from cli import user_input


if __name__ == "__main__":
    cities = user_input()
    forecast = forecast(cities)
    print_forecast(forecast)
    print("-" * 30)
    print(f"min temp: {min_temp(forecast)}")
    print(f"avg temp: {avg_temp(forecast)}")
