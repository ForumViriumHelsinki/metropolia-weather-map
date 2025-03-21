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
    VALUES ('24E124136E140271', '(25.038138954219203, 60.17019884666942)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E140271.geojson'),
('24E124136E140283', '(25.08559466020529, 60.31902912814716)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E140283.geojson'),
('24E124136E140287', '(25.033164118825763, 60.17820925308568)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E140287.geojson'),
('24E124136E146069', '(25.05280813096903, 60.32773642005459)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146069.geojson'),
('24E124136E146080', '(25.034850310632546, 60.32798317371719)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146080.geojson'),
('24E124136E146083', '(25.040422169662946, 60.3242806019864)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146083.geojson'),
('24E124136E146087', '(25.06572, 60.32294)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146087.geojson'),
('24E124136E146118', '(25.076084591672647, 60.32569598999893)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146118.geojson'),
('24E124136E146126', '(25.0811313318558, 60.16635041344928)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146126.geojson'),
('24E124136E146128', '(25.05953654541, 60.31962470187571)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146128.geojson'),
('24E124136E146155', '(25.056895458613138, 60.32381237386444)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146155.geojson'),
('24E124136E146157', '(25.050955366758195, 60.18089723029303)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146157.geojson'),
('24E124136E146167', '(25.01943622180639, 60.167472595257465)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146167.geojson'),
('24E124136E146186', '(25.03355598732001, 60.17338413916632)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146186.geojson'),
('24E124136E146190', '(25.058774546806518, 60.33326243702411)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146190.geojson'),
('24E124136E146198', '(25.089740958221043, 60.16370815865264)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146198.geojson'),
('24E124136E146218', '(25.071710650381757, 60.32108766558408)', 'Koivukylä', '2024-06-26', 'https://bri3.fvh.io/opendata/r4c/24E124136E146218.geojson'),
('24E124136E146224', '(25.051803506562962, 60.16760355134523)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146224.geojson'),
('24E124136E146235', '(25.054461721547142, 60.17791332910831)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146235.geojson'),
('24E124136E146237', '(25.068313113651286, 60.16354863794643)', 'Laajasalo', '2024-06-25', 'https://bri3.fvh.io/opendata/r4c/24E124136E146237.geojson');

