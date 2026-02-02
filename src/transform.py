import json
from datetime import datetime

RAW_DATA_PATH = "data/raw_weather.json"


def load_raw_data(path):
    with open(path, "r") as f:
        return json.load(f)


def transform_weather_data(raw_data):
    cities = {}
    measurements = []

    for record in raw_data:
        city_name = record["city"]

        # City dimension
        if city_name not in cities:
            cities[city_name] = {
                "city_name": record["city"],
                "country": record["country"],
                "latitude": record["latitude"],
                "longitude": record["longitude"],
            }

        # Fact table
        measurements.append({
            "city_name": record["city"],
            "measurement_time": datetime.fromisoformat(record["timestamp"]),
            "temperature_c": record["temperature"],
            "humidity": record["humidity"],
        })

    return cities, measurements


if __name__ == "__main__":
    raw = load_raw_data(RAW_DATA_PATH)
    cities, measurements = transform_weather_data(raw)

    print(f"Cities transformed: {len(cities)}")
    print(f"Measurements transformed: {len(measurements)}")
