import pandas as pd

SENSORS = [
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


def get_csv(year=None):
    files = {
        2024: "../data/makelankatu-2024.csv",
        2025: "../data/makelankatu-2025.csv",
    }
    
    if year is None:
        # Load all years if year is not specified
        return pd.concat([pd.read_csv(f) for f in files.values()], ignore_index=True)
    elif year in files:
        return pd.read_csv(files[year])
    else:
        raise ValueError("Invalid year. Choose 2024, 2025, or None for both.")


def separate_sensors(sensor_df):
    filtered = {
        sensor_id: group
        for sensor_id, group in sensor_df.groupby("dev-id")
        if sensor_id in SENSORS
    }
    return filtered


def apply_date_range(df, start_date, end_date):
    mask = (df["time"] >= start_date) & (df["time"] <= end_date)
    return df.loc[mask]


def filter_data_by_sunlight(daytime=True):
    daylight_info = pd.read_csv("../data/daylight.csv", parse_dates=["sunrise", "sunset"])
    sensor_readings = get_csv()

    sensor_readings["date"] = sensor_readings["time"].dt.date
    daylight_info["date"] = daylight_info["sunrise"].dt.date

    combined_data = pd.merge(sensor_readings, daylight_info, on="date")

    if daytime:
        mask = (combined_data["time"] >= combined_data["sunrise"]) & (combined_data["time"] <= combined_data["sunset"])
    else:
        mask = (combined_data["time"] < combined_data["sunrise"]) | (combined_data["time"] > combined_data["sunset"])

    return combined_data[mask].drop(columns=["sunrise", "sunset"])


def get_day_data():
    return filter_data_by_sunlight(daytime=True)


def get_night_data():
    return filter_data_by_sunlight(daytime=False)


def get_cloudiness_data(file_path="../data/cloudiness.csv"):
    cloud_df = pd.read_csv(file_path, encoding="utf-8", sep=",")
    cloud_df.columns = ["Havaintoasema", "Vuosi", "Kuukausi", "Päivä", "Aika", "Pilvisyys"]

    cloud_df["date"] = pd.to_datetime(cloud_df[["Vuosi", "Kuukausi", "Päivä"]]).dt.date
    cloud_df["Pilvisyys"] = cloud_df["Pilvisyys"].str.extract(r"(\d+)").astype(float)
    cloud_df.loc[cloud_df["Pilvisyys"] == 9, "Pilvisyys"] = None

    return cloud_df.groupby("date")["Pilvisyys"].mean().reset_index()
