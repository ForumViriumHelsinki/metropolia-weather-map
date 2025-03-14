from fastapi import APIRouter, Query
import pandas as pd
import requests


router = APIRouter()


@router.get("/api/analysis/daily-avg-temp")
async def daily_avg():
    data = daily_avg_temp()
    print("called")
    print(data)
    # query = select(sensordata_table).where(sensordata_table.c.time == date)

    return "hello"



def daily_avg_temp(date):
    SELECTED_DATE = "2024-07-01"  # Format: YYYY-MM-DD
    df = fetch_csv(2024)
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date

    filtered_df = df[df["date"] == pd.to_datetime(SELECTED_DATE).date()]
    if filtered_df.empty:
        print(f"No data available for {SELECTED_DATE}")
    else:
        hourly_avg_temp = filtered_df.groupby(df["time"].dt.hour)["temperature"].mean()

    return hourly_avg_temp



def fetch_csv(year):
    BASE_URL = "https://bri3.fvh.io/opendata/makelankatu/"

    """Fetch and load a CSV file for a given year."""
    filename = f"makelankatu-{year}.csv.gz"
    url = BASE_URL + filename

    print(f"Fetching CSV data for {year} from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    return pd.read_csv(url, parse_dates=["time"])