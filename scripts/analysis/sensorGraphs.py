import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

CSV_FILE = "../makelankatu-2024.csv"

# Load csv
data = pd.read_csv(CSV_FILE)


# Sort sensors by dev-id
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


sensor_dfs = []
for id in SENSOR_IDS: 
    df = pd.DataFrame(data)
    
    # Single sensor data
    df = df.loc[df["dev-id"] == id]

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Remove times before 27/5/24
    df = df[~(df["time"] < "2024-05-27")]
    sensor_dfs.append(df)

# Plot the data for all sensors
plt.figure(figsize=(12, 6))
for df, id in zip(sensor_dfs, SENSOR_IDS):
    plt.plot(df['time'], df['temperature'], label=f'Sensor {id}')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature Data for All Sensors')
plt.legend()
plt.show()


