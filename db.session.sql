INSERT INTO weather.sensors(id, coordinates, location, install_date, csv_data)
  VALUES ('6614', point(64, 25), 'Laajasalo', '2025-03-12', 'http://demo.test');

INSERT INTO weather.notes(note, sensor_id)
  VALUES ('auringossa', '6614');

INSERT INTO weather.notes(note, sensor_id)
  VALUES ('maassa', '6614');

SELECT
  sensors.id,
  location,
  note
FROM
  weather.sensors
  JOIN weather.notes ON sensors.id = sensor_id;

SELECT
  *
FROM
  weather.sensors;

SELECT
  note
FROM
  weather.notes
WHERE
  sensor_id = '6614';

