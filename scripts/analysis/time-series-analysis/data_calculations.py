
def compute_daily_median_temperature(df):
    """
    Calculates the daily median temperature for each district.
    """
    df["date"] = df["time"].dt.date
    daily_median = (
        df.groupby(["district", "date"])["temperature"]
        .median()
        .reset_index()
    )
    return daily_median


def compute_day_night_difference(df):
    """
    Calculates the difference between day and night median temperature
    for each district and date. Day = 6–21, Night = 22–5.
    """
    df["hour"] = df["time"].dt.hour
    df["date"] = df["time"].dt.date

    def classify_daypart(hour):
        return "night" if hour < 6 or hour >= 22 else "day"

    df["daypart"] = df["hour"].apply(classify_daypart)

    grouped = df.groupby(["district", "date", "daypart"])["temperature"].median().unstack()
    grouped["day_night_diff"] = grouped["day"] - grouped["night"]
    grouped = grouped.reset_index()
    return grouped[["district", "date", "day_night_diff"]]


def compute_daily_temperature_range(df):
    """
    Calculates the daily temperature range (max - min) per district and date.
    """
    df["date"] = df["time"].dt.date
    grouped = df.groupby(["district", "date"])["temperature"]
    daily_range = grouped.max() - grouped.min()
    return daily_range.reset_index(name="temperature_range")


def compute_monthly_night_temperature(df):
    """
    Calculates the median night-time temperature per district and month.
    Night is defined as 22:00–05:59.
    """
    df["hour"] = df["time"].dt.hour
    df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
    df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

    night_df = df[df["is_night"]]
    return (
        night_df.groupby(["district", "month"])["temperature"]
        .median()
        .reset_index()
    )


def compute_monthly_night_min_temperature(df):
    """
    Calculates the minimum night-time temperature per district and month.
    Night hours: 22:00–05:59.
    """
    df["hour"] = df["time"].dt.hour
    df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
    df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

    night_df = df[df["is_night"]]
    return (
        night_df.groupby(["district", "month"])["temperature"]
        .min()
        .reset_index()
    )


def compute_daily_median_humidity(df):
    """
    Calculates the daily median humidity for each district.
    """
    df["date"] = df["time"].dt.date
    daily_median = (
        df.groupby(["district", "date"])["humidity"]
        .median()
        .reset_index()
    )
    return daily_median


def compute_daily_humidity_range(df):
    """
    Calculates the daily humidity range (max - min) per district and date.
    """
    df["date"] = df["time"].dt.date
    grouped = df.groupby(["district", "date"])["humidity"]
    daily_range = grouped.max() - grouped.min()
    return daily_range.reset_index(name="humidity_range")


def compute_day_night_humidity_difference(df):
    """
    Calculates the difference between day and night median humidity
    for each district and date. Day = 6–21, Night = 22–5.
    """
    df["hour"] = df["time"].dt.hour
    df["date"] = df["time"].dt.date

    def classify_daypart(hour):
        return "night" if hour < 6 or hour >= 22 else "day"

    df["daypart"] = df["hour"].apply(classify_daypart)

    grouped = df.groupby(["district", "date", "daypart"])["humidity"].median().unstack()
    grouped["day_night_diff"] = grouped["day"] - grouped["night"]
    grouped = grouped.reset_index()
    return grouped[["district", "date", "day_night_diff"]]


def compute_monthly_night_humidity(df):
    """
    Calculates the median night-time humidity per district and month.
    Night is defined as 22:00–05:59.
    """
    df["hour"] = df["time"].dt.hour
    df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
    df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

    night_df = df[df["is_night"]]
    return (
        night_df.groupby(["district", "month"])["humidity"]
        .median()
        .reset_index()
    )


def compute_monthly_night_min_humidity(df):
    """
    Calculates the minimum night-time humidity per district and month.
    Night hours: 22:00–05:59.
    """
    df["hour"] = df["time"].dt.hour
    df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
    df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

    night_df = df[df["is_night"]]
    return (
        night_df.groupby(["district", "month"])["humidity"]
        .min()
        .reset_index()
    )
