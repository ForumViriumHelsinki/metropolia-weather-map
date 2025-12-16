"""Fluctuation and decomposition analysis for weather sensor data.

This module provides functions for analyzing humidity data patterns using
FFT (Fast Fourier Transform) and STL (Seasonal-Trend decomposition using LOESS).
"""

from __future__ import annotations

import gc
import io
import logging
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from numpy.fft import fft
from statsmodels.tsa.seasonal import STL

from utils.get_data_util import get_all_locations
from utils.utils import map_locations

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def plot_raw_humidity(df: pd.DataFrame | None = None) -> io.BytesIO:
    """Plot raw humidity data from all sensors.

    Args:
        df: Optional pre-loaded DataFrame. If None, loads data via get_all_locations().

    Returns:
        BytesIO buffer containing the PNG image.
    """
    logger.info("Plotting raw humidity data...")
    if df is None:
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
    plt.close(fig)
    buf.seek(0)

    # Free memory after plot generation
    del sensor_lines
    gc.collect()

    return buf


def plot_fft_analysis(
    area: str | None = None,
    df: pd.DataFrame | None = None,
) -> io.BytesIO:
    """Plot FFT analysis of humidity data.

    Uses the Fast Fourier Transform to analyze frequency components
    of the humidity data. User can specify an area to filter the data.

    Args:
        area: Optional area name to filter sensors. If None, uses all sensors.
        df: Optional pre-loaded DataFrame. If None, loads data via get_all_locations().

    Returns:
        BytesIO buffer containing the PNG image.

    Raises:
        ValueError: If specified area is not valid.
    """
    logger.info(
        "Plotting FFT analysis%s...", f" for area {area}" if area else ""
    )
    if df is None:
        df = get_all_locations()

    location_map = map_locations()

    if area:
        if area not in location_map:
            raise ValueError(
                f"Invalid area: {area}. Valid areas are: {list(location_map.keys())}"
            )
        sensor_ids = location_map[area]
        df = df[df["dev-id"].isin(sensor_ids)]

    df.set_index("time", inplace=True)
    grouped = df[["dev-id", "humidity"]].groupby("dev-id").resample("D").mean()
    grouped = grouped.reset_index()
    grouped["humidity"] = (
        grouped["humidity"].rolling(window=7, min_periods=1).mean()
    )

    # Free original df memory after grouping
    del df
    gc.collect()

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
    plt.close(fig)
    buf.seek(0)

    # Free memory after plot generation
    del grouped, sensor_lines
    gc.collect()

    return buf


def plot_seasonal_decomposition(
    df: pd.DataFrame | None = None,
) -> io.BytesIO | None:
    """Plot seasonal decomposition of humidity data using STL.

    Uses Seasonal-Trend decomposition using LOESS to decompose the time series
    data into trend, seasonal, and residual components.

    Args:
        df: Optional pre-loaded DataFrame. If None, loads data via get_all_locations().

    Returns:
        BytesIO buffer containing the PNG image, or None if insufficient data.
    """
    logger.info("Plotting seasonal decomposition...")
    if df is None:
        df = get_all_locations()

    logger.debug("Columns at start of seasonal decomposition: %s", df.dtypes)

    if "time" not in df.columns:
        logger.error("'time' column missing before STL decomposition!")
        return None

    df.set_index("time", inplace=True)
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    df = df[["humidity"]].resample("h").mean()
    df["humidity"] = df["humidity"].interpolate(method="time")
    df = df.dropna()

    min_data_points = 14  # Minimum required for STL decomposition
    if len(df) < min_data_points:
        logger.error("Not enough data points for STL decomposition!")
        return None

    stl = STL(df["humidity"], seasonal=143)
    result = stl.fit()

    # Free df memory before creating figure
    del df
    gc.collect()

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    result.trend.plot(ax=axes[0], title="Trendi")
    result.seasonal.plot(ax=axes[1], title="Kausiluonteisuus")
    result.resid.plot(ax=axes[2], title="Jäännös")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    # Free memory after plot generation
    del result
    gc.collect()

    return buf
