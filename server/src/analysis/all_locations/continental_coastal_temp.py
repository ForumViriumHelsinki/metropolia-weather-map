from src.utils.filter_tag import filter_df_by_tag
from src.utils.get_data_util import get_all_locations
from src.utils.utils import save_graph
from utils.plot_utils import (
    plot_daily_temp_avg,
    plot_monthly_temp_diff,
)
from utils.utils import daily_avg_temp


def main():
    df = get_all_locations()
    df_meri = filter_df_by_tag(df, "meri")
    avg_meri = daily_avg_temp(df_meri)

    df_manner = filter_df_by_tag(df, "manner")
    avg_manner = daily_avg_temp(df_manner)

    plt = plot_daily_temp_avg(
        avg_manner,
        avg_meri,
        "Meri- ja mannerilmasto",
        "Manner",
        "Meri",
        "Päivämäärä",
        "°C",
    )
    save_graph("continental coastal temp diff", plt, "all_locations")
    plt.clf()

    plt2 = plot_monthly_temp_diff(
        df_manner, df_meri, "Meri- ja mannerilmaseto lämpötilaero", (-1, 1)
    )
    save_graph("continental coastal monthly temp diff", plt2, "all_locations")
    plt2.clf()


if __name__ == "__main__":
    main()
