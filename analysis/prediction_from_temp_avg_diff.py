import utils
import matplotlib.pyplot as plt

SUN_SENSOR_ID = "24E124136E106619"
SHADER_SENSOR_ID = "24E124136E106618"

start_date = "2024-07-01"
end_date = "2024-07-30"

df = utils.get_csv()
df = utils.apply_date_range(df, start_date, end_date)
sensors = utils.separate_sensors(df)

shade_sensors = [sensors[i] for i in utils.SENSOR_SHADE]
sun_sensors = [sensors[i] for i in utils.SENSOR_SUN]

SUN = sensors[SUN_SENSOR_ID]
SHADE = sensors[SHADER_SENSOR_ID]


def add_date_col(df):
    df["date"] = df["time"].dt.date
    avg_temp = df.groupby("date")["temperature"].mean().reset_index()
    avg_temp["dev-id"] = df["dev-id"].iloc[0]
    return avg_temp


shade_sensors = [add_date_col(sensor) for sensor in shade_sensors]
sun_sensors = [add_date_col(sensor) for sensor in sun_sensors]


# Calculate the mean temperatures for each dataframe
shade_mean_temperatures = [df["temperature"].mean() for df in shade_sensors]
sun_mean_temperatures = [df["temperature"].mean() for df in sun_sensors]

# Calculate the overall average temperatures
avg_shade_mean_temperature = sum(shade_mean_temperatures) / len(shade_mean_temperatures)
avg_sun_mean_temperature = sum(sun_mean_temperatures) / len(sun_mean_temperatures)

temp_diff = avg_sun_mean_temperature - avg_shade_mean_temperature

SUN = add_date_col(SUN.copy())
SHADE = add_date_col(SHADE.copy())


PREDICTION = SHADE.copy()
PREDICTION2 = SHADE.copy()
PREDICTION["temperature"] = SHADE["temperature"] + temp_diff

plt.plot(SUN["date"], SUN["temperature"], color="orange", label="Sun")
plt.plot(SHADE["date"], SHADE["temperature"], color="blue", label="Shade")
plt.plot(
    PREDICTION["date"], PREDICTION["temperature"], color="green", label="Prediction"
)


plt.xlabel("Date")
plt.ylabel("Avg Temperature")
plt.title("Temperature difference after tree removal")
plt.legend(title="Sensor Location")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
