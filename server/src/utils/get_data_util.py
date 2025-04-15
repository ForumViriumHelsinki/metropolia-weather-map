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
    df["location"] = "Vallila"
    df = filter_install_date(df, "Vallila")

    return df


def get_laajasalo():
    df = get_rest()

    # get Laajasalo sensors
    sensor_ids = get_ids_by_location("Laajasalo")
    df = df[df["dev-id"].isin(sensor_ids)]
    df["location"] = "Laajasalo"
    df = filter_install_date(df, "Laajasalo")

    return df


def get_koivukyla():
    df = get_rest()

    # get Koivukylä sensors
    sensor_ids = get_ids_by_location("Koivukylä")
    df = df[df["dev-id"].isin(sensor_ids)]
    df["location"] = "Koivukylä"
    df = filter_install_date(df, "Koivukylä")

    return df


def get_all_locations():
    dfV = get_vallila()
    dfK = get_koivukyla()
    dfL = get_laajasalo()
    df_merged = pd.concat([dfV, dfK, dfL])

    return df_merged


def filter_install_date(df, location):
    # Get ids and install dates
    for db in get_session():
        res = db.exec(
            select(Sensor.id, Sensor.install_date).where(Sensor.location == location)
        ).all()

    dfs = []
    for sensor_id, install_date in res:
        mask = df["time"] >= str(install_date)
        filtered_df = df[(df["dev-id"] == sensor_id) & mask]
        dfs.append(filtered_df)

    df = pd.concat(dfs)
    return df


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
        sensor_ids = res.all()

    return sensor_ids


def set_df_date_range(df, start_date, end_date):
    mask = (df["time"] >= start_date) & (end_date <= df["time"])
    return df[mask]
