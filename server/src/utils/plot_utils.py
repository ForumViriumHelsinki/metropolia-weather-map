from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    import pandas


def plot_daily_temp_avg(
    avg1: pandas.DataFrame,
    avg2: pandas.DataFrame,
    title: str,
    diff_title: str,
    unit: str,
    plot1_label: str,
    plot2_label: str,
    line1_color="darkorange",
    line2_color="royalblue",
) -> plt:
    """Generates a plot of given daily averages of temperature or humidity

    Args:
        avg1 (pandas.DataFrame): Dataframe of average values
        avg2 (pandas.DataFrame): Dataframe of average values
        title (str): Title for generated graph
        diff_title (str): Legend title for generated differene of average values {diff_title}ero
        unit (str): Unit of the average values
        plot1_label (str): Label for plot 1
        plot2_label (str): Label for plot 2
        line1_color (str, optional): Color for the generated plot line. Defaults to darkorange.
        line2_color (str, optional): Color for the generated plot line. Defaults to royalblue.

    Returns:
        matplotlib.pyplot: Generated graph
    """
    plt.clf()

    avg1.plot(
        kind="line",
        label=plot1_label,
        color=line1_color,
    )
    avg2.plot(
        kind="line",
        label=plot2_label,
        color=line2_color,
    )

    avg_diff = avg1 - avg2

    avg_diff.plot(
        kind="line", label=f"{diff_title}ero", color="red", figsize=(10, 5)
    )

    plt.title(title)
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Päivämäärä")
    plt.ylabel(f"{diff_title} ({unit})")
    plt.legend()
    plt.grid(True)
    return plt


months = [
    "Tammikuu",
    "Helmikuu",
    "Maaliskuu",
    "Huhtikuu",
    "Toukokuu",
    "Kesäkuu",
    "Heinäkuu",
    "Elokuu",
    "Syyskuu",
    "Lokakuu",
    "Marraskuu",
    "Joulukuu",
]


def plot_monthly_diff(
    mean1: pandas.DataFrame,
    mean2: pandas.DataFrame,
    title: str,
    diff_title: str,
    unit: str,
    bar1_label: str,
    bar2_label: str,
) -> plt:
    """Generates a plot graph of monthly average values of temperature or humidity

    Args:
        mean1 (pandas.DataFrame): Dataframe of mean values
        mean2 (pandas.DataFrame): Dataframe of mean values
        title (str): Title of generated graph
        diff_title (str): Legend title for generated difference of mean values
        unit (str): Unit of the mean values
        bar1_label (str): Label for bar 1
        bar2_label (str): Label for bar 2

    Returns:
        matplotlib.pyplot: Generated graph
    """
    plt.clf()

    plt.figure(figsize=(10, 5))

    # Get the union of months present in both datasets
    available_months = sorted(set(mean1.index).union(mean2.index))

    # Align the means to the available months
    mean1 = mean1.reindex(available_months, fill_value=0)
    mean2 = mean2.reindex(available_months, fill_value=0)

    bar_width = 0.4
    months_indices = range(len(available_months))

    plt.bar(
        [x - bar_width / 2 for x in months_indices],
        mean1,
        width=bar_width,
        label=bar1_label,
        color="orange",
        zorder=3,
    )
    plt.bar(
        [x + bar_width / 2 for x in months_indices],
        mean2,
        width=bar_width,
        label=bar2_label,
        color="royalblue",
        zorder=3,
    )

    plt.grid(True, zorder=0)
    plt.title(title)
    plt.legend()
    plt.xlabel("Kuukausi")
    plt.ylabel(f"{diff_title}, ({unit})")
    plt.xticks(
        months_indices, [months[m - 1] for m in available_months], rotation=45
    )
    plt.subplots_adjust(bottom=0.2)

    return plt
