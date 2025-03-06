import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import IsolationForest
from utils import get_day_data, SENSOR_SUN, SENSOR_SHADE, load_and_process_cloudiness, apply_date_range

# Define date range
DATE_RANGE = {"start_date": "2024-07-01", "end_date": "2024-12-30"}

startTime = datetime.now()

# Function to compute daily temperature and humidity statistics
def compute_daily_stats(df, sensor_group=None):
    """Computes daily max temperature and humidity differences based on sensor type."""
    
    # Get daily max values per sensor
    daily_max = df.groupby(["date", "dev-id"])[["temperature", "humidity"]].max().reset_index()
    
    # Filter sensors if needed (all, shade, or sun)
    if sensor_group:
        daily_max = daily_max[daily_max["dev-id"].isin(sensor_group)]

    # Compute daily average max temp & humidity
    daily_avg = daily_max.groupby("date")[["temperature", "humidity"]].mean().reset_index()
    
    return daily_avg

# Function to run analysis on a dataset
def run_analysis(df, title):
    print(f"\n=== Running Analysis for: {title} ===")

    # Filter data for date range
    df = apply_date_range(df, DATE_RANGE["start_date"], DATE_RANGE["end_date"])
    df["date"] = pd.to_datetime(df["time"]).dt.date

    # Compute statistics for all, shade, and sun sensors separately
    if title == "All Sensors":
        data = compute_daily_stats(df)
    elif title == "Shade Sensors":
        data = compute_daily_stats(df, SENSOR_SHADE)
    elif title == "Sun Sensors":
        data = compute_daily_stats(df, SENSOR_SUN)
    else:
        return  # Invalid title

    # Load cloudiness data and merge
    cloud_data = load_and_process_cloudiness()
    merged_df = pd.merge(data, cloud_data, on="date", how="left").fillna({"Pilvisyys": 0})

    # ** Seasonal Decomposition**
    decomposition = seasonal_decompose(merged_df.set_index("date")["temperature"], model="additive", period=30)

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    decomposition.observed.plot(ax=axes[0], title="Observed")
    decomposition.trend.plot(ax=axes[1], title="Trend")
    decomposition.seasonal.plot(ax=axes[2], title="Seasonality")
    decomposition.resid.plot(ax=axes[3], title="Residuals")
    plt.tight_layout()
    plt.show()

    # **2️⃣ SARIMAX Forecasting**
    train = merged_df.set_index("date")[["temperature", "humidity", "Pilvisyys"]][:-30]
    test = merged_df.set_index("date")[["temperature", "humidity", "Pilvisyys"]][-30:]

    model = SARIMAX(train["temperature"], exog=train[["humidity", "Pilvisyys"]], order=(1,1,1), seasonal_order=(1,1,1,30))
    results = model.fit()

    predictions = results.predict(start=len(train), end=len(merged_df)-1, exog=test[["humidity", "Pilvisyys"]], dynamic=False)

    plt.figure(figsize=(10, 5))
    plt.plot(merged_df["date"], merged_df["temperature"], label="Actual")
    plt.plot(predictions.index, predictions, label="Predicted", linestyle="dashed")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title(f"SARIMAX Forecast vs Actual - {title}")
    plt.legend()
    plt.show()

    # ** Anomaly Detection**
    features = merged_df[["temperature", "humidity", "Pilvisyys"]]
    model = IsolationForest(contamination=0.02, random_state=42)
    merged_df["anomaly"] = model.fit_predict(features)

    plt.figure(figsize=(10, 5))
    plt.plot(merged_df["date"], merged_df["temperature"], label="Temperature")
    plt.scatter(merged_df["date"][merged_df["anomaly"] == -1], merged_df["temperature"][merged_df["anomaly"] == -1], color="red", label="Anomaly", marker="x")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.title(f"Anomaly Detection - {title}")
    plt.legend()
    plt.show()

    # Compute and print correlation
    correlation = merged_df["Pilvisyys"].corr(merged_df["temperature"])
    print(f"Correlation between Cloudiness and Temperature ({title}): {correlation:.2f}")

# Run analysis for all three groups
run_analysis(get_day_data(), "All Sensors")
run_analysis(get_day_data(), "Shade Sensors")
run_analysis(get_day_data(), "Sun Sensors")

print("\nTotal time to run script:", datetime.now() - startTime)
