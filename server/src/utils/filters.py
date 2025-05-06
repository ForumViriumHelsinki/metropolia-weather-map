from sqlmodel import select

from api.models import Sensor, SensorTag
from src.api.database import get_session
from utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)


def filter_df_by_tag(df, tag):
    for db in get_session():
        res = db.exec(
            select(Sensor.id)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
        ids = res.all()

    return df[df["dev-id"].isin(ids)]


def filter_location_with_tag(
    location,
    tag,
    get_2024=False,
    get_2025=False,
    daytime=False,
    nighttime=False,
):
    match location:
        case "Vallila":
            df = get_vallila(get_2024, get_2025, daytime, nighttime)
        case "Koivukyla":
            df = get_koivukyla(get_2024, get_2025, daytime, nighttime)
        case "Laajasalo":
            df = get_laajasalo(get_2024, get_2025, daytime, nighttime)
        case _:
            df = get_all_locations(get_2024, get_2025, daytime, nighttime)

    location_with_tag_ids = []
    for db in get_session():
        res = db.exec(
            select(SensorTag.sensor_id)
            .join(Sensor, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
            # .where(Sensor.location == location)
        )
        location_with_tag_ids = res.all()

    return df[df["dev-id"].isin(location_with_tag_ids)]
