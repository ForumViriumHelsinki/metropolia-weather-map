import requests
import pandas as pd
import gzip
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

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


def fetch_geojson(url):
    """Lataa ja käsittelee yksittäisen GeoJSON-tiedoston"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        geojson = response.json()
        return {
            "sensor_id": geojson["id"],
            "type": geojson["properties"].get("Tyyppi", "Tuntematon"),
            "notes": geojson["properties"].get("Huomiot", ""),
        }
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Virhe haettaessa GeoJSON-tiedostoa {url}: {e}")
        return None


def fetch_csv(url):
    """Lataa ja lukee yksittäisen CSV-tiedoston"""
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return pd.read_csv(gzip.open(BytesIO(response.content), "rt"))
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Virhe haettaessa CSV-tiedostoa {url}: {e}")
        return None


def fetch_geojson_data(geojson_urls):
    """Lataa kaiken GeoJSON-metadatan rinnakkain"""
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_geojson, geojson_urls))
    return pd.DataFrame([r for r in results if r])  # Poistetaan epäonnistuneet haut


def fetch_csv_data(csv_urls):
    """Lataa kaikki CSV-tiedostot rinnakkain ja yhdistää ne"""
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_csv, csv_urls))
    return pd.concat([df for df in results if df is not None], ignore_index=True)

def load_and_process_cloudiness(file_path="../data/cloudiness.csv"):
    """
    Loads and processes the cloudiness data:
    - Converts date columns into datetime
    - Extracts numeric cloudiness values (0-8)
    - Replaces 9 (undefined cloudiness) with NaN
    - Computes daily average cloudiness
    
    Returns:
        pd.DataFrame: DataFrame with daily average cloudiness
    """

    # Load cloudiness data
    cloud_df = pd.read_csv(file_path, encoding="utf-8", sep=",")
    cloud_df.columns = ["Havaintoasema", "Vuosi", "Kuukausi", "Päivä", "Aika", "Pilvisyys"]

    # Convert to datetime
    cloud_df["date"] = pd.to_datetime(
        cloud_df["Vuosi"].astype(str) + "-" +
        cloud_df["Kuukausi"].astype(str) + "-" +
        cloud_df["Päivä"].astype(str)
    ).dt.date

    # Extract numeric cloudiness values (0-8)
    cloud_df["Pilvisyys"] = cloud_df["Pilvisyys"].str.extract(r"(\d+)").astype(float)

    # Replace 9 (undefined cloudiness) with NaN
    cloud_df.loc[cloud_df["Pilvisyys"] == 9, "Pilvisyys"] = None

    # Compute daily average cloudiness (ignoring NaN)
    cloud_daily_avg = cloud_df.groupby("date")["Pilvisyys"].mean().reset_index()

    return cloud_daily_avg
