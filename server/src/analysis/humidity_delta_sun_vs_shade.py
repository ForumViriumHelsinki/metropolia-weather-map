import io

import matplotlib.pyplot as plt
import pandas as pd

from utils.filters import filter_df_by_tag
from utils.get_data_util import get_vallila

"""
Sensors in sun and shade are currently hardcoded in the utils.py file.
"""
"""
def filter_sundata(data):
    data_sun = {sensor_id: data[sensor_id] for sensor_id in SENSOR_SUN if sensor_id in data}
    return data_sun

def filter_shadedata(data):
    data_shade = {sensor_id: data[sensor_id] for sensor_id in SENSOR_SHADE if sensor_id in data}
    return data_shade

def ask_user_for_year():
    year = input("Enter year for source data or 'all' for all available: ")
    try:
        year = int(year)
    except ValueError:
        if(year == "" or year == "all"):
            return None
        print("Please enter a valid year.")
        return ask_user_for_year()
    return year
"""


def compute_humidity_change(sensor_data, resample_period):
    """
    Computes the average humidity change for a given set of sensors,
    resampled to the specified time period ('H' for hourly, 'D' for daily).
    """
    humidity_deltas = []

    for sensor_id, df in sensor_data.items():
        df = df[["time", "humidity"]].copy()
        df["time"] = pd.to_datetime(df["time"])  # Ensure datetime format
        df = df.sort_values(by="time")  # Sort by time
        df["humidity_change"] = df["humidity"].diff()  # Compute change

        # Resample to specified time period (hourly or daily)
        df.set_index("time", inplace=True)
        df_resampled = df[["humidity_change"]].resample(resample_period).mean()
        humidity_deltas.append(df_resampled)

    if not humidity_deltas:
        return None

    # Merge all sensor data and compute the average humidity change
    return pd.concat(humidity_deltas).groupby("time").mean()


def group_data(data):
    """
    groups data by 'dev-id'
    """
    return {sensor_id: group for sensor_id, group in data.groupby("dev-id")}


def main():
    """
    Main function to compute and plot humidity changes for sun and shade sensors.
    """
    buf = io.BytesIO()
    data = get_vallila()

    data_sun = group_data(filter_df_by_tag(data, "aurinko"))
    data_shade = group_data(filter_df_by_tag(data, "varjo"))

    # Compute hourly and daily humidity changes
    sun_humidity_change_hourly = compute_humidity_change(data_sun, "h")
    shade_humidity_change_hourly = compute_humidity_change(data_shade, "h")

    compute_humidity_change(data_sun, "D")
    compute_humidity_change(data_shade, "D")

    # Ensure both datasets have the same time range (inner join)
    if (
        sun_humidity_change_hourly is not None
        and shade_humidity_change_hourly is not None
    ):
        combined_hourly = sun_humidity_change_hourly.join(
            shade_humidity_change_hourly,
            lsuffix="_sun",
            rsuffix="_shade",
            how="inner",
        )

        # Plot hourly humidity change
        plt.figure(figsize=(12, 6))
        plt.plot(
            combined_hourly.index,
            combined_hourly["humidity_change_sun"],
            label="Auringossa olevat sensorit (tunnittainen)",
            color="orange",
        )
        plt.plot(
            combined_hourly.index,
            combined_hourly["humidity_change_shade"],
            label="Varjossa olevat sensorit (tunnittainen)",
            color="blue",
        )
        plt.axhline(y=0, color="black", linestyle="--", linewidth=0.8)
        plt.xlabel("Time")
        plt.ylabel("Keskiarvo kosteuden muutos (Δ%)")
        plt.title("Keskiarvo kosteuden muutos (Auringossa vs Varjossa)")
        plt.legend()
        plt.grid()
        # plt.show()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

    else:
        print("Not enough data to compute daily humidity changes.")

    """
    ## Plot daily humidity change
    if sun_humidity_change_daily is not None and shade_humidity_change_daily is not None:
        combined_daily = sun_humidity_change_daily.join(shade_humidity_change_daily, lsuffix='_sun', rsuffix='_shade', how='inner')

        # Plot daily humidity change
        plt.figure(figsize=(12, 6))
        plt.plot(combined_daily.index, combined_daily['humidity_change_sun'], label="Sun Sensors (Daily)", color='darkorange')
        plt.plot(combined_daily.index, combined_daily['humidity_change_shade'], label="Shade Sensors (Daily)", color='darkblue')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel("Time")
        plt.ylabel("Avg Daily Humidity Change (Δ Humidity)")
        plt.title("Daily Average Humidity Change (Sun vs Shade)")
        plt.legend()
        plt.grid()
        #plt.show()
        plt.savefig(buf2, format='png')
        plt.close()
        buf2.seek(0)
    """

    # return the buffer, typically used for sending the image in a web response
    return buf


if __name__ == "__main__":
    main()
