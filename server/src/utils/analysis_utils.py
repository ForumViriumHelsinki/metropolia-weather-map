import os

import matplotlib.pyplot as plt
import pandas as pd
from src.utils.get_data_util import filter_daytime_data
from src.utils.utils import filter_daytime_data


def daily_avg_temp(df):
    df.loc[:, "date"] = df["time"].dt.date

    return df.groupby("date")["temperature"].mean()


def plot_daily_temp_avg(
    df1,
    df2,
    title,
    df1_label,
    df2_label,
    line1_color=None,
    line2_color=None,
):
    plt.clf()
    print(df1.head())

    df1.plot(
        kind="line", label=df1_label, color=line1_color if line1_color else "orange"
    )
    df2.plot(
        kind="line", label=df2_label, color=line2_color if line2_color else "royalblue"
    )

    avg_diff = df1 - df2
    avg_diff.plot(kind="line", label="Lämpötilaero", color="red", figsize=(10, 5))

    plt.title(title)
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Päivämäärä")
    plt.ylabel("Lämpötila (°C)")
    plt.legend()
    plt.grid(True)
    return plt


def plot_monthly_temp_diff(df1, df2, title, ylim=None):
    plt.clf()

    df1 = df1.copy()
    df2 = df2.copy()

    df1.loc[:, "month"] = df1["time"].dt.month
    df2.loc[:, "month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

    diff = mean1 - mean2

    diff.plot(kind="bar", ylim=ylim, figsize=(10, 5), zorder=3)
    plt.grid(True, zorder=0)
    plt.title(title)
    plt.legend()
    plt.xlabel("Kuukausi")
    plt.ylabel("Ero °C")
    return plt
