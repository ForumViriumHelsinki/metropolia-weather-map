import os
import json
import csv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env.local"))


FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "sensors")
)


def write_to_csv(data):
    CSV_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "output", "sensors.csv")
    )
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["id", "coordinates", "type", "note", "attached", "install_date"]
        )
        writer.writerows(data)


def load_sensors():
    sensor_data = []
    for filename in os.listdir(FOLDER_PATH):
        FILE_PATH = os.path.join(FOLDER_PATH, filename)
        with open(FILE_PATH, encoding="utf-8") as geojson_file:
            data = json.load(geojson_file)
            coords = data["geometry"]["coordinates"]

            sensor_data.append(
                [
                    data["id"],
                    f"({coords[1]}, {coords[0]})",  # Format as (lat, lon)
                    data["properties"]["Tyyppi"],
                    data["properties"]["Huomiot"],
                    data["properties"]["Kiinnitystapa"],
                    data["properties"]["Asennettu_pvm"],
                ]
            )

    write_to_csv(sensor_data)


if __name__ == "__main__":
    load_sensors()
