import matplotlib.pyplot as plt
import pandas as pd

from utils.get_data_util import get_koivukyla, get_laajasalo, get_vallila
from utils.utils import daily_avg_temp, save_graph


def location_temps():
    dfV = get_vallila(daytime=True)
    dfK = get_koivukyla(daytime=True)
    dfL = get_laajasalo(daytime=True)

    graph_plot(dfV, dfK, dfL)
    graph_monthly_avg(dfV, dfK, dfL)


def graph_plot(dfV, dfK, dfL):
    plt.clf()

    dfV = daily_avg_temp(dfV.copy())
    dfK = daily_avg_temp(dfK.copy())
    dfL = daily_avg_temp(dfL.copy())

    dfV.plot(label="Vallila", figsize=(10, 5), color="#2ca02c")
    dfK.plot(label="Koivukylä", color="#ff7f0e")
    dfL.plot(label="Laajasalo", color="#1f77b4")

    plt.title("Temperature difference between locations")
    plt.xlabel("Päivämäärä")
    plt.ylabel("Lämpötila (°C)")
    plt.legend()

    save_graph("all locations temp diffs", plt, "all_locations")


def graph_monthly_avg(dfV, dfK, dfL):
    plt.clf()

    dfV["month"] = dfV.copy()["time"].dt.month
    dfK["month"] = dfK.copy()["time"].dt.month
    dfL["month"] = dfL.copy()["time"].dt.month

    meanV = dfV.groupby("month")["temperature"].mean()
    meanK = dfK.groupby("month")["temperature"].mean()
    meanL = dfL.groupby("month")["temperature"].mean()

    combined = pd.DataFrame(
        {"Vallila": meanV, "Koivukylä": meanK, "Laajasalo": meanL}
    ).reset_index()

    combined.plot(
        x="month",
        kind="bar",
        figsize=(10, 6),
        width=0.8,
        color=["#2ca02c", "#ff7f0e", "#1f77b4"],  # Custom colors
    )

    plt.title("Monthly Average Temperature by Location")
    plt.xlabel("Kuukausi")
    plt.ylabel("Lämpötila (°C)")
    plt.xticks(ticks=range(len(combined["month"])), labels=combined["month"])
    plt.legend(title="Location")

    save_graph("monthly_avg_temperature_grouped", plt, "all_locations")


if __name__ == "__main__":
    location_temps()
