import asyncio

import matplotlib.pyplot as plt
from analysis.tag_analysis import get_avg_temp, plot_data
from utils.filter_tag import filter_df_by_tag
from utils.get_data_util import get_all_locations


async def main():
    df = await get_all_locations()
    df_meri = await filter_df_by_tag(df, "meri")
    avg_meri = get_avg_temp(df_meri)

    df_manner = await filter_df_by_tag(df, "manner")
    avg_manner = get_avg_temp(df_manner)

    plot_data(avg_meri, avg_manner)

    return


if __name__ == "__main__":
    asyncio.run(main())
