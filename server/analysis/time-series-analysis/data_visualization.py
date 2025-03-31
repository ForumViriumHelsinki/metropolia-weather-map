import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data_calculations import compute_daily_median_temperature, compute_day_night_difference, compute_daily_temperature_range, compute_monthly_night_temperature, compute_monthly_night_min_temperature
from data_preprocessing import prepare_data

def plot_daily_temperature_range(df):
    print("[INFO] Plotting daily temperature range...")
    range_df = compute_daily_temperature_range(df)

    # Summary of statistics
    summary = range_df.groupby("district")["temperature_range"].agg(["mean", "std"]).round(2)
    print("\n[SUMMARY] Average daily temperature range (°C) with standard deviation:")
    print(summary)
    print(f"\n[INFO] Most dynamic daily temperatures: {summary['mean'].idxmax()}")

    # Plot with a line for each district
    plt.figure(figsize=(14, 6))
    for district in range_df["district"].unique():
        subset = range_df[range_df["district"] == district]
        plt.plot(subset["date"], subset["temperature_range"], label=district)

    # Adjust the plot
    plt.title("Daily Temperature Range by District")
    plt.xlabel("Date")
    plt.ylabel("Temperature Range (°C)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_daily_median_temperature(df):
    print("[INFO] Plotting daily median temperature...")
    daily_median = compute_daily_median_temperature(df)

    # Summary of statistics
    summary = daily_median.groupby("district")["temperature"].agg(["mean", "std"]).round(2)
    print("\n[SUMMARY] Average daily median temperature (°C) with standard deviation:")
    print(summary)
    print(f"\n[INFO] Warmest area on average: {summary['mean'].idxmax()}")

    # Plot
    plt.figure(figsize=(14, 6))
    for district in daily_median["district"].unique():
        subset = daily_median[daily_median["district"] == district]
        plt.plot(subset["date"], subset["temperature"], label=district)

    plt.title("Daily Median Temperature by District")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_day_night_difference(df):
    print("[INFO] Plotting day-night temperature difference (monthly)...")
    diff_df = compute_day_night_difference(df)

    diff_df['date'] = pd.to_datetime(diff_df['date'])
    diff_df['month'] = diff_df['date'].dt.month
    monthly_diff = diff_df.groupby(['month', 'district'])['day_night_diff'].mean().unstack()

    avg_diff = monthly_diff.mean(axis=0).round(2)
    print("\n[SUMMARY] Average monthly day-night temperature difference (°C):")
    print(avg_diff.sort_values(ascending=False))

    monthly_diff.plot(kind='bar', figsize=(14, 6), width=0.8)
    plt.title("Monthly Average Day-Night Temperature Difference by District")
    plt.xlabel("Month")
    plt.ylabel("Temperature Difference (°C)")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def plot_monthly_night_temperature(df):
    print("[INFO] Plotting monthly night-time median temperature...")
    night_df = compute_monthly_night_temperature(df)
    night_df["month_str"] = night_df["month"].astype(str)

    # Summary of statistics
    avg_night = night_df.groupby("district")["temperature"].mean().round(2)
    extremes = night_df.groupby("district")["temperature"].agg(["min", "max"]).round(2)
    print("\n[SUMMARY] Average monthly night-time temperature (°C):")
    print(avg_night.sort_values(ascending=False))
    print("\n[INFO] Monthly night temperature extremes per district (°C):")
    print(extremes)
    print(f"\n[INFO] Warmest nights on average: {avg_night.idxmax()}")

    # Plotting with bars for each district
    districts = night_df["district"].unique()
    months = sorted(night_df["month_str"].unique())
    x = np.arange(len(months))
    width = 0.25
    offset = (len(districts) - 1) / 2 * width

    plt.figure(figsize=(12, 6))

    for i, district in enumerate(districts):
        subset = night_df[night_df["district"] == district]
        heights = [subset[subset["month_str"] == m]["temperature"].values[0] if not subset[subset["month_str"] == m].empty else np.nan for m in months]
        plt.bar(x - offset + i * width, heights, width=width, label=district)

    plt.xticks(ticks=x, labels=months, rotation=45)
    plt.title("Monthly Median Night-Time Temperature by District")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.grid(axis="y")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_monthly_night_temperature_difference(df, reference_district="Laajasalo"):
    """
    Plots monthly difference in night-time temperature between each district and the reference district.
    """
    print("[INFO] Plotting monthly night-time temperature differences (compared to Laajasalo)...")
    night_df = compute_monthly_night_temperature(df)
    night_df["month_str"] = night_df["month"].astype(str)

    # Pivot table: rows = month, columns = district, values = temperature
    pivot = night_df.pivot(index="month_str", columns="district", values="temperature")

    if reference_district not in pivot.columns:
        print(f"[WARNING] Reference district '{reference_district}' not found in data.")
        return

    # Subtract Laajasalo's temperatures
    diff_df = pivot.subtract(pivot[reference_district], axis=0)
    diff_df = diff_df.drop(columns=[reference_district])  # Remove self-reference

    # Print monthly results before plotting
    print("\n[SUMMARY] Average monthly night-time temperature difference vs. Laajasalo (°C):")
    print(diff_df.mean().round(2))

    # Plot
    plt.figure(figsize=(12, 6))
    for district in diff_df.columns:
        plt.plot(diff_df.index, diff_df[district], marker='o', label=f"{district} - {reference_district}")

    plt.axhline(0, color="gray", linestyle="--", linewidth=1)
    plt.title(f"Monthly Night-Time Temperature Difference Compared to {reference_district}")
    plt.xlabel("Month")
    plt.ylabel("Temperature Difference (°C)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_monthly_night_min_temperature(df):
    """
    Plots monthly night-time minimum temperatures and prints monthly summaries for each district.
    """
    print("[INFO] Plotting monthly night-time minimum temperatures...")
    night_min_df = compute_monthly_night_min_temperature(df)
    night_min_df["month_str"] = night_min_df["month"].astype(str)

    # Print monthly results before plotting
    months = sorted(night_min_df["month_str"].unique())
    for month in months:
        print(f"\n[SUMMARY] Minimum night-time temperatures for {month}:")
        monthly_data = night_min_df[night_min_df["month_str"] == month]
        print(monthly_data[['district', 'temperature']].sort_values('temperature'))

    # Plotting the bar chart for monthly minimum night-time temperatures
    districts = night_min_df["district"].unique()
    x = np.arange(len(months))
    width = 0.25
    offset = (len(districts) - 1) / 2 * width

    plt.figure(figsize=(12, 6))

    for i, district in enumerate(districts):
        subset = night_min_df[night_min_df["district"] == district]
        heights = [subset[subset["month_str"] == m]["temperature"].values[0] if not subset[subset["month_str"] == m].empty else np.nan for m in months]
        plt.bar(x - offset + i * width, heights, width=width, label=district)

    plt.xticks(ticks=x, labels=months, rotation=45)
    plt.title("Monthly Minimum Night-Time Temperature by District")
    plt.xlabel("Month")
    plt.ylabel("Min Temperature (°C)")
    plt.grid(axis="y")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Average temperatures across districts
    summary = night_min_df.groupby("district")["temperature"].mean().round(2)
    print("\n[SUMMARY] Average monthly minimum night-time temperature (°C):")
    print(summary.sort_values(ascending=False))
    print(f"\n[INFO] Warmest night minimums on average: {summary.idxmax()}")

def test_visualizations():
    """
    Test function to run visualizations with preprocessed data.
    """
    df = prepare_data("2024-07-01", "2025-03-31", ["Vallila", "Koivukylä", "Laajasalo"])
    plot_daily_temperature_range(df)
    plot_daily_median_temperature(df)
    plot_day_night_difference(df)
    plot_monthly_night_min_temperature(df)
    plot_monthly_night_temperature(df)
    plot_monthly_night_temperature_difference(df)

if __name__ == "__main__":
    test_visualizations()
