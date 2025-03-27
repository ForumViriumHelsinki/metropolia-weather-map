import utils
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = utils.get_csv()
    print(f"Found {len(df)} CSV files.")  # Debugging output
    data_frames = []
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%f%z', errors='coerce')
    df.rename(columns={'dev-id': 'sensor'}, inplace=True)  # Rename sensor column
    data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

def compute_monthly_avgs(df):
    df["month"] = pd.to_datetime(df["time"]).dt.to_period("M")
    monthly_avgs = df.groupby(['month', 'sensor'])[["temperature", "humidity"]].mean().reset_index()
    return monthly_avgs

def plot_humidity_trends(monthly_avgs):
    pivot_df = monthly_avgs.pivot(index='month', columns='sensor', values='humidity')
    pivot_df.plot(kind='bar', figsize=(20, 6), width=0.8)
    
    plt.xlabel('Month')
    plt.ylabel('Average Humidity (%)')
    plt.title('Monthly Average Humidity Trends')
    plt.xticks(rotation=45)
    plt.legend(title='Sensor', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y')
    plt.show()

def plot_temp_vs_humidity(df):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=df['temperature'], y=df['humidity'], alpha=0.5)
    
    correlation = df[['temperature', 'humidity']].corr().iloc[0, 1]
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.title("Temperature vs Humidity")
    plt.legend()
    plt.grid()
    plt.show()

    print(f"correlation coefficient: {correlation:}")

def main():
    df = load_data()
    monthly_avgs = compute_monthly_avgs(df)
    plot_humidity_trends(monthly_avgs)
    plot_temp_vs_humidity(monthly_avgs)

if __name__ == "__main__":
    main()
    
