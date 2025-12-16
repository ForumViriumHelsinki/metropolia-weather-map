"""Memory usage tests for plot generation.

These tests ensure that plot generation stays within acceptable memory limits.
Target: Under 512MB peak memory usage for any single plot operation.
"""

import gc
import io
import tracemalloc
from typing import Callable

import pytest

# Target memory limit in bytes (512 MB)
MEMORY_LIMIT_BYTES = 512 * 1024 * 1024

# More aggressive target for optimized code (256 MB)
MEMORY_TARGET_BYTES = 256 * 1024 * 1024


def measure_peak_memory(func: Callable) -> tuple[bytes, float]:
    """Measure peak memory usage of a function.

    Returns:
        tuple: (result, peak_memory_bytes)
    """
    gc.collect()
    tracemalloc.start()

    try:
        result = func()
        current, peak = tracemalloc.get_traced_memory()
        return result, peak
    finally:
        tracemalloc.stop()
        gc.collect()


def bytes_to_mb(bytes_val: int) -> float:
    """Convert bytes to megabytes."""
    return bytes_val / (1024 * 1024)


class TestPlotMemoryUsage:
    """Test memory usage for plot generation endpoints."""

    @pytest.mark.slow
    def test_fft_plot_memory(self):
        """FFT plot should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        result, peak_memory = measure_peak_memory(
            fluctuation_and_decomposition_analysis.plot_fft_analysis
        )

        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"
        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"FFT plot used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )

    @pytest.mark.slow
    def test_raw_humidity_plot_memory(self):
        """Raw humidity plot should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        result, peak_memory = measure_peak_memory(
            fluctuation_and_decomposition_analysis.plot_raw_humidity
        )

        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"
        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"Raw humidity plot used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )

    @pytest.mark.slow
    def test_seasonal_decomposition_memory(self):
        """Seasonal decomposition should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        result, peak_memory = measure_peak_memory(
            fluctuation_and_decomposition_analysis.plot_seasonal_decomposition
        )

        # This may return None if not enough data
        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"Seasonal decomposition used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )

    @pytest.mark.slow
    def test_daily_temperature_range_memory(self):
        """Daily temperature range plot should use less than 512MB memory."""
        from analysis import location_analysis

        result, peak_memory = measure_peak_memory(
            location_analysis.plot_daily_temperature_range
        )

        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"
        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"Daily temp range used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )


class TestDataLoadingMemory:
    """Test memory usage for data loading operations."""

    @pytest.mark.slow
    def test_get_all_locations_memory(self):
        """Loading all locations should use reasonable memory."""
        from utils.get_data_util import get_all_locations

        result, peak_memory = measure_peak_memory(get_all_locations)

        print(f"\nget_all_locations() peak memory: {bytes_to_mb(peak_memory):.1f}MB")
        print(f"DataFrame shape: {result.shape}")
        print(f"DataFrame memory: {result.memory_usage(deep=True).sum() / 1024 / 1024:.1f}MB")

        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"get_all_locations used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )


class TestMemoryTargets:
    """Tests with stricter memory targets for optimized code."""

    @pytest.mark.slow
    @pytest.mark.xfail(reason="Target for optimized implementation")
    def test_fft_plot_optimized_target(self):
        """FFT plot should use less than 256MB after optimization."""
        from analysis import fluctuation_and_decomposition_analysis

        result, peak_memory = measure_peak_memory(
            fluctuation_and_decomposition_analysis.plot_fft_analysis
        )

        assert peak_memory < MEMORY_TARGET_BYTES, (
            f"FFT plot used {bytes_to_mb(peak_memory):.1f}MB, "
            f"target is {bytes_to_mb(MEMORY_TARGET_BYTES):.1f}MB"
        )


if __name__ == "__main__":
    # Quick profiling script when run directly
    print("Memory Profiling Report")
    print("=" * 50)

    from analysis import fluctuation_and_decomposition_analysis, location_analysis
    from utils.get_data_util import get_all_locations

    tests = [
        ("get_all_locations", get_all_locations),
        ("plot_fft_analysis", fluctuation_and_decomposition_analysis.plot_fft_analysis),
        ("plot_raw_humidity", fluctuation_and_decomposition_analysis.plot_raw_humidity),
        ("plot_daily_temperature_range", location_analysis.plot_daily_temperature_range),
    ]

    for name, func in tests:
        print(f"\nTesting: {name}")
        try:
            result, peak_memory = measure_peak_memory(func)
            status = "✅ PASS" if peak_memory < MEMORY_LIMIT_BYTES else "❌ FAIL"
            print(f"  Peak memory: {bytes_to_mb(peak_memory):.1f}MB {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
