import matplotlib.pyplot as plt
import pandas as pd
from database import get_db
from models import Sensor
from sqlmodel import select


# Fetch and filter makelankatu data
async def get_vallila():
    df24 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz",
        parse_dates=["time"],
    )
    df25 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2025.csv.gz",
        parse_dates=["time"],
    )
    df = pd.concat([df24, df25])
    df["location"] = "Vallila"
    df = await filter_install_date(df, "Vallila")

    return df


async def get_laajasalo():
    df = get_rest()

    # get Laajasalo sensors
    sensor_ids = await get_ids_by_location("Laajasalo")
    df = df[df["dev-id"].isin(sensor_ids)]
    df["location"] = "Laajasalo"
    df = await filter_install_date(df, "Laajasalo")

    return df


async def get_koivukyla():
    df = get_rest()

    # get Koivukylä sensors
    sensor_ids = await get_ids_by_location("Koivukylä")
    df = df[df["dev-id"].isin(sensor_ids)]
    df["location"] = "Koivukylä"
    df = await filter_install_date(df, "Koivukylä")

    return df


async def get_all_locations():
    dfV = await get_vallila()
    dfK = await get_koivukyla()
    dfL = await get_laajasalo()
    df_merged = pd.concat([dfV, dfK, dfL])

    return df_merged


async def filter_install_date(df, location):
    sensor_install = dict()
    # Get ids and install dates
    async for db in get_db():
        res = await db.execute(
            select(Sensor.id, Sensor.install_date).where(Sensor.location == location)
        )
        for sensor_id, install_date in res:
            sensor_install[sensor_id] = install_date

    # Mask all sensors by the install_date
    dfs = [
        item.loc[item["time"] >= str(sensor_install[sensor])]
        for sensor in sensor_install
        if (item := df.loc[df["dev-id"] == sensor]).shape[0] > 0
    ]

    # Merge all dataframes back into one
    merged_df = pd.concat(dfs, ignore_index=True)

    return merged_df


def get_rest():
    df24 = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2024.csv.gz", parse_dates=["time"]
    )
    df25 = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2025.csv.gz", parse_dates=["time"]
    )
    df = pd.concat([df24, df25])
    
    return df


async def get_ids_by_location(location: str):
    sensor_ids = []
    async for db in get_db():
        res = await db.execute(select(Sensor.id).where(Sensor.location == location))
        sensor_ids = res.scalars().all()

    return sensor_ids
