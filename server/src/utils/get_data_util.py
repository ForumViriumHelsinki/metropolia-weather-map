import pandas as pd
from database import get_db
from models import Sensor
from sqlmodel import select


def get_makelankatu():
    df = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz",
        parse_dates=["time"],
    )

    return df


async def get_laajasalo():
    df = get_rest()

    # get Laajasalo sensors
    sensor_ids = await get_ids_by_location("Laajasalo")
    df = df[df["dev-id"].isin(sensor_ids)]

    return df


async def get_koivukyla():
    df = get_rest()

    # get Koivukylä sensors
    sensor_ids = await get_ids_by_location("Koivukylä")
    print(len(sensor_ids))
    df = df[df["dev-id"].isin(sensor_ids)]

    return df


def get_rest():
    df = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2024.csv.gz", parse_dates=["time"]
    )

    return df


async def get_ids_by_location(location: str):
    sensor_ids = []
    async for db in get_db():
        res = await db.execute(select(Sensor.id).where(Sensor.location == location))
        sensor_ids = res.scalars().all()

    return sensor_ids
