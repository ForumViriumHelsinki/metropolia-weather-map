from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from api.database import get_session
from api.models import Sensor, SensorTag
from utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)

if TYPE_CHECKING:
    import pandas


def filter_df_by_tag(df: pandas.DataFrame, tag: str) -> pandas.DataFrame:
    """Filters out all sensors which do not have specified tag

    Args:
        df (pandas.DataFrame): Dataframe to filter
        tag (str): Tag used for filtering

    Returns:
        pandas.DataFrame: Dataframe that only has sensors with specified tag
    """
    for db in get_session():
        res = db.exec(
            select(Sensor.id)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
        ids = res.all()

    return df[df["dev-id"].isin(ids)]


def filter_location_with_tag(
    location: str,
    tag,
    get_2024=False,
    get_2025=False,
    daytime=False,
    nighttime=False,
) -> pandas.DataFrame:
    """Returns a dataframe of locations sensors that have the specified tag

    Args:
        location (str): Location of sensors
        tag (str): Tag to filter sensors with
        get_2024 (bool, optional): Fetches only 2024 data. Defaults to False.
        get_2025 (bool, optional): Fetches only 2025 data. Defaults to False.
        daytime (bool, optional): Use only data between sunrise and sundown. Defaults to False.
        nighttime (bool, optional): Use only data between sundown and sunrise. Defaults to False.

    Returns:
        pandas.DataFrame: Dataframe filtered with given options
    """
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
        )
        location_with_tag_ids = res.all()

    return df[df["dev-id"].isin(location_with_tag_ids)]


def tag_filter(df: pandas.DataFrame, tag: str) -> pandas.DataFrame:
    """Filters sensors which have the given tag

    Args:
        df (pandas.DataFrame): Dataframe to filter
        tag (str): Tag used for filtering

    Returns:
        pandas.DataFrame: Filtered dataframe
    """

    # Get sensors with the wanted tag
    for db in get_session():
        res = db.exec(
            select(SensorTag.sensor_id)
            .join(Sensor, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
        location_with_tag_ids = res.all()

    return df[df["dev-id"].isin(location_with_tag_ids)]
