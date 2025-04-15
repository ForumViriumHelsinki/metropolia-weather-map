import asyncio

import matplotlib.pyplot as plt
from src.utils.filter_tag import filter_location_with_tag
from src.utils.save_graph import save_graph
from src.utils.utils import filter_daytime_data


def avg_daily_temps_sun_shade():
    dfA = filter_location_with_tag("Vallila", "aurinko")
    avg_sun = get_avg_temp(dfA)

    dfV = filter_location_with_tag("Vallila", "varjo")
    avg_shade = get_avg_temp(dfV)

    plt1 = plot_data(
        avg_sun,
        avg_shade,
        "Mäkelänkadun lämpötila auringossa ja varjossa",
        "Aurinko",
        "Varjo",
        "Päivämäärä",
        "°C",
    )
    save_graph("Mäkelänkatu_sun_shade_temp_diff", plt1, folder="vallila")
    # plt1.show()

    plt2 = plot_diff_bar(dfA, dfV, "Mäkelänkadun lämpötilaero auringossa ja varjossa")
    save_graph("Mäkelänkatu_monthly_monthly_temp_diff", plt2, folder="vallila")
    # plt2.show()

    return


def get_avg_temp(df):
    df = filter_daytime_data(df)
    df["date"] = df["time"].dt.date

    return df.groupby("date")["temperature"].mean()


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


def plot_diff_bar(df1, df2, title):
    df1["month"] = df1["time"].dt.month
    df2["month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

    diff = mean1 - mean2

    diff.plot(kind="bar", ylim=(-1, 1), figsize=(10, 5), zorder=3)
    plt.grid(True, zorder=0)
    plt.title(title)
    plt.xlabel("Kuukausi")
    plt.xticks(rotation=0)
    plt.ylabel("Erotus °C")
    return plt


if __name__ == "__main__":
    avg_daily_temps_sun_shade()
