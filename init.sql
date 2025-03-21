CREATE DATABASE weatherdb;

\c weatherdb
CREATE SCHEMA IF NOT EXISTS weather;

SET search_path TO weather;

CREATE TABLE IF NOT EXISTS weather.sensors(
    id text PRIMARY KEY,
    coordinates point,
    location text,
    install_date date,
    csv_link text
);

CREATE TABLE IF NOT EXISTS weather.tags(
    id text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS weather.sensor_tags(
    sensor_id text REFERENCES weather.sensors(id) ON DELETE CASCADE,
    tag_id text REFERENCES weather.tags(id) ON DELETE CASCADE,
    PRIMARY KEY (sensor_id, tag_id)
);

