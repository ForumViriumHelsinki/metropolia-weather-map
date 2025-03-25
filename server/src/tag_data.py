import asyncio
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
from database import get_db
from models import Sensor, SensorTag
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


def filter_daytime_data(df):
    # daylight csv location
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "daylight.csv"
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
    daylight_df = df[mask]
    return daylight_df


def group_by_location(sensors):
    grouped_sensor_ids = defaultdict(list)
    for sensor in sensors:
        grouped_sensor_ids[sensor.location].append(sensor.id)

    return grouped_sensor_ids


def create_graph(df, location_sensors):
    plt.figure(figsize=(12, 8))

    # Draw a line from each sensor set
    for key in location_sensors:
        location_df = df[df["dev-id"].isin(location_sensors[key])]

        # The data that will be used for the line
        daily_avg_temp = location_df.groupby("date")["temperature"].mean()

        plt.plot(
            daily_avg_temp.index,
            daily_avg_temp.values,
            linestyle="-",
            label=f"Location: {key}",
        )

    # Show the graph
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Daily Average Temperatures per Location")
    plt.legend()
    plt.grid(True)
    # Save the graph
    abs_path = os.path.dirname(
        os.path.abspath(__file__)
    )  # Figures out the absolute path for you in case your working directory moves around.

    plt.savefig(abs_path + "/graphs/tag_test.svg", format="svg")
    plt.show()


async def tag_data(tag="harmaa-alue"):
    sensors = []

    # Query database for sensors with the specified tag
    async for db in get_db():
        if isinstance(db, AsyncSession):
            result = await db.execute(
                select(Sensor)
                .join(SensorTag, Sensor.id == SensorTag.sensor_id)
                .where(SensorTag.tag_id == tag)
            )
            sensors = result.scalars().all()

    # Group sensors by location
    location_sensors = group_by_location(sensors)

    # Fetch data for sensors
    # Mäkelänkatu
    dfM = pd.read_csv(
        "https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz",
        parse_dates=["time"],
    )
    # # Laajasalo & Koivukylä
    dfLK = pd.read_csv(
        "https://bri3.fvh.io/opendata/r4c/r4c_all-2024.csv.gz", parse_dates=["time"]
    )

    # Merge all the datasets
    df = pd.concat([dfM, dfLK], ignore_index=True)

    # Get data from only daytime
    df = filter_daytime_data(df)

    # Create the graph
    create_graph(df, location_sensors)
    return


if __name__ == "__main__":
    asyncio.run(tag_data())
