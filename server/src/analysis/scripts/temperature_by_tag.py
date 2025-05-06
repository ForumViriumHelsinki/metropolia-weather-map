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
    plot_monthly_temp_diff,
)
from utils.utils import daily_avg_temp, save_graph


def temperature_by_tag(
    tag1: str,
    tag2: str,
    graph_type: str,
    location: str = None,
    start_date: date = None,
    end_date: date = None,
    daytime: bool = False,
    nighttime: bool = False,
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

    print(is_2024, is_2025)

    def prepare_data(df, tag):
        df = tag_filter(df, tag)
        df = filter_date_range(df, start_date, end_date)
        return daily_avg_temp(df), df

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

    avg1, df1 = prepare_data(df, tag1)
    avg2, df2 = prepare_data(df, tag2)

    print(f"Max value of avg_diff: {(avg1 - avg2).max()}")

    if graph_type == "plot":
        return plot_daily_temp_avg(
            df1=avg1,
            df2=avg2,
            title=f"Päivittäinen lämpötila vaihtelu {f'{location}ssa' if location else ''}",
            df1_label=tag1,
            df2_label=tag2,
        )

    if graph_type == "bar":
        return plot_monthly_temp_diff(
            df1=df1,
            df2=df2,
            title=f"Kuukausittainen lämpötila vaihtelu {f'{location}ssa' if location else ''}",
            df1_label=tag1,
            df2_label=tag2,
        )

    raise ValueError("Invalid or undefined graph type")


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
