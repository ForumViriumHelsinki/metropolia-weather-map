import asyncio

import matplotlib.pyplot as plt
from src.utils.analysis_utils import daily_avg_temp
from src.utils.filter_tag import filter_df_by_tag
from src.utils.get_data_util import get_all_locations
from src.utils.save_graph import save_graph


def main():
    df = get_all_locations()
    df_meri = filter_df_by_tag(df, "meri")
    avg_meri = daily_avg_temp(df_meri)

    df_manner = filter_df_by_tag(df, "manner")
    avg_manner = daily_avg_temp(df_manner)

    plt = plot_data(
        avg_manner,
        avg_meri,
        "Meri- ja mannerilmasto",
        "Manner",
        "Meri",
        "Päivämäärä",
        "°C",
    )
    save_graph("continental coastal temp diff", plt, "all_locations")
    plt.clf()

    plt2 = plot_diff_bar(df_manner, df_meri)
    save_graph("continental coastal monthly temp diff", plt2, "all_locations")
    plt2.clf()

    return


def plot_data(df1, df2, title, df1_label, df2_label, xlabel, ylabel):
    df1.plot(kind="line", label=df1_label, color="orange")
    df2.plot(kind="line", label=df2_label, color="royalblue")

    avg_diff = df1 - df2
    avg_diff.plot(kind="line", label="Lämpötilaero", color="red", figsize=(10, 5))

    plt.title(title)
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    return plt


def plot_diff_bar(df1, df2):
    df1["month"] = df1["time"].dt.month
    df2["month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

    diff = mean1 - mean2

    diff.plot(kind="bar", ylim=(-1, 1), figsize=(10, 5), zorder=3)
    plt.grid(True, zorder=0)
    plt.title("Meri- ja mannerilmasto lämpötilaero")
    plt.xlabel("Kuukausi")
    plt.xticks(rotation=0)
    plt.legend()
    plt.ylabel("°C")

    return plt


if __name__ == "__main__":
    main()
