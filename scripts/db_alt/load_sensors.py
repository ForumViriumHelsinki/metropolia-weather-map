import os
import json

from custom_types import Sensor
from tables import TypeEnum
from db import insert_sensor

FILE_PATH = "../makelankatu-2024.csv"
FOLDER_PATH = "../sensors"

with open(FILE_PATH, newline="") as csvfile:
    for filename in os.listdir(FOLDER_PATH):
        FILE_PATH = os.path.join(FOLDER_PATH, filename)

        with open(FILE_PATH, encoding="utf-8") as geojson_file:
            data = json.load(geojson_file)

            lat_lon = data["geometry"]["coordinates"][::-1]

            sensor_type = None
            if data["properties"]["Tyyppi"] == "Varjossa":
                sensor_type = TypeEnum.shade
            elif data["properties"]["Tyyppi"] == "Auringossa":
                sensor_type = TypeEnum.sun

            new_sensor = Sensor(
                id=data["id"],  # id
                coords=lat_lon,  # coords
                type=sensor_type,  # type
                note=data["properties"]["Huomiot"],  # note
                attached=data["properties"]["Kiinnitystapa"],  # attached
                install_date=data["properties"]["Asennettu_pvm"],  # install_date
            )

            insert_sensor(new_sensor)
