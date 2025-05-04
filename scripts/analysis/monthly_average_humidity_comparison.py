import utils
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    df = utils.get_csv()
    print(f"Found {len(df)} CSV files.")  # Debugging output
    data_frames = []
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces     
    if 'time' not in df.columns:
            raise ValueError(f"Column 'time' not found in {df}. Check CSV formatting.")
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%f%z', errors='coerce')
    df.rename(columns={'dev-id': 'sensor'}, inplace=True)  # Rename sensor column
    data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

def compute_monthly_avg_humidity(df):
    df["month"] = pd.to_datetime(df["time"]).dt.to_period("M")
    monthly_avg_humidity = df.groupby(['month', 'sensor'])["humidity"].mean().reset_index()
    return monthly_avg_humidity

def plot_monthly_avg_humidity(mountly_avg_humidity):
    plt.figure(figsize=(12, 6))
    for sensor in mountly_avg_humidity["sensor"].unique():
        sensor_data = mountly_avg_humidity[mountly_avg_humidity["sensor"] == sensor]
        plt.plot(sensor_data['month'].astype(str), sensor_data['humidity'], label=sensor)
    
    plt.xlabel("Month")
    plt.ylabel("Average Humidity (%)")
    plt.title("Monthly Average Humidity Comparison")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()

def plot_humidity_trends(monthly_avg):
    pivot_df = monthly_avg.pivot(index='month', columns='sensor', values='humidity')
    pivot_df.plot(kind='bar', figsize=(20, 6), width=0.8)
    
    plt.xlabel('Month')
    plt.ylabel('Average Humidity (%)')
    plt.title('Monthly Average Humidity Trends')
    plt.xticks(rotation=45)
    plt.legend(title='Sensor', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y')
    plt.show()

def main():
    df = load_data()
    monthly_avg = compute_monthly_avg_humidity(df)
    plot_monthly_avg_humidity(monthly_avg)
    plot_humidity_trends(monthly_avg)

if __name__ == "__main__":
    main()


