import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from utils import get_day_data, SENSOR_SUN, SENSOR_SHADE, get_cloudiness_data, apply_date_range

DATE_RANGE = {"start_date": "2024-07-01", "end_date": "2024-12-30"}

startTime = datetime.now()

# Function to compute daily temperature difference
def compute_daily_temp_difference(df):
    daily_max_temps = df.groupby(["date", "dev-id"])["temperature"].max().reset_index()

    sun_avg = daily_max_temps[daily_max_temps["dev-id"].isin(SENSOR_SUN)].groupby("date")["temperature"].mean().reset_index()
    shade_avg = daily_max_temps[daily_max_temps["dev-id"].isin(SENSOR_SHADE)].groupby("date")["temperature"].mean().reset_index()

    temp_diff = pd.merge(sun_avg, shade_avg, on="date", suffixes=("_sun", "_shade"))
    temp_diff["temperature_diff"] = temp_diff["temperature_sun"] - temp_diff["temperature_shade"]

    return temp_diff

# Function to plot cloudiness vs temperature difference
def plot_cloudiness_vs_temp_diff(df):
    # Scatter Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Pilvisyys"], df["temperature_diff"], alpha=0.5)
    plt.xlabel("Cloudiness (0 = Clear, 8 = Overcast)")
    plt.ylabel("Temperature Difference (Sun - Shade)")
    plt.title("Effect of Cloudiness on Temperature Difference")
    plt.grid(True)
    plt.show()

    # Line Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df["date"], df["temperature_diff"], label="Temperature Difference", color="red", linestyle="-", marker="o")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature Difference (°C)", color="red")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["Pilvisyys"], label="Cloudiness", color="blue", linestyle="--", marker="x")
    ax2.set_ylabel("Cloudiness (0-8)", color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    plt.title("Cloudiness vs. Temperature Difference Over Time")
    plt.grid(True)
    plt.show()

# Load Data
df = apply_date_range(get_day_data(), DATE_RANGE["start_date"], DATE_RANGE["end_date"])
df["date"] = pd.to_datetime(df["time"]).dt.date

# Compute temperature differences
temp_diff = compute_daily_temp_difference(df)

# Load cloudiness data and merge
cloud_daily_avg = get_cloudiness_data()
merged_df = pd.merge(temp_diff, cloud_daily_avg, on="date", how="left").fillna({"Pilvisyys": 0})

# Visualize results
plot_cloudiness_vs_temp_diff(merged_df)

# Compute correlation
correlation = merged_df["Pilvisyys"].corr(merged_df["temperature_diff"])
print(f"Correlation between Cloudiness and Temperature Difference: {correlation:.2f}")

# Print execution time
print("Time to run script:", datetime.now() - startTime)
