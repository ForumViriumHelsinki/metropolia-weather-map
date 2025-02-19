CREATE DATABASE weather_alt;

\c weather_alt

CREATE SCHEMA IF NOT EXISTS weather_alt;

SET search_path TO weather_alt;

CREATE TYPE coords AS (
	lat FLOAT,
	lon FLOAT
);

CREATE TYPE sensor_type AS ENUM ('sun', 'shade');

CREATE TABLE IF NOT EXISTS weather_alt.sensors (
    id TEXT PRIMARY KEY,
    coords coords,
    type sensor_type,
    note TEXT,
    attached TEXT,
    install_date DATE
);

CREATE TABLE IF NOT EXISTS weather_alt.sensordata (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    humidity FLOAT,
    temperature FLOAT,
    sensor TEXT,
    FOREIGN KEY (sensor) REFERENCES weather_alt.sensors(id) ON DELETE CASCADE,
    CONSTRAINT sensor_time_id UNIQUE (time,sensor)
);
