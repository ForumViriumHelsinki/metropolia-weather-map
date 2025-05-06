# ruff: noqa: PLR2004
from datetime import date

from utils.filters import tag_filter
from utils.get_data_util import (
    filter_date_range,
    get_all_locations,
    get_koivukyla,
    get_laajasalo,
    get_vallila,
)
from utils.plot_utils import (
    plot_daily_temp_avg,
    plot_monthly_diff,
)
from utils.utils import save_graph


def temperature_by_tag(
    tag1: str,
    tag2: str,
    graph_type: str,
    location: str = None,
    start_date: date = None,
    end_date: date = None,
    daytime: bool = False,
    nighttime: bool = False,
    analysis_variable: str = "temperature",
):
    if start_date and start_date.year < 2024:
        raise ValueError("Start date must be in 2024 or later.")
    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date cannot be later than end date.")

    is_2024 = (
        start_date
        and end_date
        and start_date.year == end_date.year
        and start_date.year == 2024
    )

    is_2025 = (
        start_date
        and end_date
        and start_date.year == end_date.year
        and start_date.year == 2025
    )

    def prepare_data(df, tag):
        df = tag_filter(df, tag)
        df = filter_date_range(df, start_date, end_date)

        if graph_type == "plot":
            return daily_avg(df, analysis_variable)

        return monthly_avg_mean(df, analysis_variable)

    match location:
        case "Vallila":
            df = get_vallila(is_2024, is_2025, daytime, nighttime)
        case "Koivukyla":
            df = get_koivukyla(is_2024, is_2025, daytime, nighttime)
        case "Laajasalo":
            df = get_laajasalo(is_2024, is_2025, daytime, nighttime)
        case _:
            df = get_all_locations(is_2024, is_2025, daytime, nighttime)

    df = filter_date_range(df, start_date, end_date)

    var1 = prepare_data(df, tag1)
    var2 = prepare_data(df, tag2)

    print(f"Max value of avg_diff: {(var1 - var2).max()}")

    title_detail = "lämpötila"
    unit = "°C"

    if analysis_variable == "humidity":
        title_detail = "ilmankosteus"
        unit = "%"

    if graph_type == "plot":
        return plot_daily_temp_avg(
            df1=var1,
            df2=var2,
            title=f"Päivittäinen {title_detail} vaihtelu {f'{location}ssa' if location else ''}",
            diff_title=title_detail,
            unit=unit,
            df1_label=tag1,
            df2_label=tag2,
        )

    if graph_type == "bar":
        return plot_monthly_diff(
            mean1=var1,
            mean2=var2,
            title=f"Kuukausittainen {title_detail} vaihtelu {f'{location}ssa' if location else ''}",
            diff_title=title_detail,
            unit=unit,
            df1_label=tag1,
            df2_label=tag2,
        )

    raise ValueError("Invalid or undefined graph type")


def daily_avg(df, analysis_variable):
    df = df.copy()
    df.loc[:, "date"] = df["time"].dt.date
    return df.groupby("date")[analysis_variable].mean()


def monthly_avg_mean(df, analysis_variable):
    df = df.copy()
    df.loc[:, "month"] = df["time"].dt.month
    return df.groupby("month")[analysis_variable].mean()


if __name__ == "__main__":
    graph = temperature_by_tag(
        tag1="aurinko",
        tag2="varjo",
        graph_type="plot",
        start_date=None,
        end_date=None,
        daytime=False,
        nighttime=False,
    )
    save_graph(file_name="tag_general", plt=graph, folder="test")
