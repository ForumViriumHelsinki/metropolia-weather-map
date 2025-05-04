import os
from datetime import date

import pandas as pd
from sqlmodel import select
from src.api.database import get_session
from src.api.models import Sensor


def get_by_location(
    location: str = None,
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nighttime: bool = False,
):

    match location:
        case "Vallila":
            return get_vallila(get_2024, get_2025, daytime, nighttime)
        case "Koivukyla":
            return get_koivukyla(get_2024, get_2025, daytime, nighttime)
        case "Laajasalo":
            return get_laajasalo(get_2024, get_2025, daytime, nighttime)
        case _:
            return get_all_locations(get_2024, get_2025, daytime, nighttime)

    return


# Fetch and filter makelankatu data
def get_vallila(
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nightime: bool = False,
):
    df24 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz",
        parse_dates=["time"],
    )
    if get_2024:
        return df24

    df25 = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2025.csv.gz",
        parse_dates=["time"],
    )
    if get_2025:
        return df25

    df = pd.concat([df24, df25])
    df["location"] = "Vallila"
    df = filter_install_date(df, "Vallila")

    if daytime:
        return filter_daytime_data(df)

    if nightime:
        return filter_daytime_data(df, nightime=True)

    return df


def get_laajasalo(
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nightime: bool = False,
):
    if get_2024:
        df = get_rest(get_2024=True)
    elif get_2025:
        df = get_rest(get_2025=True)
    else:
        df = get_rest()

    # get Laajasalo sensors
    df["location"] = "Laajasalo"
    df = df.loc[df["location"] == "Laajasalo"]
    df = filter_install_date(df, "Laajasalo")

    if daytime:
        return filter_daytime_data(df)

    if nightime:
        return filter_daytime_data(df, nightime=True)

    return df


def get_koivukyla(
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nightime: bool = False,
):
    if get_2024:
        df = get_rest(get_2024=True)
    elif get_2025:
        df = get_rest(get_2025=True)
    else:
        df = get_rest()

    df["location"] = "Koivukyla"
    df = df.loc[df["location"] == "Koivukyla"]
    df = filter_install_date(df, "Koivukyla")

    if daytime:
        return filter_daytime_data(df)

    if nightime:
        return filter_daytime_data(df, nightime=True)

    return df


def get_all_locations(
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nightime: bool = False,
):
    if get_2024:
        dfV = get_vallila(get_2024=True)
        dfK = get_koivukyla(get_2024=True)
        dfL = get_laajasalo(get_2024=True)
    elif get_2025:
        dfV = get_vallila(get_2025=True)
        dfK = get_koivukyla(get_2025=True)
        dfL = get_laajasalo(get_2025=True)
    else:
        dfV = get_vallila()
        dfK = get_koivukyla()
        dfL = get_laajasalo()

    df_merged = pd.concat([dfV, dfK, dfL])

    if daytime:
        return filter_daytime_data(df_merged)

    if nightime:
        return filter_daytime_data(df_merged, nightime=True)

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


def get_rest(
    get_2024: bool = False,
    get_2025: bool = False,
):
    df24 = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2024.csv.gz", parse_dates=["time"]
    )
    if get_2024:
        return df24

    df25 = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2025.csv.gz", parse_dates=["time"]
    )
    if get_2025:
        return df25

    df = pd.concat([df24, df25])

    return df


def filter_date_range(df, start_date, end_date):
    if start_date:
        start_date = pd.to_datetime(start_date).tz_localize("UTC")
    if end_date:
        end_date = pd.to_datetime(end_date).tz_localize("UTC")

    if start_date and end_date:
        mask = (df["time"] >= start_date) & (df["time"] <= end_date)
    elif start_date:
        mask = df["time"] >= start_date
    elif end_date:
        mask = df["time"] <= end_date
    else:
        return df

    return df[mask]


def filter_daytime_data(df, nightime: bool = None):
    # daylight csv location
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "data", "daylight.csv"
    )

    # Sunrise and sunset data
    daylight_info = pd.read_csv(csv_path, parse_dates=["sunrise", "sunset"])

    # Add date column to dataframae and daylight_info
    df["date"] = df["time"].dt.date
    daylight_info["date"] = daylight_info["sunrise"].dt.date

    # Merge dataframes on date
    df = pd.merge(df, daylight_info, on="date", how="left")

    # Create mask from the dates and filter the times
    mask = (df["time"] >= df["sunrise"]) & (df["time"] <= df["sunset"])

    # Apply the mask to filter out timestamps after sunset

    if nightime:
        daylight_df = df[~mask]
    else:
        daylight_df = df[mask]

    daylight_df = daylight_df.drop("sunrise", axis=1)
    daylight_df = daylight_df.drop("sunset", axis=1)

    return daylight_df


def get_ids_by_location(location: str):
    sensor_ids = []
    for db in get_session():
        res = db.exec(select(Sensor.id).where(Sensor.location == location))
        sensor_ids = res.all()

    return sensor_ids
