import time

import pandas as pd
import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def fetch_pokemon_names_and_url(limit:int = 150):
    response = requests.get(BASE_URL,params={"limit":limit},timeout = 2)
    response.raise_for_status()
    return response.json()["results"]

def fetch_pokemon_details(url:str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
