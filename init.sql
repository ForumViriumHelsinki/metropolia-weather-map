CREATE DATABASE weatherdb;

\c weatherdb
CREATE SCHEMA IF NOT EXISTS weather;

SET search_path TO weather;

CREATE TYPE note AS ENUM(
    'auringossa',
    'varjossa',
    'tiellä',
    'metsässä',
    'puussa',
    'julkisivulla',
    'maassa'
);

CREATE TABLE IF NOT EXISTS weather.sensors(
    id text PRIMARY KEY,
    coordinates point,
    location text,
    install_date date,
    csv_data text
);

CREATE TABLE IF NOT EXISTS weather.notes(
    id serial PRIMARY KEY,
    note note,
    sensor_id text REFERENCES weather.sensors(id)
);

