from utils.filters import filter_location_with_tag
from utils.plot_utils import (
    filter_daytime_data,
    plot_daily_temp_avg,
    plot_monthly_diff,
)
from utils.utils import daily_avg_temp, save_graph


def area_daily_temp_diff():
    dfGreen = filter_location_with_tag("Vallila", "viheralue")
    dfGreen = filter_daytime_data(dfGreen)

    dfGray = filter_location_with_tag("Vallila", "harmaa-alue")
    dfGray = filter_daytime_data(dfGray)

    avg_green = daily_avg_temp(dfGreen)
    avg_gray = daily_avg_temp(dfGray)

    plt1 = plot_daily_temp_avg(
        avg_green,
        avg_gray,
        "Harmaa- ja viheralueiden lämpötilaero",
        "Viheralue",
        "Harmaa-alue",
        "Päivämäärä",
        "°C",
        line1_color="orange",
        line2_color="royalblue",
    )
    save_graph("green and gray space avg temp diff", plt1, folder="vallila")

    plt2 = plot_monthly_diff(
        dfGreen, dfGray, "Harmaa- ja viheralueiden lämpötilaero", ylim=(0, -1)
    )
    save_graph(
        "green and grayspace avg monthly temp diff", plt2, folder="vallila"
    )


if __name__ == "__main__":
    area_daily_temp_diff()
