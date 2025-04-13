import asyncio

import matplotlib.pyplot as plt
from analysis.save_graph import save_graph
from analysis.tag_analysis import get_avg_temp, plot_data
from utils.filter_tag import filter_df_by_tag
from utils.get_data_util import get_all_locations


def plot_diff_bar(df1, df2):
    df1["month"] = df1["time"].dt.month
    df2["month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

    diff = mean1 - mean2
    # Drop month for missing data
    diff = diff.drop(index=5)

    # print(diff)
    # return
    diff.plot(kind="bar", ylim=(-1, 1), figsize=(10, 5), zorder=3)
    plt.grid(True, zorder=0)
    plt.title("Meri- ja mannerilmasto lämpötilaero")
    plt.xlabel("Kuukausi")
    plt.xticks(rotation=0)
    plt.ylabel("Erotus °C")
    return plt


async def main():
    df = await get_all_locations()
    df_meri = await filter_df_by_tag(df, "meri")
    avg_meri = get_avg_temp(df_meri)

    df_manner = await filter_df_by_tag(df, "manner")
    avg_manner = get_avg_temp(df_manner)

    plt = plot_diff_bar(df_manner, df_meri)
    save_graph("meri_manner_kk_ero", plt)
    # plt.show()

    # print(df_meri.head())

    # plt = plot_data(
    #     avg_manner,
    #     avg_meri,
    #     "Meri- ja mannerilmasto",
    #     "Manner",
    #     "Meri",
    #     "Päivämäärä",
    #     "°C",
    # )
    # plt.show()

    # plt2 = plot_diff_bar(df_manner, df_meri, "Meri- ja mannerilmasto lämpötilaero")
    # plt2.show()

    # save_graph("Meri- ja mannerilmaston lämpötilaero", plt)

    return


if __name__ == "__main__":
    asyncio.run(main())
