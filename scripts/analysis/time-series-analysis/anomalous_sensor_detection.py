import matplotlib.pyplot as plt
import pandas as pd


def detect_sensors_with_median_deviation(
    df, threshold=3.0, min_ratio=0.3, time_round="1h"
):
    """
    Detects sensors with anomalies based on the deviation from the median temperature.
    """
    print("[INFO] Detecting sensors with median deviation anomalies...")

    df = df.copy()
    df["week"] = df["time"].dt.tz_localize(None).dt.to_period("W").astype(str)
    df["rounded_time"] = df["time"].dt.floor(time_round)

    district_medians = (
        df.groupby(["district", "rounded_time"])["temperature"]
        .median()
        .reset_index(name="district_median")
    )
    df = pd.merge(df, district_medians, on=["district", "rounded_time"], how="left")

    df["deviation"] = (df["temperature"] - df["district_median"]).abs()
    df["is_anomalous"] = df["deviation"] > threshold

    anomalies = df.groupby(["week", "device_id"])["is_anomalous"].mean().reset_index()
    anomalies = anomalies[anomalies["is_anomalous"] > min_ratio]

    result = anomalies.groupby("week")["device_id"].apply(list).to_dict()

    for week, devices in result.items():
        print(f"\nWeek {week} — {len(devices)} sensors with median deviation:")
        for device in devices:
            print(f"  {device}")

    return result


def plot_anomalous_temperature_by_area(df, anomalies):
    """
    Plots the temperature data for sensors with anomalies.
    """
    print("[INFO] Generating anomaly plots...")

    sensor_weeks = {}
    for week, sensor_ids in anomalies.items():
        for sensor_id in sensor_ids:
            sensor_weeks.setdefault(sensor_id, []).append(week)

    district_sensors = {}
    for sensor_id in sensor_weeks:
        district = df[df["device_id"] == sensor_id]["district"].iloc[0]
        district_sensors.setdefault(district, []).append(sensor_id)

    district_order = df["district"].drop_duplicates().tolist()

    for district in district_order:
        sensors = district_sensors.get(district, [])
        if not sensors:
            continue

        print(
            f"[INFO] Plotting district: {district} ({len(sensors)} anomalous sensors)"
        )
        df_district = df[df["district"] == district]

        plt.figure(figsize=(14, 6))

        sensor_anomalies = {}
        for sensor_id in sensors:
            periods = []
            for week in sensor_weeks[sensor_id]:
                start = pd.to_datetime(week.split("/")[0]).tz_localize("UTC")
                end = pd.to_datetime(week.split("/")[1]).tz_localize(
                    "UTC"
                ) + pd.Timedelta(days=1)
                periods.append((start, end))
            sensor_anomalies[sensor_id] = periods

        shown_ids = set()

        for dev_id, data in df_district.groupby("device_id"):
            data = data.sort_values("time")
            if dev_id not in sensors:
                plt.plot(
                    data["time"],
                    data["temperature"],
                    color="gray",
                    alpha=0.4,
                    linewidth=1,
                )
            else:
                mask = pd.Series(False, index=data.index)
                for start, end in sensor_anomalies[dev_id]:
                    mask |= (data["time"] >= start) & (data["time"] < end)

                temp_anomalous = data["temperature"].where(mask)
                temp_normal = data["temperature"].where(~mask)

                plt.plot(
                    data["time"], temp_normal, color="gray", alpha=0.4, linewidth=1
                )
                label = dev_id if dev_id not in shown_ids else None
                plt.plot(
                    data["time"],
                    temp_anomalous,
                    color="red",
                    linewidth=1.5,
                    label=label,
                )
                shown_ids.add(dev_id)

        if shown_ids:
            plt.legend(title="Anomalous sensors", fontsize="small")

        plt.title(f"Temperature — Sensors in {district}")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    from data_preprocessing import prepare_data

    df = prepare_data("2024-01-01", "2024-10-30", ["Vallila", "Koivukylä", "Laajasalo"])
    anomalies_median = detect_sensors_with_median_deviation(df)
    plot_anomalous_temperature_by_area(df, anomalies_median)
