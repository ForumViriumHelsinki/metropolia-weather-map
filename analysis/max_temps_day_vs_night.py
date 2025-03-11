import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from utils import get_day_data, SENSOR_SUN, SENSOR_SHADE, apply_date_range

DATE_RANGE = {"start_date": "2024-07-01", "end_date": "2024-09-30"}

startTime = datetime.now()

# Load and filter daytime data
df = apply_date_range(get_day_data(), DATE_RANGE["start_date"], DATE_RANGE["end_date"])
df["date"] = pd.to_datetime(df["time"]).dt.date

# Compute daily max temperature per sensor
daily_max = df.groupby(["date", "dev-id"])["temperature"].max().reset_index()

# Compute mean max temperatures for sun and shade sensors
sun_avg = daily_max[daily_max["dev-id"].isin(SENSOR_SUN)].groupby("date")["temperature"].mean()
shade_avg = daily_max[daily_max["dev-id"].isin(SENSOR_SHADE)].groupby("date")["temperature"].mean()

# Compute temperature difference
temp_diff = pd.DataFrame({"date": sun_avg.index, "temperature_diff": sun_avg - shade_avg})

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(temp_diff["date"], temp_diff["temperature_diff"], marker="o", linestyle="-", color="red")
plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
plt.xlabel("Date")
plt.ylabel("Temperature Difference (°C)")
plt.title("Daily Temperature Difference (Sun - Shade) During the Day")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

print("Time to run script:", datetime.now() - startTime)
