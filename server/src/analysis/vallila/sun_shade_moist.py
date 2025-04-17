import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from src.utils.analysis_utils import filter_daytime_data
from src.utils.filter_tag import filter_location_with_tag
from src.utils.save_graph import save_graph


def avg_moisture(df):
    df["date"] = df["time"].dt.date
    return df.groupby("date")["humidity"].mean()


def avg_daily_temps_sun_moisture():
    dfA = filter_location_with_tag("Vallila", "aurinko")
    dfA = filter_daytime_data(dfA)
    moistureA = avg_moisture(dfA)

    dfV = filter_location_with_tag("Vallila", "varjo")
    dfV = filter_daytime_data(dfV)
    moistureV = avg_moisture(dfV)

    plt1 = plot_hum_temp_avg(moistureA, moistureV)
    save_graph("vallila_sun_shade_moisture_diff", plt1, folder="vallila")

    plt2 = graph_monthly_avg(dfA, dfV)
    save_graph("vallila_sun_shade_monthly_moisture_diff", plt2, folder="vallila")

    return


def plot_hum_temp_avg(
    df1,
    df2,
):
    plt.clf()

    df2.plot(kind="line", label="Varjo", color="#1f77b4")
    df1.plot(kind="line", label="Aurinko", figsize=(10, 5), color="#ff7f0e")

    avg_diff = df1 - df2
    avg_diff.plot(kind="line", label="Lämpötilaero", color="red", figsize=(10, 5))

    plt.title("Mäkelänkadun ilmankosteus auringossa ja varjossa")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Päivämäärä")
    plt.ylabel("Ilmankosteus (%)")
    plt.legend()
    plt.grid(True)

    return plt


def graph_monthly_avg(dfA, dfV):
    plt.clf()

    dfA["month"] = dfA.copy()["time"].dt.month
    dfV["month"] = dfV.copy()["time"].dt.month

    meanA = dfA.groupby("month")["humidity"].mean()
    meanV = dfV.groupby("month")["humidity"].mean()

    combined = pd.DataFrame({"Aurinko": meanA, "Varjo": meanV}).reset_index()

    combined.plot(
        x="month",
        kind="bar",
        figsize=(10, 6),
        width=0.8,
        color=["#ff7f0e", "#1f77b4"],
    )

    plt.title("Kuukausittainen ilmankosteuden keskiarvo")
    plt.xlabel("Kuukausi")
    plt.ylabel("Ilmankosteus (°%)")
    plt.xticks(ticks=range(len(combined["month"])), labels=combined["month"])
    plt.legend(title="Location")

    save_graph("monthly_avg_temperature_grouped", plt, "all_locations")

    return plt


if __name__ == "__main__":
    avg_daily_temps_sun_moisture()
