import pytest
from .forecast import *
import pandas as pd
from unittest.mock import patch

response = {
    "base": "stations",
    "clouds": {"all": 40},
    "cod": 200,
    "coord": {"lat": 42.6975, "lon": 23.3242},
    "dt": 1683223663,
    "id": 727011,
    "main": {
        "feels_like": 282.64,
        "humidity": 80,
        "pressure": 1022,
        "temp": 283.46,
        "temp_max": 283.86,
        "temp_min": 282.98,
    },
    "name": "Sofia",
    "sys": {
        "country": "BG",
        "id": 2033225,
        "sunrise": 1683170268,
        "sunset": 1683221348,
        "type": 2,
    },
    "timezone": 10800,
    "visibility": 10000,
    "weather": [
        {"description": "scattered clouds", "icon": "03n", "id": 802, "main": "Clouds"}
    ],
    "wind": {"deg": 360, "speed": 2.06},
}


@pytest.fixture(scope="module")
def weather_api():
    api = WeatherService(api_key="some api_key", url="some url")
    api.cities = pd.DataFrame(
        [
            {"name": "Sofia"},
            {"name": "Varna"},
            {"name": "some city"},
            {"name": "city"},
            {"name": "Gamarjoba"},
        ]
    )
    return api


def test_wether_service_init(weather_api):
    assert weather_api
    assert isinstance(weather_api.cities, pd.DataFrame)


def test_validate_city_positive(weather_api):
    assert weather_api.validate_city("Sofia")


def test_validate_city_negative(weather_api):
    assert not weather_api.validate_city("1234")


def test_get_random_cities(weather_api):
    number = 3
    rand_cities = weather_api.get_random_cities(number)
    assert set(rand_cities).issubset(set(weather_api.cities["name"]))
    assert len(rand_cities) == len(set(rand_cities)) == number


@patch.object(WeatherService, "_get_forecast", return_value=response)
def test_get_forecast(mock_get_forecast, weather_api):
    cities = ["New York", "Sofia", "Tokyo"]
    df, errors = weather_api.get_forecast(cities)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 4)
    assert df.index.tolist() == cities
    assert "Country Code" in df.columns.tolist()
    assert "Temperature (C)" in df.columns.tolist()
    assert "Humidity (%)" in df.columns.tolist()
    assert "Description" in df.columns.tolist()

    assert isinstance(errors, list)
    assert len(errors) == 0

    # Test case for invalid input
    with pytest.raises(TypeError):
        weather_api.get_forecast("invalid input")

    # Verify that _get_forecast was called for each city
    assert mock_get_forecast.call_count == len(cities)
    for city in cities:
        mock_get_forecast.assert_any_call(city)


def test_get_forecast_negative(weather_api):
    cities = ["New York", "Sofia", "Aboba"]
    with patch.object(weather_api, "_get_forecast", lambda x: 1/0 if x == "Aboba" else response) as mock_get_forecast:
        df, errors = weather_api.get_forecast(cities)

        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 4)
        assert df.index.tolist() == cities[:2]
        assert "Country Code" in df.columns.tolist()
        assert "Temperature (C)" in df.columns.tolist()
        assert "Humidity (%)" in df.columns.tolist()
        assert "Description" in df.columns.tolist()

        assert isinstance(errors, list)
        assert len(errors) == 1

        # Test case for invalid input
        with pytest.raises(TypeError):
            weather_api.get_forecast("invalid input")


def test_calculate_stats(weather_api):
    # Create a sample DataFrame with temperature and humidity data
    data = {
        'Temperature': [10, 20, 30, 40],
        'Humidity': [20, 30, 40, 50],
        'Description': ['Sunny', 'Cloudy', 'Rainy', 'Stormy']
    }
    df = pd.DataFrame(data)

    # Test the "Temperature" field
    result = weather_api.calculate_stats(df, 'Temperature')
    assert result['Minimum Temperature'] == 10
    assert result['Maximum Temperature'] == 40
    assert result['Average Temperature'] == 25

    # Test the "Humidity" field
    result = weather_api.calculate_stats(df, 'Humidity')
    assert result['Minimum Humidity'] == 20
    assert result['Maximum Humidity'] == 50
    assert result['Average Humidity'] == 35

    # Test that an exception is raised for an invalid DataFrame shape
    invalid_df = pd.DataFrame({'Invalid': []})
    with pytest.raises(ValueError):
        weather_api.calculate_stats(invalid_df, 'Temperature')