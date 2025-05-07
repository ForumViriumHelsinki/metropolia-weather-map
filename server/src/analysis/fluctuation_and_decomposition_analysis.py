import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import gridspec
from numpy.fft import fft
from statsmodels.tsa.seasonal import STL
from utils.get_data_util import get_all_locations
from utils.utils import map_locations

### This function is used to plot the raw humidity data from all sensors
def plot_raw_humidity():
	df = get_all_locations()
	map_locations()
	fig = plt.figure(figsize=(20, 10))
	gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
	ax = fig.add_subplot(gs[0])
	ax_cb = fig.add_subplot(gs[1])

	sensor_lines = {}

	for sensor_id, sensor_data in df.groupby("dev-id"):
		(line,) = ax.plot(
			sensor_data["time"],
			sensor_data["humidity"],
			label=sensor_id,
			alpha=0.7,
		)
		sensor_lines[sensor_id] = line

	ax.set_xlabel("Aika")
	ax.set_ylabel("Ilmankosteus (%)")
	ax.set_title("Raaka ilmankosteusdata ajan mittaan")
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

## This function is used to plot the FFT analysis of the humidity data. User can specify an area to filter the data.
## The function uses the Fast Fourier Transform to analyze the frequency components of the humidity data.
def plot_fft_analysis(area=None):
	df = get_all_locations()
	map = map_locations()

	if area:
		if area not in map:
			raise ValueError(
				f"Invalid area: {area}. Valid areas are: {list(map.keys())}"
			)
		sensor_ids = map[area]
		df = df[df["dev-id"].isin(sensor_ids)]

	df.set_index("time", inplace=True)
	grouped = df[["dev-id", "humidity"]].groupby("dev-id").resample("D").mean()
	grouped = grouped.reset_index()
	grouped["humidity"] = (
		grouped["humidity"].rolling(window=7, min_periods=1).mean()
	)

	fig = plt.figure(figsize=(20, 10))
	gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
	ax = fig.add_subplot(gs[0])
	ax_cb = fig.add_subplot(gs[1])

	sensor_lines = {}

	for sensor_id in grouped["dev-id"].unique():
		sensor_df = grouped[grouped["dev-id"] == sensor_id]
		humidity_fft = fft(sensor_df["humidity"].dropna())
		freqs = np.fft.fftfreq(len(humidity_fft))
		(line,) = ax.plot(
			freqs[: len(freqs) // 2],
			np.abs(humidity_fft[: len(freqs) // 2]),
			label=sensor_id,
			alpha=0.7,
		)
		sensor_lines[sensor_id] = line

	ax.set_yscale("log")
	ax.set_title("Ilmankosteuden FFT-analyysi")
	ax.set_xlabel("Taajuus (x/1)")
	ax.set_ylabel("Voimakkuus")
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

## This function is used to plot the seasonal decomposition of the humidity data using STL (Seasonal-Trend decomposition using LOESS).
## The function decomposes the time series data into trend, seasonal, and residual components.
def plot_seasonal_decomposition():
	df = get_all_locations()
	print("Columns at start of seasonal decomposition:", df.dtypes)

	if "time" not in df.columns:
		print("Error: 'time' column missing before STL decomposition!")
		return None

	df.set_index("time", inplace=True)
	df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
	df = df[["humidity"]].resample("h").mean()
	df["humidity"] = df["humidity"].interpolate(method="time")
	df = df.dropna()

	if len(df) < 14:
		print("Error: Not enough data points for STL decomposition!")
		return None

	stl = STL(df["humidity"], seasonal=143)
	result = stl.fit()

	fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
	result.trend.plot(ax=axes[0], title="Trendi")
	result.seasonal.plot(ax=axes[1], title="Kausiluonteisuus")
	result.resid.plot(ax=axes[2], title="Jäännös")
	buf = io.BytesIO()
	plt.savefig(buf, format="png")
	plt.close()
	buf.seek(0)
	return buf
