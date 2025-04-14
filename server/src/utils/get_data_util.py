import matplotlib.pyplot as plt
import pandas as pd
from sqlmodel import select
from src.api.database import get_session
from src.api.models import Sensor


# Fetch and filter makelankatu data
def get_vallila():
    df24 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz",
        parse_dates=["time"],
    )

    df25 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2025.csv.gz",
        parse_dates=["time"],
    )

    df = pd.concat([df24, df25])
    return df
    df = filter_install_date(df, "Vallila")

    return df


async def get_laajasalo():
    df = get_rest()

    # get Laajasalo sensors
    sensor_ids = await get_ids_by_location("Laajasalo")
    df = df[df["dev-id"].isin(sensor_ids)]

    df = await filter_install_date(df, "Laajasalo")

    return df


async def get_koivukyla():
    df = get_rest()

    # get Koivukylä sensors
    sensor_ids = await get_ids_by_location("Koivukylä")
    df = df[df["dev-id"].isin(sensor_ids)]

    df = await filter_install_date(df, "Koivukylä")

    return df


async def get_all_locations():
    dfM = await get_vallila()
    dfK = await get_koivukyla()
    dfL = await get_laajasalo()

    df_merged = pd.concat([dfM, dfK, dfL])

    return df_merged


def filter_install_date(df, location):
    sensor_install = dict()
    # Get ids and install dates
    for db in get_session():
        res = db.execute(
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


def get_ids_by_location(location: str):
    sensor_ids = []
    for db in get_session():
        res = db.exec(select(Sensor.id).where(Sensor.location == location))
        sensor_ids = res.scalars().all()

    return sensor_ids


def set_df_date_range(df, start_date, end_date):
    mask = (df["time"] >= start_date) & (end_date <= df["time"])
    return df[mask]
