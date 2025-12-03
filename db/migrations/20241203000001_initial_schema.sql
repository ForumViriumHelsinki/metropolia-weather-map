-- migrate:up

-- Create weather schema
CREATE SCHEMA IF NOT EXISTS weather;

-- Sensors table (created by SQLModel but we need migration for production)
CREATE TABLE IF NOT EXISTS weather.sensors (
    id VARCHAR NOT NULL,
    lon FLOAT NOT NULL,
    lat FLOAT NOT NULL,
    location VARCHAR NOT NULL,
    install_date DATE,
    csv_link VARCHAR,
    PRIMARY KEY (id)
);

-- Tags table
CREATE TABLE IF NOT EXISTS weather.tags (
    id VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

-- Sensor-Tags association table
CREATE TABLE IF NOT EXISTS weather.sensor_tags (
    sensor_id VARCHAR NOT NULL,
    tag_id VARCHAR NOT NULL,
    PRIMARY KEY (sensor_id, tag_id),
    FOREIGN KEY (sensor_id) REFERENCES weather.sensors(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES weather.tags(id) ON DELETE CASCADE
);

-- migrate:down

DROP TABLE IF EXISTS weather.sensor_tags;
DROP TABLE IF EXISTS weather.tags;
DROP TABLE IF EXISTS weather.sensors;
DROP SCHEMA IF EXISTS weather;
