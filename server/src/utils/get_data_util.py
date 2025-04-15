import matplotlib.pyplot as plt
import pandas as pd
from sqlmodel import select
from src.api.database import get_session
from src.api.models import Sensor


# Fetch and filter makelankatu data
def get_vallila(get_2024: bool = None, get_2025: bool = None):

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

    return df


def get_laajasalo(get_2024: bool = None, get_2025: bool = None):
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

    return df


def get_koivukyla(get_2024: bool = None, get_2025: bool = None):
    if get_2024:
        df = get_rest(get_2024=True)
    elif get_2025:
        df = get_rest(get_2025=True)
    else:
        df = get_rest()

    df["location"] = "Koivukylä"
    df = df.loc[df["location"] == "Koivukylä"]
    df = filter_install_date(df, "Koivukylä")

    return df


def get_all_locations(get_2024: bool = None, get_2025: bool = None):
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


def get_rest(get_2024: bool = None, get_2025: bool = None):
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


def set_df_date_range(df, start_date, end_date):
    mask = (df["time"] >= start_date) & (end_date <= df["time"])
    return df[mask]
