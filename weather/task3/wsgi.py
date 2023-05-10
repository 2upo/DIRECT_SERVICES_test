from flask import Flask
from flask_cors import CORS
import pandas as pd
from forecast import WeatherService
from config import get_config
from flask import jsonify
from tabulate import tabulate
import logging
import os
app = Flask(__name__)
CORS(app)


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


@app.route("/api/weather/<city>", methods=['GET'])
def forecast(city: str):
    """
    Get forecast for given city from OpenWeatherApi.

    Arguments:
        city: query param.

    Returns: Response if 200
        {
            "errors": [],
            "forecast": {
                "Country Code": {
                "Sofia": "BG"
                },
                "Description": {
                "Sofia": "broken clouds"
                },
                "Humidity (%)": {
                "Sofia": 72
                },
                "Icon": {
                "Sofia": "04d"
                },
                "Temperature (C)": {
                "Sofia": 14
                },
                "Timestamp": {
                "Sofia": 1683629188
                },
                "Timezone": {
                "Sofia": 10800
                }
            }
        }
    """
    if not weather_service.validate_city(city):
        return jsonify({'errors': ['Not valid city']})
    forecast, errors = weather_service.get_forecast([city])
    for error in errors:
        logging.info(error)
    return jsonify({'forecast': forecast.to_dict(), 'errors': errors})

@app.route("/api/weather/random", methods=['GET'])
def random_forecast():
    """
    Get forecast for 5 random city from OpenWeatherApi.

    Returns: Response if 200
    {
    "aggregated": {
        "Average Temperature (C)": 16.4,
        "Maximum Temperature (C)": 20,
        "Minimum Temperature (C)": 12
    },
    "errors": [],
    "forecast": {
        "Cupar": {
        "Country Code": "GB",
        "Description": "few clouds",
        "Humidity (%)": 66,
        "Icon": "02d",
        "Temperature (C)": 17,
        "Timestamp": 1683629459,
        "Timezone": 3600
        },
        .... and 5 same ....
    }
    }
    """
    cities = weather_service.get_random_cities(5)
    forecast, errors = weather_service.get_forecast(cities)

    agg_field = "Temperature (C)"
    aggregated = weather_service.calculate_stats(forecast, agg_field)

    return jsonify({'forecast': forecast.T.to_dict(),'aggregated': aggregated, 'errors': errors})

@app.route("/api/healthcheck", methods=['GET'])
def healthcheck():
    """ healthcheck """
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
