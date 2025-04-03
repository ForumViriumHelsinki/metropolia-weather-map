import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

""" These values are loaded dynamically at the end of the script file with get_sensors() function.
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
"""

BASE_URL = "https://bri3.fvh.io/opendata/makelankatu/"

def get_csv(year=None):
    """Load sensor data for a specific year or all available years."""
    available_years = [2024, 2025]  # Update this when new data is available

    if year is None:
        dfs = [fetch_csv(y) for y in available_years]
        df = pd.concat(dfs, ignore_index=True)
    elif year in available_years:
        df = fetch_csv(year)
    else:
        raise ValueError(f"Invalid year. Choose from {available_years} or None for all years.")

    print("CSV loading complete.")
    return df


def fetch_csv(year):
    """Fetch and load a CSV file for a given year."""
    filename = f"makelankatu-{year}.csv.gz"
    url = BASE_URL + filename

    print(f"Fetching CSV data for {year} from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    return pd.read_csv(url, parse_dates=["time"])


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

    cloud_df = cloud_df.rename(columns={"Vuosi": "year", "Kuukausi": "month", "Päivä": "day"})
    cloud_df["date"] = pd.to_datetime(cloud_df[["year", "month", "day"]]).dt.date
    cloud_df["Pilvisyys"] = cloud_df["Pilvisyys"].str.extract(r"(\d+)").astype(float)
    cloud_df.loc[cloud_df["Pilvisyys"] == 9, "Pilvisyys"] = None

    return cloud_df.groupby("date")["Pilvisyys"].mean().reset_index()

"""
returns a list of links to .geojson files found at the BASE_URL
"""
def get_geojson_files():
    """Fetch the list of available .geojson files from the URL."""
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed to fetch file list")
        return []

    # Parse the HTML to find all .geojson file links
    soup = BeautifulSoup(response.text, 'html.parser')
    files = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.geojson')]

    return files

"""
files is a list of links to .geojson files, you can get them using the get_geojson_files function
This function returns the "id" and "Tyyppi" from each file
"""
def fetch_sensorid_and_type(files):
    """Download each .geojson file and extract 'id' and 'Tyyppi'."""
    extracted_data = []

    for file in files:
        file_url = BASE_URL + file
        response = requests.get(file_url)
        if response.status_code != 200:
            print(f"Failed to fetch {file}")
            continue

        try:
            geojson_data = response.json()
            # Extracting required fields
            sensor_id = geojson_data.get("id", "Unknown ID")
            tyyppi = geojson_data.get("properties", {}).get("Tyyppi", "Unknown Tyyppi")
            extracted_data.append((sensor_id, tyyppi))
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file}")

    return extracted_data

def get_sensors():
    sensordata = fetch_sensorid_and_type(get_geojson_files())  # Fetch sensor data
    sensors = []
    sensor_sun = []
    sensor_shade = []

    for item in sensordata:  # Iterate through the list of tuples (id, Tyyppi)
        sensor_id, sensor_type = item  # Unpack tuple
        if sensor_id != "Unknown ID":
            sensors.append(sensor_id)  # Add sensor ID to the main list

        if sensor_type == "Auringossa":  # Sunlight sensors
            sensor_sun.append(sensor_id)
        elif sensor_type == "Varjossa":  # Shade sensors
            sensor_shade.append(sensor_id)
    """
    print("Sensor IDs:", sensors)
    print("Sensor IDs in sunlight:", sensor_sun)
    print("Sensor IDs in shade:", sensor_shade)
    """
    return sensors, sensor_sun, sensor_shade  # Return lists if needed

SENSORS, SENSOR_SUN, SENSOR_SHADE = get_sensors()

