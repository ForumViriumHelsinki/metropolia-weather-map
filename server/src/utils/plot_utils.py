import matplotlib.pyplot as plt


def daily_avg_temp(df):
    df = df.copy()
    df.loc[:, "date"] = df["time"].dt.date
    return df.groupby("date")["temperature"].mean()


def plot_daily_temp_avg(
    df1,
    df2,
    title,
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
        kind="line", label="Lämpötilaero", color="red", figsize=(10, 5)
    )

    plt.title(title)
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel("Päivämäärä")
    plt.ylabel("Lämpötila (°C)")
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


def plot_monthly_temp_diff(df1, df2, title, df1_label, df2_label, ylim=None):
    plt.clf()

    plt.figure(figsize=(10, 5))

    df1 = df1.copy()
    df2 = df2.copy()

    df1.loc[:, "month"] = df1["time"].dt.month
    df2.loc[:, "month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

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
    plt.ylabel("Lämpötila (°C)")
    plt.xticks(
        months_indices, [months[m - 1] for m in available_months], rotation=45
    )
    plt.subplots_adjust(bottom=0.2)

    return plt
