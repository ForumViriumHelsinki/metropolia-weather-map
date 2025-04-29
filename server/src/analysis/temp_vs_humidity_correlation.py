import asyncio
import io
from matplotlib.widgets import CheckButtons
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..utils import get_data_util

'''def load_data():
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
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%f%z', errors='coerce')
    df.rename(columns={'dev-id': 'sensor'}, inplace=True)  # Rename sensor column
    return df
'''
def compute_monthly_avgs(df):
    df["month"] = pd.to_datetime(df["time"]).dt.to_period("M")
    monthly_avgs = df.groupby(['month', 'dev-id'])[["temperature", "humidity"]].mean().reset_index()
    return monthly_avgs


def plot_humidity_trends():
    monthly_avgs = compute_monthly_avgs(get_data_util.get_all_locations())
    fig = plt.figure(figsize=(10, 5))
    gs = plt.GridSpec(1, 2, width_ratios=[4, 1])
    ax = fig.add_subplot(gs[0])
    ax_cb = fig.add_subplot(gs[1])

    sensor_lines = {}

    for sensor_id, sensor_data in monthly_avgs.groupby('dev-id'):
        line, = ax.plot(sensor_data['month'].dt.to_timestamp(), sensor_data['humidity'], label=sensor_id, alpha=0.7)
        sensor_lines[sensor_id] = line
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Humidity (%)')
    ax.set_title('Monthly Average Humidity Data Over Time')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    ax.legend(title="Sensors", bbox_to_anchor=(1, 1))

    ax_cb.set_xticks([])
    ax_cb.set_yticks([])
    ax_cb.set_frame_on(False)

    '''vallila = get_data_util.get_ids_by_location("Vallila")
    laajasalo = get_data_util.get_ids_by_location("Laajasalo")
    koivukyla = get_data_util.get_ids_by_location("Koivukylä")
    location_map = {
        'Vallila': vallila,
        'Koivukylä': koivukyla,
        'Laajasalo': laajasalo,
    }

    all_sensor_ids = list(sensor_lines.keys())
    location_labels = list(location_map.keys())
    all_labels = location_labels + all_sensor_ids
    visibility = [True] * len(all_labels)

    check = CheckButtons(ax_cb, all_labels, visibility)
    label_to_index = {label: i for i, label in enumerate(all_labels)}

    def toggle(label):
        status = check.get_status()
        if label in sensor_lines:
            sensor_lines[label].set_visible(status[label_to_index[label]])
        elif label in location_map:
            sensors = location_map[label]
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
    plt.show()'''

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf

def plot_temp_vs_humidity():
    print ("plot_temp_vs_humidity")
    df = compute_monthly_avgs(get_data_util.get_all_locations())
    print (df.columns)
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=df['temperature'], y=df['humidity'], alpha=0.5)
    
    correlation = df[['temperature', 'humidity']].corr().iloc[0, 1]
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.title(f"correlation coefficient: {correlation:}")
    plt.legend()
    plt.grid()
    #plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    print(f"correlation coefficient: {correlation:}")
    return buf
def main():
    df = get_data_util.get_all_locations()
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    monthly_avgs = compute_monthly_avgs(df)
    plot_humidity_trends(monthly_avgs)
    plot_temp_vs_humidity()

if __name__ == "__main__":
    asyncio.run(main())
    
