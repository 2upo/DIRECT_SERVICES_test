import pandas
from random import randrange

valid_cities = pandas.read_csv("city_name.csv")


def input_city() -> str:
    while True:
        city = input("Enter a city name: ")
        if not valid_cities[valid_cities["name"] == city].empty:
            return city
        else:
            logging.error(f"{city} is not a valid city name. Please try again.")


def get_rand_cities() -> list:
    cities = []
    dataset_len = 209578
    for i in range(5):
        id = randrange(0, dataset_len)
        cities.append(valid_cities["name"][id])
    return cities


def user_input() -> list:
    cities = []
    mode = ""

    while mode not in ["rand", "input"]:
        mode = input("Enter a mode(rand, input): ")
        if mode == 'rand':
            cities = get_rand_cities()
        elif mode == 'input':
            cities.append(input_city())
        else:
            logging.error(f"{mode} is not a valid mode. Please try again.")
    
    return cities
