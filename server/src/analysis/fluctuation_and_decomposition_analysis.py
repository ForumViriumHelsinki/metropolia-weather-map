import asyncio

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import CheckButtons
from numpy.fft import fft
from src.utils.get_data_util import get_all_locations
from src.utils.save_graph import save_graph
from src.utils.utils import map_locations
from statsmodels.tsa.seasonal import STL

"""def load_data():
    data_frames = []
    year = input("Enter year for source data or 'all' for all available: ")
    try:    
        year = int(year)
    except ValueError:
        if(year == "" or year == "all"):
            year = None
        else:
            print("Please enter a valid year.")
    data_frames.append(utils.get_csv(year=year))
    data_frames.append(utils.get_r4c_csv(year=year))
    df = pd.concat(data_frames, ignore_index=True)

    print("Initial DataFrame Columns:", df.columns)

    if 'time' not in df.columns:
        print("Error: 'time' column is missing after loading data!")
        return None  # Exit early if something is wrong
    
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # Ensure datetime format
    df.rename(columns={'sensor': 'sensor'}, inplace=True)
    print (f'{df.columns} load check')
    return df
"""


def plot_raw_humidity(df, map):
    fig = plt.figure(figsize=(14, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
    ax = fig.add_subplot(gs[0])
    ax_cb = fig.add_subplot(gs[1])

    sensor_lines = {}

    for sensor_id, sensor_data in df.groupby("sensor"):
        (line,) = ax.plot(
            sensor_data["time"], sensor_data["humidity"], label=sensor_id, alpha=0.7
        )
        sensor_lines[sensor_id] = line

    ax.set_xlabel("Time")
    ax.set_ylabel("Humidity (%)")
    ax.set_title("Raw Humidity Data Over Time")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True)
    ax.legend(title="Sensors", bbox_to_anchor=(1, 1))

    ax_cb.set_xticks([])
    ax_cb.set_yticks([])
    ax_cb.set_frame_on(False)

    all_sensor_ids = list(sensor_lines.keys())
    location_labels = list(map.keys())
    all_labels = location_labels + all_sensor_ids
    visibility = [True] * len(all_labels)

    check = CheckButtons(ax_cb, all_labels, visibility)
    label_to_index = {label: i for i, label in enumerate(all_labels)}

    def toggle(label):
        status = check.get_status()
        if label in sensor_lines:
            sensor_lines[label].set_visible(status[label_to_index[label]])
        elif label in map:
            sensors = map[label]
            new_state = status[label_to_index[label]]
            for sid in sensors:
                if sid in sensor_lines:
                    sensor_lines[sid].set_visible(new_state)
                    idx = label_to_index.get(sid)
                    if idx is not None and check.get_status()[idx] != new_state:
                        check.set_active(idx)
        fig.canvas.draw_idle()

    check.on_clicked(toggle)
    plt.tight_layout()
    plt.show()


def plot_fft_analysis(df, map):
    df_copy = df.copy()
    df_copy.set_index("time", inplace=True)
    grouped = (
        df_copy[["sensor", "humidity"]]
        .groupby("sensor")
        .resample("D")
        .mean()
        .reset_index(level="sensor")
    )
    grouped["humidity"] = grouped["humidity"].rolling(window=7, min_periods=1).mean()

    fig = plt.figure(figsize=(14, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
    ax = fig.add_subplot(gs[0])
    ax_cb = fig.add_subplot(gs[1])

    sensor_lines = {}

    for sensor_id in grouped["sensor"].unique():
        sensor_df = grouped[grouped["sensor"] == sensor_id]
        humidity_fft = fft(sensor_df["humidity"].dropna())
        freqs = np.fft.fftfreq(len(humidity_fft))
        (line,) = ax.plot(
            freqs[: len(freqs) // 2],
            np.abs(humidity_fft[: len(freqs) // 2]),
            label=sensor_id,
            alpha=0.7,
        )
        sensor_lines[sensor_id] = line

    ax.set_yscale("log")
    ax.set_title("Fourier Transform of Humidity Data")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Magnitude")
    ax.grid(True)
    ax.legend(title="Sensors", bbox_to_anchor=(1, 1))

    ax_cb.set_xticks([])
    ax_cb.set_yticks([])
    ax_cb.set_frame_on(False)

    all_sensor_ids = list(sensor_lines.keys())
    location_labels = list(map.keys())
    all_labels = location_labels + all_sensor_ids
    visibility = [True] * len(all_labels)

    check = CheckButtons(ax_cb, all_labels, visibility)
    label_to_index = {label: i for i, label in enumerate(all_labels)}

    def toggle(label):
        status = check.get_status()
        if label in sensor_lines:
            sensor_lines[label].set_visible(status[label_to_index[label]])
        elif label in map:
            sensors = map[label]
            new_state = status[label_to_index[label]]
            for sid in sensors:
                if sid in sensor_lines:
                    sensor_lines[sid].set_visible(new_state)
                    idx = label_to_index.get(sid)
                    if idx is not None and check.get_status()[idx] != new_state:
                        check.set_active(idx)
        fig.canvas.draw_idle()

    check.on_clicked(toggle)
    plt.tight_layout()
    plt.show()


"""
def reconstruct_weekly_cycle(df):
    sensor_id = input("Enter sensor ID to analyze for weekly pattern: ")
    df_sensor = df[df['sensor'] == sensor_id].copy()
    df_sensor.set_index('time', inplace=True)
    df_sensor = df_sensor.resample('D').mean()
    df_sensor['humidity'] = df_sensor['humidity'].interpolate(method='time')

    y = df_sensor['humidity'].dropna()
    Y = fft(y)
    freqs = np.fft.fftfreq(len(Y))

    weekly_band = (freqs > 0.125) & (freqs < 0.15)
    Y_filtered = np.zeros_like(Y, dtype=complex)
    Y_filtered[weekly_band] = Y[weekly_band]
    Y_filtered[-weekly_band] = Y[-weekly_band]  # mirror frequencies for real signal

    reconstructed = np.real(ifft(Y_filtered))

    plt.figure(figsize=(12, 6))
    plt.plot(y.index, y, label='Original', alpha=0.5)
    plt.plot(y.index, reconstructed, label='Reconstructed ~Weekly Cycle', linewidth=2)
    plt.title(f"Weekly Humidity Cycle for Sensor {sensor_id}")
    plt.xlabel("Date")
    plt.ylabel("Humidity (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
"""


def plot_seasonal_decomposition(df):
    print("Columns at start of seasonal decomposition:", df.dtypes)

    if "time" not in df.columns:
        print("Error: 'time' column missing before STL decomposition!")
        return

    df = df.copy()
    df.set_index("time", inplace=True)
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    df = df[["humidity"]].resample("h").mean()
    df["humidity"] = df["humidity"].interpolate(method="time")
    df = df.dropna()

    if len(df) < 14:
        print("Error: Not enough data points for STL decomposition!")
        return

    stl = STL(df["humidity"], seasonal=143)
    result = stl.fit()

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    result.trend.plot(ax=axes[0], title="Trend")
    result.seasonal.plot(ax=axes[1], title="Seasonality")
    result.resid.plot(ax=axes[2], title="Residual")
    save_graph("fluc_test", plt, "test")
    plt.show()


def main():
    df = get_all_locations()
    print("Columns after loading data:", df.columns)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df.rename(columns={"dev-id": "sensor"}, inplace=True)
    map = map_locations()
    if df is not None:
        plot_raw_humidity(df, map)
        plot_fft_analysis(df, map)
        # reconstruct_weekly_cycle(df)
        plot_seasonal_decomposition(df)


if __name__ == "__main__":
    main()
