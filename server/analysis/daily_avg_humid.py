import pandas as pd
import matplotlib.pyplot as plt
import utils

df = utils.get_csv()
df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date

SELECTED_DATE = "2024-07-01"

filtered_df = df[df["date"] == pd.to_datetime(SELECTED_DATE).date()]

if filtered_df.empty:
    print(f"No data available for {SELECTED_DATE}")
else:
    hourly_avg_humidity = filtered_df.groupby(df["time"].dt.hour)["humidity"].mean()

    plt.figure(figsize=(10, 5))
    plt.bar(hourly_avg_humidity.index, hourly_avg_humidity.values, color="blue", alpha=0.7, width=0.6)

    plt.xticks(ticks=range(0, 24, 2), labels=[f"{h}:00" for h in range(0, 24, 2)])
    plt.ylim(30, 100)  # Set humidity range (adjust based on data)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Humidity (%)")
    plt.title(f"Humidity Levels for {SELECTED_DATE}")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
