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

INSERT INTO weather.sensors(id, coordinates, location, install_date, csv_link)
    VALUES ('24E124136E106616', '(24.953944343215543, 60.19628790558516)', 'makelankatu', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106616.geojson'),
('24E124136E106617', '(24.949683705063027, 60.19858337673502)', 'makelankatu', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106617.geojson'),
('24E124136E106618', '(24.95214986305944, 60.19603679151048)', 'makelankatu', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106618.geojson'),
('24E124136E106619', '(24.954472833953627, 60.19597458443258)', 'makelankatu', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106619.geojson'),
('24E124136E106635', '(24.95465791769169, 60.19665805740335)', 'makelankatu', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106635.geojson'),
('24E124136E106636', '(24.947575305714295, 60.197169753763504)', 'makelankatu', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106636.geojson'),
('24E124136E106637', '(24.94848480567734, 60.19845337489223)', 'makelankatu', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106637.geojson'),
('24E124136E106638', '(24.952021110782997, 60.19691015749769)', 'makelankatu', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106638.geojson'),
('24E124136E106643', '(24.95440486752224, 60.19778118227482)', 'makelankatu', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106643.geojson'),
('24E124136E106661', '(24.95566158371556, 60.19641839065333)', 'makelankatu', '2024-06-16', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106661.geojson'),
('24E124136E106674', '(24.949697722407258, 60.19760495885829)', 'makelankatu', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106674.geojson'),
('24E124136E106686', '(24.954281110891024, 60.19476461138742)', 'makelankatu', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/24E124136E106686.geojson');

INSERT INTO weather.sensors(id, coordinates, location, install_date, csv_link)
    VALUES ('23E124136E106616', '(60.19628790558516, 24.953944343215543)', 'Varjossa', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106616.geojson'),
('23E124136E106617', '(60.19858337673502, 24.949683705063027)', 'Varjossa', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106617.geojson'),
('23E124136E106618', '(60.19603679151048, 24.95214986305944)', 'Varjossa', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106618.geojson'),
('23E124136E106619', '(60.19597458443258, 24.954472833953627)', 'Auringossa', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106619.geojson'),
('23E124136E106635', '(60.19665805740335, 24.95465791769169)', 'Varjossa', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106635.geojson'),
('23E124136E106636', '(60.197169753763504, 24.947575305714295)', 'Varjossa', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106636.geojson'),
('23E124136E106637', '(60.19845337489223, 24.94848480567734)', 'Auringossa', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106637.geojson'),
('23E124136E106638', '(60.19691015749769, 24.952021110782997)', 'Auringossa', '2024-06-14', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106638.geojson'),
('23E124136E106643', '(60.19778118227482, 24.95440486752224)', 'Varjossa', '2024-05-27', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106643.geojson'),
('23E124136E106661', '(60.19641839065333, 24.95566158371556)', 'Auringossa', '2024-06-16', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106661.geojson'),
('23E124136E106674', '(60.19760495885829, 24.949697722407258)', 'Varjossa', '2024-05-30', 'https://bri3.fvh.io/opendata/makelankatu/23E124136E106674.geojson');

