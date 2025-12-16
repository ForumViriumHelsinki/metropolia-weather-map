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

        print(
            f"\nget_all_locations() peak memory: {bytes_to_mb(peak_memory):.1f}MB"
        )
        print(f"DataFrame shape: {result.shape}")
        print(
            f"DataFrame memory: {result.memory_usage(deep=True).sum() / 1024 / 1024:.1f}MB"
        )

        assert peak_memory < MEMORY_LIMIT_BYTES, (
            f"get_all_locations used {bytes_to_mb(peak_memory):.1f}MB, "
            f"limit is {bytes_to_mb(MEMORY_LIMIT_BYTES):.1f}MB"
        )


class TestMemoryTargets:
    """Tests with stricter memory targets for optimized code."""

    @pytest.mark.slow
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

    @pytest.mark.slow
    def test_daylight_data_caching(self):
        """Daylight data should be cached and not reload on each call."""
        import gc

        from analysis.location_analysis import load_daylight_data

        gc.collect()
        tracemalloc.start()

        # First call loads data
        df1 = load_daylight_data()
        _, first_peak = tracemalloc.get_traced_memory()

        # Second call should use cache (minimal memory allocation)
        tracemalloc.reset_peak()
        df2 = load_daylight_data()
        _, second_peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        # Both should return same data
        assert df1.equals(df2), "Cached data should be identical"

        # Second call should use significantly less memory (cache hit)
        # Allow some overhead but expect < 10% of first call
        max_cache_hit_memory = first_peak * 0.1
        assert second_peak < max_cache_hit_memory, (
            f"Cache hit used {bytes_to_mb(second_peak):.1f}MB, "
            f"expected < {bytes_to_mb(max_cache_hit_memory):.1f}MB (10% of first call)"
        )

    @pytest.mark.slow
    def test_filter_install_date_memory_efficiency(self):
        """filter_install_date should not create excessive intermediate DataFrames."""
        from utils.get_data_util import filter_install_date, get_rest

        # Load test data
        df = get_rest(get_2024=True)
        initial_size = df.memory_usage(deep=True).sum()

        gc.collect()
        tracemalloc.start()

        filter_install_date(df, "Laajasalo")

        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak memory should not exceed 3x the input DataFrame size
        # (1x for input, 1x for output, 1x for intermediate operations)
        max_allowed = initial_size * 3
        assert peak_memory < max_allowed, (
            f"filter_install_date peak memory {bytes_to_mb(peak_memory):.1f}MB "
            f"exceeded 3x input size ({bytes_to_mb(max_allowed):.1f}MB)"
        )

    @pytest.mark.slow
    def test_all_plot_functions_under_target(self):
        """All plot functions should stay under 256MB target."""
        from analysis import location_analysis

        # Functions that should be optimized
        plot_functions = [
            (
                "plot_daily_temperature_range",
                location_analysis.plot_daily_temperature_range,
            ),
            (
                "plot_daily_median_temperature",
                location_analysis.plot_daily_median_temperature,
            ),
        ]

        failures = []
        for name, func in plot_functions:
            result, peak_memory = measure_peak_memory(func)
            if peak_memory >= MEMORY_TARGET_BYTES:
                failures.append(
                    f"{name}: {bytes_to_mb(peak_memory):.1f}MB "
                    f"(target: {bytes_to_mb(MEMORY_TARGET_BYTES):.1f}MB)"
                )

        assert not failures, "Functions exceeding 256MB target:\n" + "\n".join(
            failures
        )


if __name__ == "__main__":
    # Quick profiling script when run directly
    print("Memory Profiling Report")
    print("=" * 50)

    from analysis import (
        fluctuation_and_decomposition_analysis,
        location_analysis,
    )
    from utils.get_data_util import get_all_locations

    tests = [
        ("get_all_locations", get_all_locations),
        (
            "plot_fft_analysis",
            fluctuation_and_decomposition_analysis.plot_fft_analysis,
        ),
        (
            "plot_raw_humidity",
            fluctuation_and_decomposition_analysis.plot_raw_humidity,
        ),
        (
            "plot_daily_temperature_range",
            location_analysis.plot_daily_temperature_range,
        ),
    ]

    for name, func in tests:
        print(f"\nTesting: {name}")
        try:
            result, peak_memory = measure_peak_memory(func)
            status = (
                "✅ PASS" if peak_memory < MEMORY_LIMIT_BYTES else "❌ FAIL"
            )
            print(f"  Peak memory: {bytes_to_mb(peak_memory):.1f}MB {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
