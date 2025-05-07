import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import get_data_util

# This function is used to compute the monthly averages of temperature and humidity data
# for each sensor. It groups the data by month and sensor ID, and calculates the mean values. 
def compute_monthly_avgs(df):
	df["month"] = pd.to_datetime(df["time"]).dt.to_period("M")
	return (
		df.groupby(["month", "dev-id"])[["temperature", "humidity"]]
		.mean()
		.reset_index()
	)

# This function is used to plot the monthly average humidity data for all sensors.
# It creates a line plot for each sensor, showing the average humidity over time.
def plot_humidity_trends():
	monthly_avgs = compute_monthly_avgs(get_data_util.get_all_locations())
	fig = plt.figure(figsize=(20, 10))
	gs = plt.GridSpec(1, 2, width_ratios=[4, 1])
	ax = fig.add_subplot(gs[0])
	ax_cb = fig.add_subplot(gs[1])

	sensor_lines = {}

	for sensor_id, sensor_data in monthly_avgs.groupby("dev-id"):
		(line,) = ax.plot(
			sensor_data["month"].dt.to_timestamp(),
			sensor_data["humidity"],
			label=sensor_id,
			alpha=0.7,
		)
		sensor_lines[sensor_id] = line

	ax.set_xlabel("Aika")
	ax.set_ylabel("Ilmankosteus(%)")
	ax.set_title("Keskimääräinen kuukausittainen ilmankosteus ajan mittaan")
	ax.tick_params(axis="x", rotation=45)
	ax.grid(True)
	ax.legend(title="Sensors", bbox_to_anchor=(1, 1))

	ax_cb.set_xticks([])
	ax_cb.set_yticks([])
	ax_cb.set_frame_on(False)

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)

	return buf

# This function is used to plot the correlation between temperature and humidity data.
# It creates a scatter plot showing the relationship between the two variables.
def plot_temp_vs_humidity():
	print("plot_temp_vs_humidity")
	df = compute_monthly_avgs(get_data_util.get_all_locations())
	print(df.columns)
	plt.figure(figsize=(12, 6))
	sns.scatterplot(x=df["temperature"], y=df["humidity"], alpha=0.5)

	correlation = df[["temperature", "humidity"]].corr().iloc[0, 1]
	plt.xlabel("Lämpötila (°C)")
	plt.ylabel("Ilmankosteus (%)")
	plt.title(f"Korrelaatiokerroin: {correlation:}")
	plt.legend()
	plt.grid()
	# plt.show()

	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	print(f"correlation coefficient: {correlation:}")
	return buf