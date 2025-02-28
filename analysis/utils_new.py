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


def get_csv():
    df = pd.read_csv("../data/makelankatu-2024.csv")
    df["time"] = pd.to_datetime(df["time"])

    return df


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


def get_day_data():
    # Read csv containing daylight hour data
    day_df = pd.read_csv("../data/daylight.csv")
    day_df["sunrise"] = pd.to_datetime(day_df["sunrise"])
    day_df["sunset"] = pd.to_datetime(day_df["sunset"])

    # Get dataframe containing data from makelankatu csv
    df = get_csv()

    # Create date fields and merge dataframes on them
    df["date"] = df["time"].dt.date
    day_df["date"] = day_df["sunrise"].dt.date
    merged_df = pd.merge(df, day_df, on="date")

    # Create mask to get hours between sunrise and sunset
    mask = (merged_df["time"] >= merged_df["sunrise"]) & (
        merged_df["time"] <= merged_df["sunset"]
    )

    # Apply the mask
    filtered_df = merged_df[mask]
    filtered_df = filtered_df.drop(columns=["sunrise", "sunset"])

    return filtered_df


def get_night_data():
    # Read csv containing daylight hour data
    day_df = pd.read_csv("../data/daylight.csv")
    day_df["sunrise"] = pd.to_datetime(day_df["sunrise"])
    day_df["sunset"] = pd.to_datetime(day_df["sunset"])

    # Get dataframe containing data from makelankatu csv
    df = get_csv()

    # Create date fields and merge dataframes on them
    df["date"] = df["time"].dt.date
    day_df["date"] = day_df["sunrise"].dt.date
    merged_df = pd.merge(df, day_df, on="date")

    # Create mask to get hours outside sunrise and sunset
    mask = (merged_df["time"] < merged_df["sunrise"]) | (
        merged_df["time"] > merged_df["sunset"]
    )

    # Apply the mask
    filtered_df = merged_df[mask]
    filtered_df = filtered_df.drop(columns=["sunrise", "sunset"])

    return filtered_df
