from flask import Flask
from flask_cors import CORS
import pandas as pd
from .forecast import WeatherService
from .config import get_config
from flask import jsonify
from tabulate import tabulate
import logging
import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:password123@db:5432/weather'
db = SQLAlchemy(app)

CORS(app)

migrate = Migrate(app, db)

_config = get_config()

class CityWeather(db.Model):
    __tablename__ = 'city_weather'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    temperature = db.Column(db.Float())
    humidity = db.Column(db.Integer())

    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return f"{self.name}: {self.temperature}, {self.humidity}"


_weather_service= WeatherService(
    api_key= _config['API_KEY'],
    url = _config["URL"],
)

try:
    filepath = os.path.join(
        os.path.dirname(__file__), "city_name.csv"
    )
    _weather_service.load_available_cities(filepath)
except Exception as exc:
    print(
        "Sorry, could not load cities from file: ",
        "city_name.csv",
        "\nPlease, try to edit config file. Error:",
        str(exc),
    )
    sys.exit(1)

@app.route("/api/weather/<city>", methods=['GET'])
def forecast(city):
    if not _weather_service.validate_city(city):
        return jsonify({'errors': ['Not valid city']})
    forecast, errors = _weather_service.get_forecast([city])
    for error in errors:
        logging.info(error)

    city_weather = CityWeather(city, forecast['Temperature (C)'][city], forecast['Humidity (%)'][city])
    db.session.add(city_weather)
    db.session.commit()

    return jsonify({'forecast': forecast.to_dict(), 'errors': errors})

@app.route("/api/weather/random", methods=['GET'])
def random_forecast():
    cities = _weather_service.get_random_cities(5)
    forecast, errors = _weather_service.get_forecast(cities)
    for city in cities:
        city_weather = CityWeather(city, forecast['Temperature (C)'][city], forecast['Humidity (%)'][city],)
        db.session.add(city_weather)
        db.session.commit()
    agg_field = "Temperature (C)"
    aggregated = _weather_service.calculate_stats(forecast, agg_field)

    return jsonify({'forecast': forecast.T.to_dict(),'aggregated': aggregated, 'errors': errors})


@app.route("/api/database/get")
def get_cities():
    cities = db.session.query(CityWeather).order_by(CityWeather.id.desc()).limit(100).all()
    return {"cities": [{"id": city.id, "name": city.name, "temperature": city.temperature, "humidity": city.humidity} for city in cities]}


@app.route("/api/healthcheck", methods=['GET'])
def healthcheck():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
