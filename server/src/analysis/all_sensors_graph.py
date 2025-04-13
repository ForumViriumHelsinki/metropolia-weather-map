import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from analysis.tag_analysis import get_avg_temp, plot_data
from utils.filter_tag import filter_df_by_tag
from utils.get_data_util import (
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_makelankatu,
)


async def main():
    df = await get_koivukyla()

    # grouped = df.groupby("dev-id").agg(list).to_dict("asd")
    dfs = [g for _, g in df.groupby("dev-id")]

    print(dfs[0].head())

    for df in dfs:
        sensor_id = df.iloc[0]["dev-id"]
        plt.plot(df["time"], df["temperature"], label=sensor_id)
        # df_id = df["dev-id"].iloc[0]

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Over Time by Device")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    asyncio.run(main())
