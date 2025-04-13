import pandas as pd
from database import get_db
from models import Sensor, SensorTag
from sqlmodel import select

from .get_data_util import get_koivukyla, get_laajasalo, get_makelankatu

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


async def filter_df_by_tag(df, tag):
    print("filter_df_by_tag()")
    async for db in get_db():
        res = await db.execute(
            select(Sensor.id)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
        ids = res.scalars().all()

    print(ids)
    return df[df["dev-id"].isin(ids)]


async def filter_location_with_tag(location, tag):
    print("filter_location_with_tag()")

    match location:
        case "Koivukylä":
            df = await get_koivukyla()
        case "Mäkelänkatu":
            df = await get_makelankatu()
        case "Laajasalo":
            df = await get_laajasalo()
        case _:
            raise Exception("Invalid location")

    location_with_tag_ids = []
    async for db in get_db():
        res = await db.execute(
            select(SensorTag.sensor_id)
            .join(Sensor, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
            .where(Sensor.location == location)
        )
        location_with_tag_ids = res.scalars().all()

    print(location_with_tag_ids)

    df = df[df["dev-id"].isin(location_with_tag_ids)]
    return df
