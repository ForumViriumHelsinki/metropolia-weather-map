import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from analysis.save_graph import save_graph
from utils.filter_tag import filter_df_by_tag
from utils.get_data_util import get_all_locations


async def main():
    df = await get_all_locations()
    df_meri = await filter_df_by_tag(df, "meri")
    df_meri["month"] = df_meri["time"].dt.month
    avg_temp_month_meri = df_meri.groupby("month")["temperature"].mean()

    df_manner = await filter_df_by_tag(df, "manner")
    df_manner["month"] = df_manner["time"].dt.month
    avg_temp_month_manner = df_manner.groupby("month")["temperature"].mean()

    # merged = pd.concat([avg_temp_month_manner, avg_temp_month_meri])
    merged = pd.DataFrame(
        {"Meri": avg_temp_month_meri, "Manner": avg_temp_month_manner}
    )

    diff = avg_temp_month_meri - avg_temp_month_manner

    print(diff)

    merged.plot(kind="bar")
    plt.title("Average Monthly Temperature: Meri vs Manner")
    plt.xlabel("Month")
    plt.ylabel("Temperature")
    save_graph("average_monthly_temperature", plt)
    plt.show()

    # diff.plot(kind="bar")
    # plt.show()

    return


if __name__ == "__main__":
    asyncio.run(main())
