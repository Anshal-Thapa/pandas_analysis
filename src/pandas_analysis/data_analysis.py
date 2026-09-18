import time

import pandas as pd
import requests

from pandas_analysis.api_calls import fetch_pokemon_details, fetch_pokemon_names_and_url


def extract_pokemon_row(data: dict) -> dict:
    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
    return {
        "id": data["id"],
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "base_experience": data["base_experience"],
        "primary_type": data["types"][0]["type"]["name"],
        "hp": stats.get("hp"),
        "attack": stats.get("attack"),
        "special-attack": stats.get("special-attack"),
        "defense": stats.get("defense"),
        "special-defense": stats.get("special-defense"),
        "speed": stats.get("speed"),
    }


def fetch_pokemon_dataset(limit: int = 150) -> list[dict]:
    index = fetch_pokemon_names_and_url(limit=limit)
    rows = []
    for entry in index:
        try:
            detail = fetch_pokemon_details(entry["url"])
            rows.append(extract_pokemon_row(detail))
        except (requests.exceptions.RequestException, KeyError) as e:
            print(f"Skipping {entry['name']}: {e}")
        time.sleep(0.04)
    return pd.DataFrame(rows)


def clean(df:pd.DataFrame) -> pd.DataFrame:
    before_len = len(df)
    df = df.dropna(subset=["hp", "attack", "special-attack", "defense", "special-defense", "speed"])
    dropped = before_len - len(df)
    if dropped > 0:
        print(f"Removed {dropped} rows with missing stat.")
    df = df.drop_duplicates(subset="id")
    df["primary_type"] = df["primary_type"].astype("category")
    return df

def summarize_data_by_type(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("primary_type",observed=True)[["hp","attack","special-attack","defense","special-defense","speed"]].mean().round(1)

if __name__ == "__main__":
    df = fetch_pokemon_dataset(200)
    df = clean(df)
 
    print(f"\nLoaded {len(df)} Pokemon\n")
 
    print("=== Average stats by primary type ===")
    print(summarize_data_by_type(df))