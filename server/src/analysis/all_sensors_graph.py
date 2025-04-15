import matplotlib.pyplot as plt
from src.utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)
from src.utils.save_graph import save_graph


def main():
    df = get_all_locations(get_2025=True)

    # grouped = df.groupby("dev-id").agg(list).to_dict("asd")
    dfs = [g for _, g in df.groupby("dev-id")]

    print(dfs[0].head())

    plt.figure(figsize=(15, 5))
    for df in dfs:
        sensor_id = df.iloc[0]["dev-id"]
        plt.plot(df["time"], df["temperature"], label=sensor_id)
        # df_id = df["dev-id"].iloc[0]

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Over Time by Device")
    plt.legend()
    plt.grid(True)
    save_graph("test plot", plt, "test")

    return


if __name__ == "__main__":
    main()
