from fastapi import Response
import pandas as pd
import matplotlib.pyplot as plt
import requests
import io


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

SENSORS_ALL = SENSOR_SUN + SENSOR_SHADE

CSV_CACHE = {}

def fetch_csv(start_year, end_year=None):
    """Fetch and cache CSV data for one or multiple years."""
    BASE_URL = "https://bri3.fvh.io/opendata/makelankatu/"
    
    if end_year is None:
        end_year = start_year

    all_dfs = []
    for year in range(start_year, end_year + 1):
        if year in CSV_CACHE:
            print(f"Using cached data for {year}")
            all_dfs.append(CSV_CACHE[year])
        else:
            filename = f"makelankatu-{year}.csv.gz"
            url = BASE_URL + filename
            print(f"Fetching CSV data for {year} from {url}...")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            df = pd.read_csv(url, parse_dates=["time"])
            CSV_CACHE[year] = df  # Store in cache
            all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True)


def save_plot_as_png(fig):
    """Converts a Matplotlib figure to a PNG response."""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    plt.close(fig)
    img_buffer.seek(0)

    return Response(content=img_buffer.getvalue(), media_type="image/png")


def create_bar_chart(x, y, title, xlabel, ylabel, color="blue"):
    """Generates a bar chart and returns a PNG response."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, y, color=color, alpha=0.7, width=0.6)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    return save_plot_as_png(fig)


def create_plot_chart(x, y, title, xlabel, ylabel, color="red"):
    """Generates a line plot and returns a PNG response."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, marker="o", linestyle="-", color=color, label=ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid()
    return save_plot_as_png(fig)


def filter_sensors(df, sensor_id):
    """Filters data based on a sensor ID, sun sensors, shade sensors, or all sensors."""
    sensor_groups = {
        "sun": (SENSOR_SUN, "Sun Sensors"),
        "shade": (SENSOR_SHADE, "Shade Sensors"),
    }
    if sensor_id in sensor_groups:
        filtered_df = df[df["dev-id"].isin(sensor_groups[sensor_id][0])]
        return filtered_df, sensor_groups[sensor_id][1]
    if sensor_id:
        return df[df["dev-id"] == sensor_id], f"Sensor {sensor_id}"

    return df[df["dev-id"].isin(SENSORS_ALL)], "All Sensors"


def filter_date_range(df, start_date, end_date):
    """Filters data based on a date range."""
    
    if "time" not in df.columns:
        raise ValueError("Missing 'time' column in DataFrame.")
    
    df["time"] = pd.to_datetime(df["time"], errors='coerce')  # Convert to datetime safely
    df = df.dropna(subset=["time"])
    df["date"] = df["time"].dt.date

    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    return df[(df["date"] >= start_date) & (df["date"] <= end_date)]