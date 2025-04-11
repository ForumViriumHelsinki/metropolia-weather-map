import os

import pandas as pd


def filter_daytime_data(df):
    # daylight csv location
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "data", "daylight.csv"
    )

    # Sunrise and sunset data
    daylight_info = pd.read_csv(csv_path, parse_dates=["sunrise", "sunset"])

    # Add date column to dataframae and daylight_info
    df["date"] = df["time"].dt.date
    daylight_info["date"] = daylight_info["sunrise"].dt.date

    # Merge dataframes on date
    df = pd.merge(df, daylight_info, on="date", how="left")

    # Create mask from the dates and filter the times
    mask = (df["time"] >= df["sunrise"]) & (df["time"] <= df["sunset"])

    # Apply the mask to filter out timestamps after sunset
    daylight_df = df[mask]
    return daylight_df
