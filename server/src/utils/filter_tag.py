import pandas as pd
from sqlmodel import select
from src.api.database import get_session
from src.api.models import Sensor, SensorTag

from .get_data_util import get_by_location

# Get ids with the specified tag
# async def sensors_with_tag(tag):
#     print("sensors_with_tag()")
#     sensor_with_tag_id = []
#     async for db in get_db():
#         result = await db.execute(
#             select(Sensor.id)
#             .join(SensorTag, Sensor.id == SensorTag.sensor_id)
#             .where(SensorTag.tag_id == tag)
#         )
#         sensor_with_tag_id = result.scalars().all()
#     return sensor_with_tag_id


def filter_df_by_tag(df, tag):
    print("filter_df_by_tag()")
    for db in get_session():
        res = db.exec(
            select(Sensor.id)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
        ids = res.all()

    print(ids)
    return df[df["dev-id"].isin(ids)]


def filter_location_with_tag(location, tag, get_2024, get_2025, daytime, nighttime):
    print("filter_location_with_tag()")

    df = get_by_location(location, get_2024, get_2025, daytime, nighttime)

    location_with_tag_ids = []
    for db in get_session():
        res = db.exec(
            select(SensorTag.sensor_id)
            .join(Sensor, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
            .where(Sensor.location == location)
        )
        location_with_tag_ids = res.all()

    print(location_with_tag_ids)

    df = df[df["dev-id"].isin(location_with_tag_ids)]
    return df
