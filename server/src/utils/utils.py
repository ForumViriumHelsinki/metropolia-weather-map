import os
from typing import TYPE_CHECKING

from utils.get_data_util import get_ids_by_location

if TYPE_CHECKING:
    import pandas


def map_locations():
    """Map sensor IDs to their respective locations."""
    vallila = get_ids_by_location("Vallila")
    print(vallila)
    laajasalo = get_ids_by_location("Laajasalo")
    koivukyla = get_ids_by_location("Koivukyla")
    print(koivukyla)

    return {
        "Vallila": vallila,
        "Koivukylä": koivukyla,
        "Laajasalo": laajasalo,
    }


def save_graph(file_name: str, plt, folder: str = None):
    """Saves generated plot in png and svg format

    Args:
        file_name (_type_): Name which the files will be saved as
        plt (_type_): Plot to save
        folder (_type_, optional): Folder which images will be saved into, if unspecified saves to root folder. Defaults to None.
    """
    base_path = os.path.join(
        os.path.dirname(__file__), "..", "analysis", "graphs"
    )
    if folder:
        base_path = os.path.join(base_path, folder)

    svg_path = os.path.join(base_path, f"{file_name}.svg")
    png_path = os.path.join(base_path, f"{file_name}.png")

    plt.savefig(svg_path)
    plt.savefig(png_path)


def daily_avg_temp(df: pandas.DataFrame) -> pandas.DataFrame:
    df = df.copy()
    df.loc[:, "date"] = df["time"].dt.date
    return df.groupby("date")["temperature"].mean()
