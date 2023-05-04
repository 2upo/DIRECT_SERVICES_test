import json
from requests.exceptions import RequestException, HTTPError
from requests import Session
from tenacity import (
    retry,
    wait_random,
    stop_after_attempt,
    retry_if_exception_type,
)
import logging
from os import environ as env
import sys
from conf import config


try:
    API_KEY = config["API_KEY"]
    URL = config["URL"]
except (KeyError, ValueError):
    logging.exception("Environment variable missing or invalid")
    sys.exit(1)


@retry(
    wait=wait_random(min=3, max=5),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(RequestException),
)
def get_forecast(session: Session, city: str) -> dict:
    try:
        response = session.get(URL, timeout=5, params={"q": city, "appid": API_KEY})
        response.raise_for_status()
        return json.loads(response.text)
    except RequestException as err:
        logging.error(f"Error connecting to server for {city}: {err}")


def validate(forecast: list) -> list:
    if not isinstance(forecast, dict):
        logging.error("response is not a dict")
        raise Exception("bad response from API")
    elif forecast.get("cod") != 200:
        logging.error(f"Error: {forecast.get('message')}")
        raise Exception("bad response from API")
    return forecast


def forecast(cities: list) -> list:
    forecast = []

    with Session() as session:
        for city in cities:
            try:
                response = get_forecast(session, city)
                data = validate(response)
                if data:
                    forecast.append(data)
            except Exception as e:
                logging.error(
                    f"Sorry, city with name {city} cound not be fetched from API. Error is {e}"
                )
    return forecast
