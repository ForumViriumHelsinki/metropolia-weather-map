# ruff: noqa: PLR2004
from datetime import date

from src.utils.get_data_util import filter_date_range
from src.utils.utils import save_graph
from utils.filters import filter_df_by_tag, filter_location_with_tag
from utils.plot_utils import (
    plot_daily_temp_avg,
    plot_monthly_temp_diff,
)
from utils.utils import daily_avg_temp


def temperature_by_tag(
    tag1: str,
    tag2: str,
    graph_type: str,
    location: str = None,
    start_date: str = date,
    end_date: str = date,
    daytime: bool = False,
    nighttime: bool = False,
):
    # Data does not exist before year 2024
    if start_date and start_date.year < 2024:
        raise ValueError("Start date must be in 2024 or later.")

    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date cannot be later than end date.")

    is_year_2024 = False
    is_year_2025 = False

    if start_date and end_date and start_date.year == end_date.year:
        if start_date.year == 2024:
            is_year_2024 = True

        if start_date.year == 2025:
            is_year_2025 = True

    df1 = filter_location_with_tag(
        location,
        tag1,
        get_2024=is_year_2024,
        get_2025=is_year_2025,
        daytime=daytime,
        nighttime=nighttime,
    )

    df1 = filter_date_range(df1, start_date, end_date)

    df2 = filter_location_with_tag(
        location,
        tag2,
        get_2024=is_year_2024,
        get_2025=is_year_2025,
        daytime=daytime,
        nighttime=nighttime,
    )

    df2 = filter_date_range(df2, start_date, end_date)

    # Location of analysis Vallila | Laajasalo | Koivukylä | All
    df1 = filter_df_by_tag(df1, tag1)
    avg1 = daily_avg_temp(df1)

    df2 = filter_df_by_tag(df2, tag2)
    avg2 = daily_avg_temp(df2)

    print(f"Max value of avg_diff: {(avg1 - avg2).max()}")

    match graph_type:
        case "plot":
            return plot_daily_temp_avg(
                df1=avg1,
                df2=avg2,
                title=f"Päivittäinen lämpötila vaihtelu {f'{location}ssa' if location else ''}",
                df1_label=tag1,
                df2_label=tag2,
            )

        case "bar":
            return plot_monthly_temp_diff(
                df1=df1,
                df2=df2,
                title=f"Kuukausittainen lämpötila vaihtelu {f'{location}ssa' if location else ''}",
                df1_label=tag1,
                df2_label=tag2,
            )
        case _:
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
