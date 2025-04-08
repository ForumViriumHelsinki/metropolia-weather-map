import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

startTime = datetime.now()

SENSOR_IDS = [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106619",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106643",
    "24E124136E106661",
    "24E124136E106674",
    "24E124136E106686",
]

SENSOR_SUN = [
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106619",
    "24E124136E106661",
]

SENSOR_SHADE = [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106643",
    "24E124136E106674",
    "24E124136E106686",
]

DATE_RANGE = {"start_date": "2024-07-1", "end_date": "2024-9-30"}

# This script gets the max temperature from each day between the dates in DATE_RANGE.
# Mean temperatures from sensors in the sun and shade are calculated separately.
# Max temperatures are plotted by "dev-id" and mean temperatures are overlaid on the graph

df = pd.read_csv("../../data/makelankatu-2024.csv")

df["time"] = pd.to_datetime(df["time"])

# Mask to get dates between the range
mask = (df["time"] >= DATE_RANGE["start_date"]) & (df["time"] <= DATE_RANGE["end_date"])

# Filter the dataframe with the mask
filtered_df = df.loc[mask]

# Group by 'dev-id' and create a dictionary of dataframes
sensors = {
    sensor_id: group
    for sensor_id, group in filtered_df.groupby("dev-id")
    if sensor_id in SENSOR_IDS
}


# Get max temp from each day
def max_temp_per_day(sensor_df):
    sensor_df["date"] = sensor_df["time"].dt.date
    max_temps = sensor_df.groupby("date")["temperature"].max().reset_index()
    max_temps["dev-id"] = sensor_df["dev-id"].iloc[0]

    if sensor_df["dev-id"].iloc[0] in SENSOR_SUN:
        max_temps["type"] = "sun"
    else:
        max_temps["type"] = "shade"

    return max_temps


max_temp_sensors = {
    sensor_id: max_temp_per_day(sensor_df) for sensor_id, sensor_df in sensors.items()
}

df_merged = pd.concat(max_temp_sensors, ignore_index=True)

# Calculate average temperature for sensors in the sun
sun_avg_temp = df_merged[df_merged["type"] == "sun"]["temperature"].mean()

# Calculate average temperature for sensors in the shade
shade_avg_temp = df_merged[df_merged["type"] == "shade"]["temperature"].mean()

# Plotting
plt.figure(figsize=(10, 6))

# Plot sensors in the sun first
for sensor_id in SENSOR_SUN:
    sensor_data = df_merged[df_merged["dev-id"] == sensor_id]
    sensor_digits = sensor_id[-4:]
    label = f"Sun: {sensor_digits}"
    plt.plot(sensor_data["date"], sensor_data["temperature"], label=label)

# Plot sensors in the shade next
for sensor_id in SENSOR_SHADE:
    sensor_data = df_merged[df_merged["dev-id"] == sensor_id]
    sensor_digits = sensor_id[-4:]
    label = f"Shade: {sensor_digits}"
    plt.plot(sensor_data["date"], sensor_data["temperature"], label=label)

# Add average temperature lines
plt.axhline(
    y=sun_avg_temp,
    color="orange",
    linestyle="--",
    label=f"Sun Avg Temp: {sun_avg_temp:.2f}°C",
)
plt.axhline(
    y=shade_avg_temp,
    color="blue",
    linestyle="--",
    label=f"Shade Avg Temp: {shade_avg_temp:.2f}°C",
)

plt.xlabel("Date")
plt.ylabel("Max Temperature (°C)")
plt.title("Max Temperature per Day for Each Sensor")
plt.legend(title="Sensor Location")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()


print("Time to run script:", datetime.now() - startTime)

plt.show()
