import io

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.get_data_util import get_vallila
from utils.filters import filter_df_by_tag


def compute_tempdeltas(sensor_data, resample_period):
    """
    Computes the average temperature change for a given set of sensors,
    resampled to the specified time period ('h' for hourly, 'D' for daily).
    """
    temperature_deltas = []

    for sensor_id, df in sensor_data.items():
        df = df[["time", "temperature"]].copy()
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values(by="time")
        df["temperature_change"] = df["temperature"].diff()

        # Resample to specified time period (hourly or daily)
        df.set_index("time", inplace=True)
        df_resampled = (
            df[["temperature_change"]].resample(resample_period).mean()
        )
        temperature_deltas.append(df_resampled)

    if not temperature_deltas:
        return None

    # Merge all sensor data and compute the average humidity change
    return pd.concat(temperature_deltas).groupby("time").mean()


def group_data(data):
    """
    groups data by 'dev-id'
    """
    return {sensor_id: group for sensor_id, group in data.groupby("dev-id")}


def main():
    """
    Main function to compute and plot temperature changes for sun and shade sensors.
    """
    # buffer for data stream
    buf = io.BytesIO()
    # Get Vallila data
    data = get_vallila()

    # Filter data using existing functions
    data_sun = group_data(filter_df_by_tag(data, "aurinko"))
    data_shade = group_data(filter_df_by_tag(data, "varjo"))

    # Compute hourly and daily temperature changes for sun and shade sensors
    sun_tempdelta_hourly = compute_tempdeltas(data_sun, "h")
    shade_tempdelta_hourly = compute_tempdeltas(data_shade, "h")

    compute_tempdeltas(data_sun, "D")
    compute_tempdeltas(data_shade, "D")

    # Ensure both datasets have the same time range (inner join)
    if sun_tempdelta_hourly is not None and shade_tempdelta_hourly is not None:
        combined_delta_hourly = sun_tempdelta_hourly.join(
            shade_tempdelta_hourly,
            lsuffix="_sun",
            rsuffix="_shade",
            how="inner",
        )

        # Plot hourly temperature changes for sun and shade sensors
        plt.figure(figsize=(12, 6))
        plt.plot(
            combined_delta_hourly.index,
            combined_delta_hourly["temperature_change_sun"],
            label="Auringossa olevat sensorit (tunnittainen)",
            color="orange",
        )
        plt.plot(
            combined_delta_hourly.index,
            combined_delta_hourly["temperature_change_shade"],
            label="Varjossa olevat sensorit (tunnittainen)",
            color="blue",
        )
        plt.axhline(y=0, color="black", linestyle="--", linewidth=0.8)
        plt.xlabel("Aika")
        plt.ylabel("Keskiarvo lämpotilan muutos(°C)")
        plt.title("Keskiarvo lämpotilan muutos (°C) (Auringossa vs Varjossa)")
        plt.legend()
        plt.grid()

        # Save the plot to a buffer
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

    else:
        print("Not enough data to compute temperature changes.")
    """
    # Plot daily temperature changes for sun and shade sensors
    if sun_tempdelta_daily is not None and shade_tempdelta_daily is not None:

        combined_delta_daily = sun_tempdelta_daily.join(shade_tempdelta_daily, lsuffix='_sun', rsuffix='_shade', how='inner')

        # Plot daily temperature changes for sun and shade sensors
        plt.figure(figsize=(12, 6))
        plt.plot(combined_delta_daily.index, combined_delta_daily['temperature_change_sun'], label="Sun Sensors (Daily)", color='orange')
        plt.plot(combined_delta_daily.index, combined_delta_daily['temperature_change_shade'], label="Shade Sensors (Daily)", color='blue')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel('Time')
        plt.ylabel('Avg Daily Temperature Change (°C)')
        plt.title('Daily Average Temperature Change (Sun vs Shade)')
        plt.legend()
        plt.grid()
        plt.show()
    """
    # return the buffer, typically used for sending the image in a web response
    return buf


if __name__ == "__main__":
    main()
