import io

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.get_data_util import get_all_locations

# --------------------------
# TEMP FUNCTIONS
# --------------------------


def plot_daily_temperature_range():
	print("[INFO] Plotting daily temperature range...")
	df = get_all_locations()
	df["date"] = df["time"].dt.date
	grouped = df.groupby(["location", "date"])["temperature"]
	daily_range = (grouped.max() - grouped.min()).reset_index(
		name="temperature_range"
	)

	summary = (
		daily_range.groupby("location")["temperature_range"]
		.agg(["mean", "std"])
		.round(2)
	)
	print(
		"\n[SUMMARY] Average daily temperature range (°C) with standard deviation:"
	)
	print(summary)
	print(
		f"\n[INFO] Most dynamic daily temperatures: {summary['mean'].idxmax()}"
	)

	plt.figure(figsize=(10, 5))
	for loc in daily_range["location"].unique():
		subset = daily_range[daily_range["location"] == loc]
		plt.plot(subset["date"], subset["temperature_range"], label=loc)

	plt.title("Päivittäinen lämpötilavaihtelu alueittain")
	plt.xlabel("Päivämäärä")
	plt.ylabel("Lämpötila (°C)")
	plt.grid(axis="y")
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_daily_median_temperature():
	print("[INFO] Plotting daily median temperature...")
	df = get_all_locations()
	df["date"] = df["time"].dt.date
	daily_median = (
		df.groupby(["location", "date"])["temperature"].median().reset_index()
	)

	summary = (
		daily_median.groupby("location")["temperature"]
		.agg(["mean", "std"])
		.round(2)
	)
	print(
		"\n[SUMMARY] Average daily median temperature (°C) with standard deviation:"
	)
	print(summary)
	print(f"\n[INFO] Warmest area on average: {summary['mean'].idxmax()}")

	plt.figure(figsize=(10, 5))
	for loc in daily_median["location"].unique():
		subset = daily_median[daily_median["location"] == loc]
		plt.plot(subset["date"], subset["temperature"], label=loc)

	plt.title("Päivittäinen lämpötilamediaani alueittain")
	plt.xlabel("Päivämäärä")
	plt.ylabel("Lämpötila (°C)")
	plt.grid(axis="y")
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_day_night_temperature_difference():
	print("[INFO] Plotting day-night temperature difference (monthly)...")
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["date"] = df["time"].dt.date
	df["daypart"] = df["hour"].apply(
		lambda h: "night" if h < 6 or h >= 22 else "day"
	)

	grouped = (
		df.groupby(["location", "date", "daypart"])["temperature"]
		.median()
		.unstack()
	)
	grouped["day_night_diff"] = grouped["day"] - grouped["night"]
	grouped = grouped.reset_index()
	grouped["month"] = pd.to_datetime(grouped["date"]).dt.to_period("M")

	monthly_diff = (
		grouped.groupby(["month", "location"])["day_night_diff"]
		.mean()
		.unstack()
	)

	avg_diff = monthly_diff.mean(axis=0).round(2)
	print("\n[SUMMARY] Average monthly day-night temperature difference (°C):")
	print(avg_diff.sort_values(ascending=False))

	monthly_diff.plot(kind="bar", figsize=(10, 5))
	plt.title(
		"Kuukausittainen keskimääräinen lämpötilaero päivän ja yön välillä alueittain"
	)
	plt.xlabel("Kuukausi")
	plt.ylabel("Lämpötilaero (°C)")
	plt.grid(axis="y")
	plt.xticks(rotation=0)
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_monthly_night_temperature():
	print("[INFO] Plotting monthly night-time median temperature...")
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
	df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

	night_df = df[df["is_night"]]
	night_df = (
		night_df.groupby(["location", "month"])["temperature"]
		.median()
		.reset_index()
	)
	night_df["month_str"] = night_df["month"].astype(str)

	avg_night = night_df.groupby("location")["temperature"].mean().round(2)
	extremes = (
		night_df.groupby("location")["temperature"].agg(["min", "max"]).round(2)
	)

	print("\n[SUMMARY] Average monthly night-time temperature (°C):")
	print(avg_night.sort_values(ascending=False))
	print("\n[INFO] Monthly night temperature extremes per location:")
	print(extremes)
	print(f"\n[INFO] Warmest nights on average: {avg_night.idxmax()}")

	pivot_df = night_df.pivot(
		index="month_str", columns="location", values="temperature"
	)
	pivot_df.plot(kind="bar", figsize=(10, 5))
	plt.title("Kuukausittainen yölämpötilan mediaani alueittain")
	plt.xlabel("Kuukausi")
	plt.ylabel("Lämpötila (°C)")
	plt.grid(axis="y")
	plt.xticks(rotation=0)
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_monthly_night_min_temperature():
	print("[INFO] Plotting monthly night-time minimum temperatures...")
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
	df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

	night_df = df[df["is_night"]]
	night_min_df = (
		night_df.groupby(["location", "month"])["temperature"]
		.min()
		.reset_index()
	)
	night_min_df["month_str"] = night_min_df["month"].astype(str)

	# Kuukauden minimitulostus
	for month in sorted(night_min_df["month_str"].unique()):
		print(f"\n[SUMMARY] Minimum night-time temperatures for {month}:")
		print(
			night_min_df[night_min_df["month_str"] == month][
				["location", "temperature"]
			].sort_values("temperature")
		)

	pivot_df = night_min_df.pivot(
		index="month_str", columns="location", values="temperature"
	)
	pivot_df.plot(kind="bar", figsize=(10, 5))
	plt.title("Kuukausittainen yön alin lämpötila alueittain")
	plt.xlabel("Kuukausi")
	plt.ylabel("Alin lämpötila (°C)")
	plt.grid(axis="y")
	plt.xticks(rotation=0)
	plt.legend()
	plt.tight_layout()

	summary = night_min_df.groupby("location")["temperature"].mean().round(2)
	print("\n[SUMMARY] Average monthly minimum night-time temperature (°C):")
	print(summary.sort_values(ascending=False))
	print(f"\n[INFO] Warmest night minimums on average: {summary.idxmax()}")

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_monthly_night_temperature_difference(reference_location="Laajasalo"):
	print(
		"[INFO] Plotting monthly night-time temperature differences (compared to Laajasalo)..."
	)
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
	df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

	night_df = df[df["is_night"]]
	grouped = (
		night_df.groupby(["location", "month"])["temperature"]
		.median()
		.reset_index()
	)
	grouped["month_str"] = grouped["month"].astype(str)

	pivot = grouped.pivot(
		index="month_str", columns="location", values="temperature"
	)

	if reference_location not in pivot.columns:
		print(
			f"[WARNING] Reference location '{reference_location}' not found in data."
		)
		return None

	diff_df = pivot.subtract(pivot[reference_location], axis=0).drop(
		columns=[reference_location]
	)

	print(
		"\n[SUMMARY] Average monthly night-time temperature difference vs. Laajasalo (°C):"
	)
	print(diff_df.mean().round(2))

	plt.figure(figsize=(10, 5))
	for loc in diff_df.columns:
		plt.plot(
			diff_df.index,
			diff_df[loc],
			marker="o",
			label=f"{loc} - {reference_location}",
		)

	plt.axhline(0, color="gray", linestyle="--", linewidth=1)
	plt.title("Kuukausittainen yölämpötilaero verrattuna Laajasaloon")
	plt.xlabel("Kuukausi")
	plt.ylabel("Lämpötilaero (°C)")
	plt.grid(axis="y")
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


