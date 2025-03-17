from fastapi import APIRouter, Query
import pandas as pd
from .analysis_route_utils import (
    fetch_csv,
    create_bar_chart,
    create_plot_chart,
    filter_sensors,
    filter_date_range,
)

router = APIRouter()


@router.get("/api/analysis/daily-humidity-graph")
async def daily_humidity_graph(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    sensor_id: str = Query(
        None,
        description="Sensor ID, 'sun' for sun sensors, 'shade' for shade sensors, or leave blank for all",
    ),
):
    """
    Generates a humidity chart that dynamically adjusts based on the selected date range:
    - If the range is a single day, show hourly humidity.
    - If the range spans multiple days, show daily average humidity.
    """

    end_date = end_date or start_date  # Default to single date if no end_date provided

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    df = fetch_csv(start_year, end_year)
    filtered_df = filter_date_range(df, start_date, end_date)

    if filtered_df.empty:
        return {"error": f"No data available from {start_date} to {end_date}"}

    if sensor_id == "all":
        sensor_id = ""

    filtered_df, sensor_label = filter_sensors(filtered_df, sensor_id)

    num_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

    if num_days == 1:
        # Single-day graph: group by hour
        humidity_data = (
            filtered_df.groupby(filtered_df["time"].dt.hour)["humidity"]
            .mean()
            .reset_index()
        )
        x_values = humidity_data["time"]
        x_label = "Hour of the Day"
        title = f"Hourly Humidity for {sensor_label} on {start_date}"
    else:
        # Multi-day graph: group by day
        humidity_data = (
            filtered_df.groupby(filtered_df["date"])["humidity"].mean().reset_index()
        )
        x_values = humidity_data["date"]
        x_label = "Date"
        title = f"Daily Average Humidity for {sensor_label} ({start_date} - {end_date})"

    return create_bar_chart(
        x=x_values,
        y=humidity_data["humidity"],
        title=title,
        xlabel=x_label,
        ylabel="Humidity (%)",
        color="blue",
    )


@router.get("/api/analysis/daily-temperature-graph")
async def daily_temperature_graph(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    sensor_id: str = Query(
        None,
        description="Sensor ID, 'sun' for sun sensors, 'shade' for shade sensors, or leave blank for all",
    ),
):
    """
    Generates a temperature chart that dynamically adjusts based on the selected date range:
    - If the range is a single day, show hourly temperature.
    - If the range spans multiple days, show daily average temperature.
    """

    end_date = end_date or start_date

    start_year = int(start_date[:4])
    end_year = int(end_date[:4])

    df = fetch_csv(start_year, end_year)
    filtered_df = filter_date_range(df, start_date, end_date)

    if filtered_df.empty:
        return {"error": f"No data available from {start_date} to {end_date}"}

    if sensor_id == "all":
        sensor_id = ""

    filtered_df, sensor_label = filter_sensors(filtered_df, sensor_id)

    num_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

    if num_days == 1:
        # Single-day graph: group by hour
        temp_data = (
            filtered_df.groupby(filtered_df["time"].dt.hour)["temperature"]
            .mean()
            .reset_index()
        )
        x_values = temp_data["time"]
        x_label = "Hour of the Day"
        title = f"Hourly Temperature for {sensor_label} on {start_date}"
    else:
        # Multi-day graph: group by day
        temp_data = (
            filtered_df.groupby(filtered_df["date"])["temperature"].mean().reset_index()
        )
        x_values = temp_data["date"]
        x_label = "Date"
        title = (
            f"Daily Average Temperature for {sensor_label} ({start_date} - {end_date})"
        )

    return create_plot_chart(
        x=x_values,
        y=temp_data["temperature"],
        title=title,
        xlabel=x_label,
        ylabel="Temperature (°C)",
        color="red",
    )
