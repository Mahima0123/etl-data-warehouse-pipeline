-- Drop tables if they exist
DROP TABLE IF EXISTS weather_measurements;
DROP TABLE IF EXISTS cities;

-- Cities table
CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(10),
    latitude NUMERIC,
    longitude NUMERIC
);

-- Weather measurements table
CREATE TABLE weather_measurements (
    measurement_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(city_id),
    timestamp TIMESTAMP NOT NULL,
    temperature NUMERIC,
    humidity INT,
    weather_main VARCHAR(50),
    weather_desc VARCHAR(100),
    wind_speed NUMERIC
);
