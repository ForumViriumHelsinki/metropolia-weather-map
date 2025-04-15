import matplotlib.pyplot as plt
from src.utils.filter_tag import filter_location_with_tag
from src.utils.save_graph import save_graph
from src.utils.utils import filter_daytime_data


def area_daily_temp_diff():
    dfGreen = filter_location_with_tag("Vallila", "viheralue")
    dfGray = filter_location_with_tag("Vallila", "harmaa-alue")

    avg_green = get_avg_temp(dfGreen)
    avg_gray = get_avg_temp(dfGray)

    plt1 = plot_data(
        avg_green,
        avg_gray,
        "Harmaa- ja viheralueiden lämpötilaero",
        "Viheralue",
        "Harmaa-alue",
        "Päivämäärä",
        "°C",
    )
    # plt1.show()
    save_graph("green and gray space avg temp diff", plt1, folder="vallila")

    plt2 = plot_area_diff_bar(dfGreen, dfGray, "Harmaa- ja viheralueiden lämpötilaero")
    save_graph("green and grayspace avg monthly temp diff", plt2, folder="vallila")
    # plt2.show()

    return


def plot_data(df1, df2, title, df1_label, df2_label, xlabel, ylabel):
    df1.plot(kind="line", label=df1_label, color="orange")
    df2.plot(kind="line", label=df2_label, color="royalblue")

    avg_diff = df1 - df2
    avg_diff.plot(kind="line", label="Lämpötilaero", color="red", figsize=(10, 5))

    plt.title(title)
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt


def get_avg_temp(df):
    df = filter_daytime_data(df)
    df["date"] = df["time"].dt.date

    return df.groupby("date")["temperature"].mean()


def plot_area_diff_bar(df1, df2, title):
    df1["month"] = df1["time"].dt.month
    df2["month"] = df2["time"].dt.month

    mean1 = df1.groupby("month")["temperature"].mean()
    mean2 = df2.groupby("month")["temperature"].mean()

    diff = mean1 - mean2

    diff.plot(kind="bar", ylim=(0, -1), figsize=(10, 5))
    plt.title(title)
    plt.xlabel("Kuukausi")
    plt.ylabel("Erotus °C")
    return plt


if __name__ == "__main__":
    area_daily_temp_diff()
