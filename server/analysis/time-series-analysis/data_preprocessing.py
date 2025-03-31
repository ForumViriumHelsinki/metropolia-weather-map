import pandas as pd
from data_loading import load_sensor_data

def clean_sensor_data(df):
    """
    Cleans sensor data by handling missing values, filtering out invalid readings,
    and ensuring correct data types.
    """
    print("[INFO] Cleaning sensor data...")
    original_len = len(df)
    df = df.dropna(subset=["temperature", "humidity"])
    df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
    df = df[(df["temperature"] > -50) & (df["temperature"] < 60)]
    cleaned_len = len(df)
    removed = original_len - cleaned_len
    print(f"[INFO] Rows after cleaning: {cleaned_len} (removed {removed})")
    return df


def remove_pre_analysis_data(df):
    """
    Removes sensor data before trusted start dates for each district.
    Optimized for performance using vectorized filtering per district.
    """
    print("[INFO] Filtering out data before reliable analysis start dates...")

    analysis_start_dates = {
        "Laajasalo": pd.Timestamp("2024-06-25", tz="UTC"),
        "Koivukylä": pd.Timestamp("2024-06-25", tz="UTC"),
        "Vallila": pd.Timestamp("2024-06-17", tz="UTC"),
    }

    filtered_parts = []

    for district, start_date in analysis_start_dates.items():
        if district in df["district"].unique():
            part = df[(df["district"] == district) & (df["time"] >= start_date)]
            filtered_parts.append(part)

    filtered_df = pd.concat(filtered_parts, ignore_index=True)
    removed = len(df) - len(filtered_df)
    print(f"[INFO] Removed {removed} rows before reliable analysis start dates.")
    return filtered_df


def prepare_data(start_date, end_date, locations):
    """
    Loads, cleans, and filters sensor data for the selected locations and time range.
    """
    df = load_sensor_data(start_date, end_date, locations)
    df = clean_sensor_data(df)
    df = remove_pre_analysis_data(df) # Delete this when anomalous_sensor_detection.py works
    return df


if __name__ == "__main__":
    df = prepare_data("2024-01-01", "2025-03-27", ["Vallila", "Koivukylä"])
    print("\n[INFO] Processed data:")
    print(df.head())
