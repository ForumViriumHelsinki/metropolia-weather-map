import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE_24 = "./data/makelankatu-2024.csv"
CSV_FILE_25 = "./data/makelankatu-2025.csv"

# Load csv
data = pd.read_csv(CSV_FILE_24)

SENSOR_IDS = [
    "24E124136E106616", "24E124136E106617", "24E124136E106618", "24E124136E106619",
    "24E124136E106635", "24E124136E106636", "24E124136E106637", "24E124136E106638",
    "24E124136E106643", "24E124136E106661", "24E124136E106674", "24E124136E106686"
]

SENSOR_SUN = [
    "24E124136E106637", "24E124136E106638", "24E124136E106619", "24E124136E106661"
]

SENSOR_SHADE = [
    "24E124136E106616", "24E124136E106617", "24E124136E106618", "24E124136E106635",
    "24E124136E106636", "24E124136E106643" "24E124136E106674", "24E124136E106686"
]

SENSOR_MIX = [
    "24E124136E106637", "24E124136E106638", "24E124136E106619", "24E124136E106661",
    "24E124136E106643"

]

SENSOR_TO_ANALYZE = SENSOR_MIX

sensor_dfs = []
for id in SENSOR_TO_ANALYZE: 
    df = pd.DataFrame(data)
    
    # Single sensor data
    df = df.loc[df["dev-id"] == id]

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Remove times before 27/5/24
    df = df[~(df["time"] < "2024-05-27")]
    sensor_dfs.append(df)

# Plot the data for all selected sensors
plt.figure(figsize=(12, 6))
for df, id in zip(sensor_dfs, SENSOR_TO_ANALYZE):
    plt.plot(df['time'], df['temperature'], label=f'Sensor {id}')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature Data for All Sensors')
plt.legend()
plt.show()


