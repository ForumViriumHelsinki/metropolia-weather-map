import matplotlib.pyplot as plt


def plot_daily_temp_avg(
    df1,
    df2,
    title,
    diff_title,
    unit,
    df1_label,
    df2_label,
    line1_color=None,
    line2_color=None,
):
    plt.clf()

    df1.plot(
        kind="line",
        label=df1_label,
        color=line1_color if line1_color else "darkorange",
    )
    df2.plot(
        kind="line",
        label=df2_label,
        color=line2_color if line2_color else "royalblue",
    )

    avg_diff = df1 - df2

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
    mean1, mean2, title, diff_title, unit, df1_label, df2_label
):
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
        label=df1_label,
        color="orange",
        zorder=3,
    )
    plt.bar(
        [x + bar_width / 2 for x in months_indices],
        mean2,
        width=bar_width,
        label=df2_label,
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
