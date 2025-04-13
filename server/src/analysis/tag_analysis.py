import asyncio

import matplotlib.pyplot as plt
from utils.filter_tag import filter_location_with_tag
from utils.utils import filter_daytime_data


# ================== UTILS ==================
def get_avg_temp(df):
    df = filter_daytime_data(df)
    df["date"] = df["time"].dt.date

    return df.groupby("date")["temperature"].mean()


def plot_data(df1, df2):
    df1.plot(kind="line", title="Average Temperature Per Day", color="orange")
    df2.plot(kind="line", title="Average Temperature Per Day", color="royalblue")

    avg_diff = df1 - df2
    avg_diff.plot(kind="line", title="Average Temperature Per Day", color="red")

    plt.xlabel("Date")
    plt.ylabel("Average Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return


# ======================================================


async def avg_daily_temps_sun_shade():
    dfA = await filter_location_with_tag("Mäkelänkatu", "aurinko")
    avg_sun = get_avg_temp(dfA)

    dfV = await filter_location_with_tag("Mäkelänkatu", "varjo")
    avg_shade = get_avg_temp(dfV)

    plot_data(avg_sun, avg_shade)

    return


async def area_daily_temp_diff():
    dfGreen = await filter_location_with_tag("Mäkelänkatu", "viheralue")
    dfGray = await filter_location_with_tag("Mäkelänkatu", "harmaa-alue")

    avg_green = get_avg_temp(dfGreen)
    avg_gray = get_avg_temp(dfGray)

    plot_data(avg_green, avg_gray)

    return


# async def coastal_continental_temp_diff():
#     dfCoastal = await filter_location_with_tag(L)

#     return


async def test_func():
    await avg_daily_temps_sun_shade()
    await area_daily_temp_diff()


if __name__ == "__main__":
    asyncio.run(test_func())
    # asyncio.run(avg_daily_temps_sun_shade())
    # asyncio.run(area_daily_temp_diff())
    # print(asd)
