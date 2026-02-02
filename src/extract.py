import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OWM_API_KEY")

if not API_KEY:
    raise ValueError("OpenWeatherMap API key not found in .env file")

# OpenWeatherMap endpoint
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cities to extract data for
CITIES = ["New York", "London", "Tokyo", "Sydney", "Mumbai"]

def extract_weather_data():
    """
    Extract weather data from OpenWeatherMap API for predefined cities
    """
    all_data = []

    for city in CITIES:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch data for {city}: {response.text}")
            continue

        data = response.json()

        record = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            "timestamp": datetime.utcfromtimestamp(data["dt"]).isoformat(),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_main": data["weather"][0]["main"],
            "weather_desc": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

        all_data.append(record)

    return all_data


def save_raw_data(data, file_path="data/raw_weather.json"):
    os.makedirs("data", exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved raw data to {file_path}")


if __name__ == "__main__":
    weather_data = extract_weather_data()
    save_raw_data(weather_data)
