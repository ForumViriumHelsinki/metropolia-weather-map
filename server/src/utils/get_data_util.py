from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import TYPE_CHECKING

import pandas as pd
from sqlmodel import select

from api.database import get_session
from api.models import Sensor

if TYPE_CHECKING:
    from datetime import date

    from sqlalchemy import Sequence

logger = logging.getLogger(__name__)


# Fetch and filter makelankatu data
def get_vallila(
    get_2024: bool = False,
    get_2025: bool = False,
    daytime: bool = False,
    nightime: bool = False,
) -> pd.DataFrame:
    """Fetch data of Mäkelänkatu sensors

    Args:
        get_2024 (bool, optional): Fetch only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetch only 2025 data. Defaults to False.
        daytime (bool, optional): Use only data between sunrise and sundown. Defaults to False.
        nightime (bool, optional): Use only data between sundown and sunrise. Defaults to False.

    Returns:
        pandas.DataFrame: Dataframe of location data with specified filters
    """
    df24 = None
    df25 = None

    if get_2024:
        logger.debug("Loading Vallila 2024")
        df24 = read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.parquet"
        )

    if get_2025:
        logger.debug("Loading Vallila 2025")
        df25 = read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2025.parquet"
        )

    if not get_2024 and not get_2025:
        logger.debug("Loading Vallila all years")
        df24 = read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.parquet"
        )
        df25 = read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2025.parquet"
        )

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
) -> pd.DataFrame:
    """Fetch data of Laajasalo sensors

    Args:
        get_2024 (bool, optional): Fetch only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetch only 2025 data. Defaults to False.
        daytime (bool, optional): Use only data between sunrise and sundown. Defaults to False.
        nightime (bool, optional): Use only data between sundown and sunrise. Defaults to False.

    Returns:
        pandas.DataFrame: Dataframe of location data with specified filters
    """
    if get_2024:
        logger.debug("Loading Laajasalo 2024")
        df = get_rest(get_2024=True)
    elif get_2025:
        logger.debug("Loading Laajasalo 2025")
        df = get_rest(get_2025=True)
    else:
        logger.debug("Loading Laajasalo all years")
        df = get_rest()

    df["location"] = "Laajasalo"
    df = filter_install_date(df, "Laajasalo")
    logger.debug("Laajasalo sensors: %s", df["dev-id"].unique())

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
) -> pd.DataFrame:
    """Fetch data of Koivukylä sensors

    Args:
        get_2024 (bool, optional): Fetch only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetch only 2025 data. Defaults to False.
        daytime (bool, optional): Use only data between sunrise and sundown. Defaults to False.
        nightime (bool, optional): Use only data between sundown and sunrise. Defaults to False.

    Returns:
        pandas.DataFrame: Dataframe of location data with specified filters
    """
    if get_2024:
        logger.debug("Loading Koivukylä 2024")
        df = get_rest(get_2024=True)
    elif get_2025:
        logger.debug("Loading Koivukylä 2025")
        df = get_rest(get_2025=True)
    else:
        logger.debug("Loading Koivukylä all years")
        df = get_rest()

    df["location"] = "Koivukyla"
    df = df.loc[df["location"] == "Koivukyla"]
    df = filter_install_date(df, "Koivukyla")
    logger.debug("Koivukylä sensors: %s", df["dev-id"].unique())

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
) -> pd.DataFrame:
    """Fetch data of all sensors

    Args:
        get_2024 (bool, optional): Fetch only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetch only 2025 data. Defaults to False.
        daytime (bool, optional): Use only data between sunrise and sundown. Defaults to False.
        nightime (bool, optional): Use only data between sundown and sunrise. Defaults to False.

    Returns:
        pandas.DataFrame: Dataframe of all locations data with specified filters
    """
    if get_2024:
        logger.info("Loading all 2024 data")
        dfV = get_vallila(get_2024=True)
        dfR = get_rest(get_2024=True)

    elif get_2025:
        logger.info("Loading all 2025 data")
        dfV = get_vallila(get_2025=True)
        dfR = get_rest(get_2025=True)
    else:
        logger.info("Loading all year data")
        dfV = get_vallila()
        dfR = get_rest()

    # filter_install_date returns boolean-indexed views, so we need .copy()
    # to safely add the location column without SettingWithCopyWarning.
    # Memory is freed when dfR is deleted before the final concat.
    dfK = filter_install_date(dfR, "Koivukyla").copy()
    dfK["location"] = "Koivukyla"

    dfL = filter_install_date(dfR, "Laajasalo").copy()
    dfL["location"] = "Laajasalo"

    # Delete dfR to free memory before concat
    del dfR

    df_merged = pd.concat([dfV, dfK, dfL])

    if daytime:
        return filter_daytime_data(df_merged)

    if nightime:
        return filter_daytime_data(df_merged, nightime=True)

    return df_merged


