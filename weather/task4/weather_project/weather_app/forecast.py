"""OpenWeatherAPI Service"""
import pandas as pd
from typing import List, Tuple, Dict
from requests.exceptions import RequestException
from requests import Session
from tenacity import (
    retry,
    wait_random,
    stop_after_attempt,
    retry_if_exception_type,
)


class WeatherService:
    """OpenWeatherAPI service."""

    def __init__(self, url: str, api_key: str):
        self.cities = pd.DataFrame()
        self._url = url
        self._api_key = api_key

    def load_available_cities(self, filename: str) -> pd.DataFrame:
        """
        Load available cities from csv file to current class.

        Arguments:
            filename: csv file name, containing columns (id,name).
        """
        self.cities = pd.read_csv(filename)

    def validate_city(self, city_name: str) -> bool:
        """
        Validate if city name is recognized by OpenweatherAPI.

        Arguments:
            city_name: city name to validate.

        Returns:
            if city_name is supported by API.
        """
        return not bool(self.cities[self.cities["name"] == city_name].empty)

    def get_random_cities(self, number: int = 5) -> List[str]:
        """
        Get random cities names from list of available cities.

        Arguments:
            number: number of random cities to get.

        Return:
            list of cities names.
        """
        return list(
            map(lambda x: x[1]["name"], self.cities.sample(n=number).iterrows())
        )

    def get_forecast(self, city_names: List[str]) -> Tuple[pd.DataFrame, Exception]:
        """
        Get formatted weather information by cities names.

        Argument:
            city_names: valid cities names as strings.

        Return:
            (DataFrame for outputing, list of exceptions)
        """
        result = {}
        errors = []
        if type(city_names) != list:
            raise TypeError("Invalid type for city_names: {}".format(type(city_names)))

        self._session = Session()

        for city in city_names:
            try:
                weather_data = self._get_forecast(city)

                result[city] = {
                    "Country Code": weather_data["sys"]["country"],
                    "Temperature (C)": int(round(weather_data["main"]["temp"] - 272.15, 1)),
                    "Humidity (%)": weather_data["main"]["humidity"],
                    "Description": weather_data["weather"][0]["description"],
                    "Icon": weather_data["weather"][0]["icon"],
                    "Timestamp": weather_data["dt"],
                    "Timezone": weather_data["timezone"]
                }
            except Exception as exc:
                errors.append(
                    "Error occured while requesting forecast"
                    " for city {}".format(city)
                )

        self._session.close()
        # Transpose DataFrame to Get cities as rows.
        return pd.DataFrame(result).T, errors

    @retry(
        wait=wait_random(min=1, max=7),
        stop=stop_after_attempt(2),
        retry=retry_if_exception_type(RequestException),
        reraise=True,
    )
    def _get_forecast(self, city: str) -> dict:
        """
        Get forecast from OpenweatherAPI for given city name.

        Arguments:
            city: string name of city.

        Returns:
            Deserialized json response.

        Example:
            Expected response from API:
            {'base': 'stations',
            'clouds': {'all': 40},
            'cod': 200,
            'coord': {'lat': 42.6975, 'lon': 23.3242},
            'dt': 1683223663,
            'id': 727011,
            'main': {'feels_like': 282.64,
                    'humidity': 80,
                    'pressure': 1022,
                    'temp': 283.46,
                    'temp_max': 283.86,
                    'temp_min': 282.98},
            'name': 'Sofia',
            'sys': {'country': 'BG',
                    'id': 2033225,
                    'sunrise': 1683170268,
                    'sunset': 1683221348,
                    'type': 2},
            'timezone': 10800,
            'visibility': 10000,
            'weather': [{'description': 'scattered clouds',
                        'icon': '03n',
                        'id': 802,
                        'main': 'Clouds'}],
            'wind': {'deg': 360, 'speed': 2.06}}
        """
        response = self._session.get(
            self._url, timeout=5, params={"q": city, "appid": self._api_key}
        )
        response.raise_for_status()

        data = response.json()
        if data.get("cod") != 200:
            raise Exception(
                "Non-200 status code. Msg: {}".format(data.get("message", "No message"))
            )
        return data

    @classmethod
    def calculate_stats(
        cls,
        df: pd.DataFrame,
        field: str,
    ) -> Dict[str, str]:
        """
        Aggregate weather data.

        Arguments:
            df: dataframe, containing "Temperature",
                "Humidity" and "Description" as columns.
            field: df field to compute stats.
        """
        try:
            return {
                f"Minimum {field}": df[field].min(),
                f"Maximum {field}": df[field].max(),
                f"Average {field}": df[field].mean(),
            }
        except Exception:
            raise ValueError("Given DataFrame shape is invalid.")
