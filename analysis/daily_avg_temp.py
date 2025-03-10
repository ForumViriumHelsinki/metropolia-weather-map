import pandas as pd
import matplotlib.pyplot as plt
import utils

df = utils.get_csv()
df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date

SELECTED_DATE = "2024-07-01"  # Format: YYYY-MM-DD

filtered_df = df[df["date"] == pd.to_datetime(SELECTED_DATE).date()]

if filtered_df.empty:
    print(f"No data available for {SELECTED_DATE}")
else:
    hourly_avg_temp = filtered_df.groupby(df["time"].dt.hour)["temperature"].mean()

    plt.figure(figsize=(10, 5))
    plt.plot(hourly_avg_temp.index, hourly_avg_temp.values, marker="o", linestyle="-", color="red", label="Temperature")
    
    plt.xticks(ticks=range(0, 24, 2), labels=[f"{h}:00" for h in range(0, 24, 2)])  # Show every 2 hours
    plt.xlabel("Hour of the Day")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature for {SELECTED_DATE}")
    plt.legend()
    plt.grid()
    plt.show()
