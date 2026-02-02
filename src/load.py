import psycopg2
from psycopg2.extras import execute_values
from transform import load_raw_data, transform_weather_data
import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": "localhost",
    "port": 5432,
}

def load_cities(conn, cities):
    query = """
        INSERT INTO cities (name, country, latitude, longitude)
        VALUES %s
        ON CONFLICT (name) DO NOTHING;  -- idempotent
    """

    values = [
        (
            city["city_name"],   # Python key stays the same
            city["country"],
            city["latitude"],
            city["longitude"],
        )
        for city in cities.values()
    ]

    with conn.cursor() as cur:
        execute_values(cur, query, values)

def get_city_id_map(conn):
    query = "SELECT city_id, name FROM cities;"

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

    return {city_name: city_id for city_id, city_name in rows}

def load_measurements(conn, measurements, city_id_map):
    query = """
        INSERT INTO weather_measurements
        (
            city_id,
            timestamp,
            temperature,
            humidity,
            weather_main,
            weather_desc,
            wind_speed
        )
        VALUES %s
        ON CONFLICT (city_id, timestamp) DO NOTHING;  -- idempotent
    """

    values = [
        (
            city_id_map[m["city_name"]],
            m["measurement_time"],   # Python datetime
            m["temperature_c"],
            m["humidity"],
            m.get("weather_main"),
            m.get("weather_desc"),
            m.get("wind_speed"),
        )
        for m in measurements
    ]

    with conn.cursor() as cur:
        execute_values(cur, query, values)

if __name__ == "__main__":
    raw = load_raw_data("data/raw_weather.json")
    cities, measurements = transform_weather_data(raw)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True

    load_cities(conn, cities)
    city_id_map = get_city_id_map(conn)
    load_measurements(conn, measurements, city_id_map)

    conn.close()

    print("Data successfully loaded into PostgreSQL")
