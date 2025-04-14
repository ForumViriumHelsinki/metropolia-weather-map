import os
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import utils

# from database import get_db
from models import get_sensors

# from utils import filter_daytime_data


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


def tag_data(tag="harmaa-alue"):
    sensors = []
    test = get_sensors()
    print(test)

    return

    # Query database for sensors with the specified tag
    # async for db in get_db():
    #     if isinstance(db, AsyncSession):
    #         result = await db.execute(
    #             select(Sensor)
    #             .join(SensorTag, Sensor.id == SensorTag.sensor_id)
    #             .where(SensorTag.tag_id == tag)
    #         )
    #         sensors = result.scalars().all()

    # Group sensors by location
    location_sensors = group_by_location(sensors)

    # Fetch data for sensors
    # Mäkelänkatu
    dfM = utils.get_makelankatu()
    dfLK = utils.get_rest()

    # Merge all the datasets
    df = pd.concat([dfM, dfLK], ignore_index=True)

    # Get data from only daytime
    df = utils.filter_daytime_data(df)

    # Create the graph
    create_graph(df, location_sensors)
    return


if __name__ == "__main__":
    tag_data()
