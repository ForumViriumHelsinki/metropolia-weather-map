import utils
import pandas as pd
import matplotlib.pyplot as plt

def load_data(year):
    df = utils.get_csv(year)
    data = utils.separate_sensors(df)
    return data

def filter_sundata(data):
    data_sun = {sensor_id: data[sensor_id] for sensor_id in utils.SENSOR_SUN if sensor_id in data}
    return data_sun

def filter_shadedata(data):
    data_shade = {sensor_id: data[sensor_id] for sensor_id in utils.SENSOR_SHADE if sensor_id in data}
    return data_shade

def ask_user_for_year():
    year = input("Enter year for source data or 'all' for all available: ")
    try:
        year = int(year)
    except ValueError:
        if(year == "" or year == "all"):
            return None
        print("Please enter a valid year.")
        return ask_user_for_year()
    return year

def compute_tempdeltas(sensor_data, resample_period):
    """
    Computes the average temperature change for a given set of sensors,
    resampled to the specified time period ('h' for hourly, 'D' for daily).
    """
    temperature_deltas = []

    for sensor_id, df in sensor_data.items():
        df = df[['time', 'temperature']].copy()
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values(by='time')
        df['temperature_change'] = df['temperature'].diff()

        # Resample to specified time period (hourly or daily)
        df.set_index('time', inplace=True)
        df_resampled = df[['temperature_change']].resample(resample_period).mean()
        temperature_deltas.append(df_resampled)

    if not temperature_deltas:
        return None

    # Merge all sensor data and compute the average humidity change
    merged_df = pd.concat(temperature_deltas).groupby('time').mean()
    return merged_df

def main():
    data = load_data(ask_user_for_year())

    # Filter data using existing functions
    data_sun = filter_sundata(data)
    data_shade = filter_shadedata(data)

    # Compute hourly and daily temperature changes for sun and shade sensors
    sun_tempdelta_hourly = compute_tempdeltas(data_sun, 'h')
    shade_tempdelta_hourly = compute_tempdeltas(data_shade, 'h')

    sun_tempdelta_daily = compute_tempdeltas(data_sun, 'D')
    shade_tempdelta_daily = compute_tempdeltas(data_shade, 'D')

    # Ensure both datasets have the same time range (inner join)
    if sun_tempdelta_hourly is not None and shade_tempdelta_hourly is not None:

        combined_delta_hourly = sun_tempdelta_hourly.join(shade_tempdelta_hourly, lsuffix='_sun', rsuffix='_shade', how='inner')

        # Plot hourly temperature changes for sun and shade sensors
        plt.figure(figsize=(12, 6))
        plt.plot(combined_delta_hourly.index, combined_delta_hourly['temperature_change_sun'], label="Sun Sensors (Hourly)", color='orange')
        plt.plot(combined_delta_hourly.index, combined_delta_hourly['temperature_change_shade'], label="Shade Sensors (Hourly", color='blue')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel('Time')
        plt.ylabel('Avg Hourly Temperature Change (°C)')
        plt.title('Hourly Average Temperature Change (Sun vs Shade)')
        plt.legend()
        plt.grid()
        plt.show()

    if sun_tempdelta_daily is not None and shade_tempdelta_daily is not None:

        combined_delta_daily = sun_tempdelta_daily.join(shade_tempdelta_daily, lsuffix='_sun', rsuffix='_shade', how='inner')

        # Plot daily temperature changes for sun and shade sensors
        plt.figure(figsize=(12, 6))
        plt.plot(combined_delta_daily.index, combined_delta_daily['temperature_change_sun'], label="Sun Sensors (Daily)", color='orange')
        plt.plot(combined_delta_daily.index, combined_delta_daily['temperature_change_shade'], label="Shade Sensors (Daily)", color='blue')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel('Time')
        plt.ylabel('Avg Daily Temperature Change (°C)')
        plt.title('Daily Average Temperature Change (Sun vs Shade)')
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("Not enough data to compute temperature changes.")

if __name__ == "__main__":
    main()
