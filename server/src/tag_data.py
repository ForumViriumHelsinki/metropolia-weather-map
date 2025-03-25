import asyncio
import requests
import pandas as pd

from sqlmodel import select

from database import get_db
from models import Sensor, SensorTag
from sqlalchemy.ext.asyncio import AsyncSession
import matplotlib.pyplot as plt



def filter_daytime_data(df):
    # Sunrise and sunset data
    daylight_info = pd.read_csv("../data/daylight.csv", parse_dates=["sunrise", "sunset"])

    df['date'] = df['time'].dt.date 
    daylight_info['date'] = daylight_info['sunrise'].dt.date
    df = pd.merge(df, daylight_info, on='date', how="left")

    mask = (df["time"] >= df["sunrise"]) & (df["time"] <= df["sunset"])
    filtered_df = df[mask]
    return filtered_df

def create_graph(df, sensor_ids):
    plt.figure(figsize=(12, 8))  # Create a single figure
    grouped = df.groupby("dev-id")
    for sensor_id, group in grouped:
        if sensor_id in sensor_ids:
            plt.plot(group["time"], group["temperature"], label=f"Sensor {sensor_id}")
    
    # Add labels, title, legend, and grid to the single figure
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Sensor Data for All Sensor IDs")
    plt.legend()
    plt.grid(True)
    
    # Save the single figure
    plt.savefig("all_sensors.png")
    plt.close()

async def tag_data(tag="viheralue"):
    sensors = []
    async for db in get_db():
        if isinstance(db, AsyncSession):
            # Simplified query to match the provided SQL
            result = await db.execute(
                select(Sensor)
                .join(SensorTag, Sensor.id == SensorTag.sensor_id)
                .where(SensorTag.tag_id == tag)
            )
            sensors = result.scalars().all()

    sensor_ids = [i.id for i in sensors]

    # Mäkelänkatu
    dfM = pd.read_csv("https://bri3.fvh.io/opendata/makelankatu/makelankatu-2024.csv.gz", parse_dates=["time"])
    # Laajasalo & Koivukylä
    dfLK = pd.read_csv("https://bri3.fvh.io/opendata/r4c/r4c_all-2024.csv.gz", parse_dates=["time"])

    df = pd.concat([dfM, dfLK], ignore_index=True)
    
    df = filter_daytime_data(df)
    print(df.head())
    
    create_graph(df, sensor_ids)


if __name__ == "__main__":
    asyncio.run(tag_data())