# --------------------------
# HUMIDITY FUNCTIONS
# --------------------------


def plot_daily_median_humidity():
	print("[INFO] Plotting daily median humidity...")
	df = get_all_locations()
	df["date"] = df["time"].dt.date
	daily_median = (
		df.groupby(["location", "date"])["humidity"].median().reset_index()
	)

	summary = (
		daily_median.groupby("location")["humidity"]
		.agg(["mean", "std"])
		.round(2)
	)
	print(
		"\n[SUMMARY] Average daily median humidity (%) with standard deviation:"
	)
	print(summary)

	plt.figure(figsize=(10, 5))
	for loc in daily_median["location"].unique():
		subset = daily_median[daily_median["location"] == loc]
		plt.plot(subset["date"], subset["humidity"], label=loc)

	plt.title("Päivittäinen kosteuden mediaani alueittain")
	plt.xlabel("Päivämäärä")
	plt.ylabel("Kosteus (%)")
	plt.grid(axis="y")
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_daily_humidity_range():
	print("[INFO] Plotting daily humidity range...")
	df = get_all_locations()
	df["date"] = df["time"].dt.date
	grouped = df.groupby(["location", "date"])["humidity"]
	daily_range = (grouped.max() - grouped.min()).reset_index(
		name="humidity_range"
	)

	summary = (
		daily_range.groupby("location")["humidity_range"]
		.agg(["mean", "std"])
		.round(2)
	)
	print(
		"\n[SUMMARY] Average daily humidity range (%) with standard deviation:"
	)
	print(summary)

	plt.figure(figsize=(10, 5))
	for loc in daily_range["location"].unique():
		subset = daily_range[daily_range["location"] == loc]
		plt.plot(subset["date"], subset["humidity_range"], label=loc)

	plt.title("Päivittäinen kosteuden vaihteluväli alueittain")
	plt.xlabel("Päivämäärä")
	plt.ylabel("Kosteusvaihtelu (%)")
	plt.grid(axis="y")
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_day_night_humidity_difference():
	print("[INFO] Plotting day-night humidity difference (monthly)...")
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["date"] = df["time"].dt.date
	df["daypart"] = df["hour"].apply(
		lambda h: "night" if h < 6 or h >= 22 else "day"
	)

	grouped = (
		df.groupby(["location", "date", "daypart"])["humidity"]
		.median()
		.unstack()
	)
	grouped["day_night_diff"] = grouped["day"] - grouped["night"]
	grouped = grouped.reset_index()
	grouped["month"] = pd.to_datetime(grouped["date"]).dt.to_period("M")

	monthly_diff = (
		grouped.groupby(["month", "location"])["day_night_diff"]
		.mean()
		.unstack()
	)

	avg_diff = monthly_diff.mean(axis=0).round(2)
	print("\n[SUMMARY] Average monthly day-night humidity difference (%):")
	print(avg_diff.sort_values(ascending=False))

	monthly_diff.plot(kind="bar", figsize=(10, 5))
	plt.title("Kuukausittainen kosteusero päivän ja yön välillä alueittain")
	plt.xlabel("Kuukausi")
	plt.ylabel("Kosteusero (%)")
	plt.grid(axis="y")
	plt.xticks(rotation=0)
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


