import numpy as np
import utils
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft
from statsmodels.tsa.seasonal import STL

def load_data():
    df = utils.get_csv()  # Already a DataFrame, no need for concat

    # Debug: Check initial DataFrame structure
    print("Initial DataFrame Columns:", df.columns)

    if 'time' not in df.columns:
        print("Error: 'time' column is missing after loading data!")
        return None  # Exit early if something is wrong
    
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # Ensure datetime format
    df.rename(columns={'dev-id': 'sensor'}, inplace=True)
    print (f'{df.columns} load check')
    return df

def plot_fft_analysis(df):
    df_copy = df.copy()  # Create a copy of the DataFrame for safety
    print (f'{df_copy.columns} fft check') # Debugging output
    print(f'{df_copy.info()} fft info 1')# Check if 'time' exists and is a datetime object
    df_copy.set_index('time', inplace=True)
    print(f'{df_copy.info()} fft info 2')  # Confirm it's now the index

    grouped = df_copy.groupby('sensor').resample('D').mean().reset_index(level='sensor')

    plt.figure(figsize=(8, 6))
    
    for sensor_id in grouped['sensor'].unique():
        sensor_df = grouped[grouped['sensor'] == sensor_id]
        humidity_fft = fft(sensor_df['humidity'].dropna())
        freqs = np.fft.fftfreq(len(humidity_fft))

        plt.plot(freqs[:len(freqs)//2], np.abs(humidity_fft[:len(freqs)//2]), label=f'Sensor {sensor_id}')
    
    plt.title('Fourier Transform of Humidity Data')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    plt.legend(title="Sensors", loc='upper right')  # Move legend to upper right
    plt.grid(True)
    plt.show()

def plot_seasonal_decomposition(df):
    print("Columns at start of seasonal decomposition:", df.dtypes)  # Debugging
    
    if 'time' not in df.columns:
        print("Error: 'time' column missing before STL decomposition!")
        return
    
    df = df.copy()  # Avoid modifying the original DataFrame
    df.set_index('time', inplace=True)

    # Convert numeric columns explicitly
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

    # Select only numeric columns for resampling (avoid sensor ID issues)
    numeric_cols = ['humidity']  # Add 'temperature' if needed
    df = df[numeric_cols].resample('H').mean()  # Change 'H' to 'D' for daily if needed

    # Fill missing values using interpolation
    df['humidity'] = df['humidity'].interpolate(method='time')

    # Drop NaNs that may still be present
    df = df.dropna()

    # Ensure enough data points before running STL
    if len(df) < 14:  # Needs at least 2 cycles (e.g., 14 days for weekly data)
        print("Error: Not enough data points for STL decomposition!")
        return

    stl = STL(df['humidity'], seasonal=143)  # 24 = One day cycle (Hourly data)
    result = stl.fit()
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    result.trend.plot(ax=axes[0], title='Trend')
    result.seasonal.plot(ax=axes[1], title='Seasonality')
    result.resid.plot(ax=axes[2], title='Residual')
    plt.show()



def main():
    df = load_data()
    print (f'{df.columns} main check') # Debugging output
    plot_fft_analysis(df)
    plot_seasonal_decomposition(df)

if __name__ == "__main__":
    main()