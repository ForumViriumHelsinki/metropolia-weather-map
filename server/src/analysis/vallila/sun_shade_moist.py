import asyncio

import matplotlib.pyplot as plt
from src.utils.analysis_utils import (
    daily_avg_temp,
    filter_daytime_data,
    plot_daily_temp_avg,
    plot_monthly_temp_diff,
)
from src.utils.filter_tag import filter_location_with_tag
from src.utils.save_graph import save_graph


def avg_moisture(df):
    df["date"] = df["time"].dt.date
    df.groupby("date")["humidity"].mean()
    return df


def avg_daily_temps_sun_moisture():
    dfA = filter_location_with_tag("Vallila", "aurinko")
    dfA = filter_daytime_data(dfA)
    moistureA = avg_moisture(dfA)

    dfV = filter_location_with_tag("Vallila", "varjo")
    dfV = filter_daytime_data(dfV)
    moistureV = avg_moisture(dfV)

    plt1 = plot_daily_temp_avg(
        moistureA,
        moistureV,
        title="Mäkelänkadun lämpötila auringossa ja varjossa",
        df1_label="Aurinko",
        df2_label="Varjo",
        xlabel="Päivämäärä",
        ylabel="Ilmankosteus (%)",
        label="Ilmankosteus",
    )
    save_graph("vallila_sun_shade_moisture_diff", plt1, folder="vallila")

    plt2 = plot_monthly_temp_diff(
        dfA, dfV, "Mäkelänkadun ilmankosteus auringossa ja varjossa", ylim=(0, 1)
    )
    save_graph("vallila_sun_shade_monthly_moisture_diff", plt2, folder="vallila")

    return


if __name__ == "__main__":
    avg_daily_temps_sun_moisture()