@lru_cache(maxsize=4)
def _fetch_parquet_cached(url: str) -> pd.DataFrame:
    """Fetch and cache parquet data from URL.

    Uses LRU cache to avoid re-downloading the same files.
    Cache size of 4 covers all parquet files used by the app.
    """
    logger.info("Fetching parquet from %s", url)
    return pd.read_parquet(url)


def read_and_clean_parquet(url: str) -> pd.DataFrame:
    """Fetches parquet data and sets time column to datetime

    Args:
        url (str): URL of the parquet file

    Returns:
        pandas.DataFrame: Dataframe of parquet data
    """
    # No .copy() needed - reset_index() returns a new DataFrame,
    # so modifications here don't affect the cached data
    df = _fetch_parquet_cached(url).rename_axis("time").reset_index()
    df["time"] = pd.to_datetime(df["time"])
    return df


def clear_parquet_cache() -> None:
    """Clear the parquet file cache. Useful for testing or memory management."""
    _fetch_parquet_cached.cache_clear()
    logger.info("Parquet cache cleared")


def filter_install_date(df: pd.DataFrame, location: str) -> pd.DataFrame:
    """Filters sensors by location and removes invalid data before install date.

    Uses vectorized operations instead of sensor-by-sensor filtering for
    better memory efficiency and performance.

    Args:
        df (pandas.DataFrame): Dataframe of fetched data from bri3
        location (str): Location of wanted sensors

    Returns:
        pandas.DataFrame: Dataframe which includes only sensors
        of the specified location with corrected install date
    """
    # Get ids and install dates from database
    for db in get_session():
        res = db.exec(
            select(Sensor.id, Sensor.install_date).where(
                Sensor.location == location
            )
        ).all()

    if not res:
        logger.warning("No sensors found for location: %s", location)
        return df.iloc[0:0]  # Return empty DataFrame with same columns

    # Create a mapping of sensor_id -> install_date for vectorized lookup
    # Localize to UTC to match parquet data timestamps
    sensor_dates = {
        sensor_id: pd.Timestamp(install_date).tz_localize("UTC")
        for sensor_id, install_date in res
    }
    sensor_ids = set(sensor_dates.keys())

    # Filter to only sensors in this location (single boolean mask)
    location_mask = df["dev-id"].isin(sensor_ids)
    df_location = df[location_mask]

    if df_location.empty:
        logger.warning("No data found for sensors in location: %s", location)
        return df_location

    # Map each row's sensor_id to its install_date, then compare with time
    # This is a vectorized operation - much faster than looping
    install_dates = df_location["dev-id"].map(sensor_dates)
    valid_mask = df_location["time"] >= install_dates

    return df_location[valid_mask]


def get_rest(
    get_2024: bool = False,
    get_2025: bool = False,
) -> pd.DataFrame:
    """Helper function to fetch Koivukylä and Laajasalo data

    Args:
        get_2024 (bool, optional): Fetch only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetch only 2025 data. Defaults to False.
    """

    def fetch_2024():
        return read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/r4c/r4c_all-2024.parquet"
        )

    def fetch_2025():
        return read_and_clean_parquet(
            "https://bri3.fvh.io/opendata/r4c/r4c_all-2025.parquet"
        )

    if get_2024:
        logger.debug("Loading R4C 2024")
        return fetch_2024()

    if get_2025:
        logger.debug("Loading R4C 2025")
        return fetch_2025()

    df24 = fetch_2024()
    df25 = fetch_2025()

    logger.debug("Loading R4C all years")
    return pd.concat([df24, df25])


def filter_date_range(
    df: pd.DataFrame, start_date: date, end_date: date
) -> pd.DataFrame:
    """Filters dataframe with the wanted date range

    Args:
        df (pandas.DataFrame): Dataframe to filter
        start_date (datetime.date): Start date of the range
        end_date (datetime.date): End date of the range

    Returns:
        pandas.DataFrame: Filtered DataFrame with the specified date range
    """
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


def filter_daytime_data(
    df: pd.DataFrame, nightime: bool = None
) -> pd.DataFrame:
    """Filters dataframe to only include data between sunrise and sundown or opposite

    Args:
        df (pandas.DataFrame): Dataframe to filter
        nightime (bool, optional): Returns nighttime data if True. Defaults to None.

    Returns:
        pandas.DataFrame: Filtered DataFrame
    """
    # daylight csv location
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "analysis", "daylight.csv"
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
    return daylight_df.drop("sunset", axis=1)


def get_ids_by_location(location: str) -> Sequence[str] | list:
    """Returns list of sensor ids in the specified location

    Args:
        location (str): Wanted location

    Returns:
        Sequence[str] | list: List of sensor ids in specified location
    """
    sensor_ids = []
    for db in get_session():
        res = db.exec(select(Sensor.id).where(Sensor.location == location))
        sensor_ids = res.all()

    return sensor_ids