def plot_monthly_night_humidity():
	print("[INFO] Plotting monthly night-time median humidity...")
	df = get_all_locations()
	df["hour"] = df["time"].dt.hour
	df["month"] = df["time"].dt.tz_convert(None).dt.to_period("M")
	df["is_night"] = df["hour"].between(0, 5) | df["hour"].between(22, 23)

	night_df = df[df["is_night"]]
	night_df = (
		night_df.groupby(["location", "month"])["humidity"]
		.median()
		.reset_index()
	)
	night_df["month_str"] = night_df["month"].astype(str)

	avg_night = night_df.groupby("location")["humidity"].mean().round(2)
	extremes = (
		night_df.groupby("location")["humidity"].agg(["min", "max"]).round(2)
	)

	print("\n[SUMMARY] Average monthly night-time humidity (%):")
	print(avg_night.sort_values(ascending=False))
	print("\n[INFO] Monthly night humidity extremes per location:")
	print(extremes)
	print(
		f"\n[INFO] Highest humidity at night on average: {avg_night.idxmax()}"
	)

	pivot_df = night_df.pivot(
		index="month_str", columns="location", values="humidity"
	)
	pivot_df.plot(kind="bar", figsize=(10, 5))
	plt.title("Kuukausittainen yökosteuden mediaani alueittain")
	plt.xlabel("Kuukausi")
	plt.ylabel("Kosteus (%)")
	plt.grid(axis="y")
	plt.xticks(rotation=0)
	plt.legend()
	plt.tight_layout()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
	# plt.show()


# --------------------------
# MAIN
# --------------------------


def main():
	df = get_all_locations()

	# Temperature
	plot_daily_temperature_range(df)
	plot_daily_median_temperature(df)
	plot_day_night_temperature_difference(df)
	plot_monthly_night_temperature(df)
	plot_monthly_night_min_temperature(df)
	plot_monthly_night_temperature_difference(df)

	# Humidity
	plot_daily_median_humidity(df)
	plot_daily_humidity_range(df)
	plot_day_night_humidity_difference(df)
	plot_monthly_night_humidity(df)


if __name__ == "__main__":
	main()
