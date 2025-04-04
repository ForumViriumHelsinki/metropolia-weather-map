import numpy as np
import utils
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft
from statsmodels.tsa.seasonal import STL
from matplotlib.widgets import CheckButtons

def load_data():
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
    df.rename(columns={'dev-id': 'sensor'}, inplace=True)
    print (f'{df.columns} load check')
    return df

def plot_raw_humidity(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sensor_lines = {}
    
    for sensor_id, sensor_data in df.groupby('sensor'):
        line, = ax.plot(sensor_data['time'], sensor_data['humidity'], label=f"Sensor {sensor_id}", alpha=0.7)
        sensor_lines[sensor_id] = line
    
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')
    plt.title('Raw Humidity Data Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    legend = plt.legend(title="Sensors", bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.8)
    
    # Separate checkboxes
    fig_checkbox, ax_checkbox = plt.subplots(figsize=(2, 6))
    ax_checkbox.set_xticks([])
    ax_checkbox.set_yticks([])
    ax_checkbox.set_frame_on(False)
    
    labels = list(sensor_lines.keys())
    visibility = [line.get_visible() for line in sensor_lines.values()]
    check = CheckButtons(ax_checkbox, labels, visibility)
    
    def toggle_visibility(label):
        sensor_lines[label].set_visible(not sensor_lines[label].get_visible())
        fig.canvas.draw()
    
    check.on_clicked(toggle_visibility)
    plt.show()
    plt.show()

def plot_fft_analysis(df):
    df_copy = df.copy()
    df_copy.set_index('time', inplace=True)
    grouped = df_copy.groupby('sensor').resample('D').mean().reset_index(level='sensor')
    grouped['humidity'] = grouped['humidity'].rolling(window=7, min_periods=1).mean()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sensor_lines = {}
    
    for sensor_id in grouped['sensor'].unique():
        sensor_df = grouped[grouped['sensor'] == sensor_id]
        humidity_fft = fft(sensor_df['humidity'].dropna())
        freqs = np.fft.fftfreq(len(humidity_fft))
        line, = ax.plot(freqs[:len(freqs)//2], np.abs(humidity_fft[:len(freqs)//2]), label=f'Sensor {sensor_id}')
        sensor_lines[sensor_id] = line
    
    plt.yscale('log')
    plt.title('Fourier Transform of Humidity Data')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.tight_layout()
    
    legend = plt.legend(title="Sensors", loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.8)
    
    # Separate checkboxes
    fig_checkbox, ax_checkbox = plt.subplots(figsize=(2, 6))
    ax_checkbox.set_xticks([])
    ax_checkbox.set_yticks([])
    ax_checkbox.set_frame_on(False)
    
    labels = list(sensor_lines.keys())
    visibility = [line.get_visible() for line in sensor_lines.values()]
    check = CheckButtons(ax_checkbox, labels, visibility)
    
    def toggle_visibility(label):
        sensor_lines[label].set_visible(not sensor_lines[label].get_visible())
        fig.canvas.draw()
    
    check.on_clicked(toggle_visibility)
    plt.show()
    plt.show()

def plot_seasonal_decomposition(df):
    print("Columns at start of seasonal decomposition:", df.dtypes)
    
    if 'time' not in df.columns:
        print("Error: 'time' column missing before STL decomposition!")
        return
    
    df = df.copy()
    df.set_index('time', inplace=True)
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    df = df[['humidity']].resample('h').mean()
    df['humidity'] = df['humidity'].interpolate(method='time')
    df = df.dropna()
    
    if len(df) < 14:
        print("Error: Not enough data points for STL decomposition!")
        return
    
    stl = STL(df['humidity'], seasonal=143)
    result = stl.fit()
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    result.trend.plot(ax=axes[0], title='Trend')
    result.seasonal.plot(ax=axes[1], title='Seasonality')
    result.resid.plot(ax=axes[2], title='Residual')
    plt.show()

def main():
    df = load_data()
    if df is not None:
        plot_raw_humidity(df)
        plot_fft_analysis(df)
        plot_seasonal_decomposition(df)

if __name__ == "__main__":
    main()
