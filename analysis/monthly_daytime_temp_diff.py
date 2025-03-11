import pandas as pd
import matplotlib.pyplot as plt
import utils

df = utils.get_day_data()
df = utils.apply_date_range(df, "2024-06-24", "2024-12-31")
df["month"] = df["time"].dt.month
print(df.head())

sun_sensors = [
    group for dev_id, group in df.groupby("dev-id") if dev_id in utils.SENSOR_SUN
]

shade_sensors = [
    group for dev_id, group in df.groupby("dev-id") if dev_id in utils.SENSOR_SHADE
]


def get_sensor_monthly_average(df):
    avg_frame = df.groupby("month")["temperature"].mean().reset_index()
    avg_frame["dev-id"] = df["dev-id"].iloc[0]

    return avg_frame


avg_sun_temps = [get_sensor_monthly_average(s) for s in sun_sensors]
avg_shade_temps = [get_sensor_monthly_average(s) for s in shade_sensors]


monthly_avg_sun_temps = pd.concat(avg_sun_temps).groupby("month")["temperature"].mean()
monthly_avg_shade_temps = (
    pd.concat(avg_shade_temps).groupby("month")["temperature"].mean()
)

avg_diff_per_month = monthly_avg_sun_temps - monthly_avg_shade_temps

for s in avg_sun_temps:
    label = s["dev-id"].iloc[0][-2:]
    plt.plot(s["month"], s["temperature"], color="orange", label=label)

for s in avg_shade_temps:
    label = s["dev-id"].iloc[0][-2:]
    plt.plot(s["month"], s["temperature"], color="blue", label=label)

plt.xlabel("Month")
plt.ylabel("Average temperature")
plt.title("Average monthly temperature")
plt.legend(title="Sensor id")
plt.show()

plt.figure()
avg_diff_per_month.plot(kind="bar", color="purple")
plt.xlabel("Month")
plt.ylabel("Average temperature difference")
plt.title("Average monthly temperature difference (Sun - Shade)")
plt.show()
