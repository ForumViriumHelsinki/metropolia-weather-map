import pandas as pd
import matplotlib.pyplot as plt
import utils

df = utils.get_day_data()
df["hour"] = df["time"].dt.hour

sun_sensors = [group for dev_id, group in df.groupby("dev-id") if dev_id in utils.SENSOR_SUN]
shade_sensors = [group for dev_id, group in df.groupby("dev-id") if dev_id in utils.SENSOR_SHADE]

def get_sensor_hourly_average(df):
    avg_frame = df.groupby("hour")["temperature"].mean().reset_index()
    avg_frame["dev-id"] = df["dev-id"].iloc[0]
    return avg_frame

avg_sun_temps = [get_sensor_hourly_average(s) for s in sun_sensors]
avg_shade_temps = [get_sensor_hourly_average(s) for s in shade_sensors]

hourly_avg_sun_temps = pd.concat(avg_sun_temps).groupby("hour")["temperature"].mean()
hourly_avg_shade_temps = pd.concat(avg_shade_temps).groupby("hour")["temperature"].mean()

hourly_diff = hourly_avg_sun_temps - hourly_avg_shade_temps

plt.figure(figsize=(10, 5))
for s in avg_sun_temps:
    label = s["dev-id"].iloc[0][-2:]
    plt.plot(s["hour"], s["temperature"], color="orange", alpha=0.5, label=f"Sun {label}")
for s in avg_shade_temps:
    label = s["dev-id"].iloc[0][-2:]
    plt.plot(s["hour"], s["temperature"], color="blue", alpha=0.5, label=f"Shade {label}")

plt.plot(hourly_avg_sun_temps, color="darkorange", linewidth=2, label="Average Sun")
plt.plot(hourly_avg_shade_temps, color="darkblue", linewidth=2, label="Average Shade")

plt.xticks(ticks=range(0, 24), labels=[f"{h}:00" for h in range(0, 24)])  # Format as HH:00
plt.xlabel("Hour of the Day")
plt.ylabel("Temperature (°C)")
plt.title("Average Hourly Temperature (Sun vs Shade Sensors)")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 5))
hourly_diff.plot(kind="bar", color="purple")

plt.xticks(ticks=range(0, 24), labels=[f"{h}:00" for h in range(0, 24)], rotation=45)
plt.xlabel("Hour of the Day")
plt.ylabel("Temperature Difference (°C)")
plt.title("Hourly Temperature Difference (Sun - Shade)")
plt.grid()
plt.show()
