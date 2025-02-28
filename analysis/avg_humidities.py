import pandas as pd
import utils
from utils import SENSORS, SENSOR_SUN, SENSOR_SHADE
import matplotlib.pyplot as plt


start_date = "2024-07-1"
end_date = "2024-9-30"


# Calculate the average humidity for each day in the date range and calculate
# the mean humidity during the whole date range

df = utils.get_csv()
df = utils.apply_date_range(df, start_date, end_date)
sensors = utils.separate_sensors(df)


def avg_hum_per_day(sensor_df):
    sensor_df["date"] = sensor_df["time"].dt.date
    avg_hums = sensor_df.groupby("date")["humidity"].mean().reset_index()
    avg_hums["dev-id"] = sensor_df["dev-id"].iloc[0]

    if sensor_df["dev-id"].iloc[0] in SENSOR_SUN:
        avg_hums["type"] = "sun"
    else:
        avg_hums["type"] = "shade"

    return avg_hums


avg_hums = {
    sensor_id: avg_hum_per_day(sensor_df) for sensor_id, sensor_df in sensors.items()
}

df_merged = pd.concat(avg_hums, ignore_index=True)

sensor_avg_humidities = df_merged.groupby("dev-id")["humidity"].mean().reset_index()
sensor_avg_humidities.columns = ["dev-id", "avg_humidity"]


i = 0
for sensor_id in SENSOR_SUN:
    r_value = 1 - (i * 0.05)
    g_value = (i * 0.1) + 0.35
    b_value = i * 0.2

    sensor_data = df_merged[df_merged["dev-id"] == sensor_id]
    sensor_digits = sensor_id[-2:]
    label = f"Sun: {sensor_digits}"

    plt.plot(
        sensor_data["date"],
        sensor_data["humidity"],
        label=label,
        color=(r_value, g_value, b_value),
    )
    i = i + 1

    # Average humidity for sensor during the whole date range
    # avg_hum = sensor_data["humidity"].mean()

    # plt.axhline(
    #     y=avg_hum,
    #     color="orange",
    #     linestyle="--",
    #     label=f"Sun Avg Hum: {avg_hum:.2f}%",
    # )


i = 0
for sensor_id in SENSOR_SHADE:
    r_value = i * 0.05
    g_value = 1 - (i * 0.1)
    b_value = i * 0.1

    sensor_data = df_merged[df_merged["dev-id"] == sensor_id]
    sensor_digits = sensor_id[-2:]
    label = f"Shade: {sensor_digits}"
    plt.plot(
        sensor_data["date"],
        sensor_data["humidity"],
        label=label,
        color=(r_value, g_value, b_value),
    )
    i = i + 1

    # Average humidity for sensor during the whole date range
    # avg_hum = sensor_data["humidity"].mean()

    # plt.axhline(
    #     y=avg_hum,
    #     color="green",
    #     linestyle="--",
    #     label=f"Sun Avg Hum: {avg_hum:.2f}%",
    # )

sun_avg_hum = df_merged[df_merged["type"] == "sun"]["humidity"].mean()
shade_avg_hum = df_merged[df_merged["type"] == "shade"]["humidity"].mean()


plt.axhline(
    y=sun_avg_hum,
    color="purple",
    linestyle="--",
    label=f"Sun Avg Hum: {sun_avg_hum:.2f}%",
)
plt.axhline(
    y=shade_avg_hum,
    color="aquamarine",
    linestyle="--",
    label=f"Shade Avg Hum: {shade_avg_hum:.2f}%",
)


plt.xlabel("Date")
plt.ylabel("Avg humidity")
plt.title("Average Humidity per Day for Each Sensor")
plt.legend(title="Sensor Location")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
