"""Memory usage tests for plot generation.

These tests ensure that plot generation stays within acceptable memory limits.
Uses pytest-memray for native code tracking (matplotlib C extensions) and
automatic memory limit enforcement.

Memory Limits:
- Hard limit: 512MB (must not exceed, blocks PR)
- Optimization target: 256MB (goal for optimized functions)

Run with:
    pytest -m slow src/tests/test_memory_usage.py -v
    pytest --memray -m slow src/tests/test_memory_usage.py -v  # With memray profiling
"""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable

# Memory limits
MEMORY_LIMIT_MB = 512
MEMORY_TARGET_MB = 256


# =============================================================================
# Plot Generation Tests - Hard Limits (512MB)
# =============================================================================


class TestPlotMemoryLimits:
    """Test that plot generation stays within 512MB hard limit.

    These tests use pytest-memray's limit_memory marker for accurate
    native code tracking (matplotlib C extensions, NumPy, etc.).
    """

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_fft_plot_memory(self):
        """FFT plot should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        result = fluctuation_and_decomposition_analysis.plot_fft_analysis()
        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_raw_humidity_plot_memory(self):
        """Raw humidity plot should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        result = fluctuation_and_decomposition_analysis.plot_raw_humidity()
        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_seasonal_decomposition_memory(self):
        """Seasonal decomposition should use less than 512MB memory."""
        from analysis import fluctuation_and_decomposition_analysis

        # This may return None if not enough data
        fluctuation_and_decomposition_analysis.plot_seasonal_decomposition()

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_daily_temperature_range_memory(self):
        """Daily temperature range plot should use less than 512MB memory."""
        from analysis import location_analysis

        result = location_analysis.plot_daily_temperature_range()
        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_daily_median_temperature_memory(self):
        """Daily median temperature plot should use less than 512MB memory."""
        from analysis import location_analysis

        result = location_analysis.plot_daily_median_temperature()
        assert isinstance(result, io.BytesIO), "Should return BytesIO buffer"


# =============================================================================
# Data Loading Tests
# =============================================================================


class TestDataLoadingMemory:
    """Test memory usage for data loading operations."""

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_LIMIT_MB} MB")
    def test_get_all_locations_memory(self):
        """Loading all locations should use less than 512MB memory."""
        from utils.get_data_util import get_all_locations

        df = get_all_locations()
        assert not df.empty, "Should return non-empty DataFrame"


# =============================================================================
# Optimization Target Tests (256MB)
# =============================================================================


class TestMemoryOptimizationTargets:
    """Tests with stricter 256MB memory targets.

    These represent optimization goals. Failures indicate
    opportunities for improvement, not blocking issues.
    """

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_TARGET_MB} MB")
    def test_fft_plot_optimized(self):
        """FFT plot should use less than 256MB after optimization."""
        from analysis import fluctuation_and_decomposition_analysis

        result = fluctuation_and_decomposition_analysis.plot_fft_analysis()
        assert isinstance(result, io.BytesIO)

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_TARGET_MB} MB")
    def test_daily_temperature_range_optimized(self):
        """Daily temperature range should use less than 256MB."""
        from analysis import location_analysis

        result = location_analysis.plot_daily_temperature_range()
        assert isinstance(result, io.BytesIO)

    @pytest.mark.slow
    @pytest.mark.limit_memory(f"{MEMORY_TARGET_MB} MB")
    def test_daily_median_temperature_optimized(self):
        """Daily median temperature should use less than 256MB."""
        from analysis import location_analysis

        result = location_analysis.plot_daily_median_temperature()
        assert isinstance(result, io.BytesIO)


# =============================================================================
# Memory Leak Detection Tests
# =============================================================================


class TestMemoryLeaks:
    """Test for memory leaks in repeated operations.

    Uses pytest-memray's limit_leaks marker to detect memory
    that isn't freed after multiple iterations.
    """

    @pytest.mark.slow
    @pytest.mark.limit_leaks("10 MB")
    def test_repeated_plot_generation_no_leak(self):
        """Repeated plot generation should not leak memory."""
        from analysis import location_analysis

        for _ in range(3):
            result = location_analysis.plot_daily_temperature_range()
            assert isinstance(result, io.BytesIO)
            # Buffer should be garbage collected between iterations

    @pytest.mark.slow
    @pytest.mark.limit_leaks("5 MB")
    def test_daylight_cache_no_leak(self):
        """Daylight data cache should not leak on repeated access."""
        from analysis.location_analysis import load_daylight_data

        for _ in range(10):
            df = load_daylight_data()
            assert not df.empty


# =============================================================================
# Cache Efficiency Tests
# =============================================================================


class TestCacheEfficiency:
    """Test that caching mechanisms work correctly."""

    @pytest.mark.slow
    def test_daylight_data_caching(self):
        """Daylight data should be cached and not reload on each call."""
        import gc
        import tracemalloc

        from analysis.location_analysis import (
            clear_daylight_cache,
            load_daylight_data,
        )

        # Clear cache to start fresh
        clear_daylight_cache()
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
        # Allow some overhead but expect < 50% of first call
        assert second_peak < first_peak * 0.5, (
            f"Cache hit used {second_peak / 1024 / 1024:.1f}MB, "
            f"expected < {first_peak * 0.5 / 1024 / 1024:.1f}MB"
        )

    @pytest.mark.slow
    def test_parquet_cache_efficiency(self):
        """Parquet data should be cached across calls."""
        import gc
        import tracemalloc

        from utils.get_data_util import clear_parquet_cache, get_vallila

        # Clear cache to start fresh
        clear_parquet_cache()
        gc.collect()

        tracemalloc.start()

        # First call downloads and caches
        df1 = get_vallila(get_2024=True)
        _, first_peak = tracemalloc.get_traced_memory()

        # Second call should hit cache
        tracemalloc.reset_peak()
        df2 = get_vallila(get_2024=True)
        _, second_peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        assert len(df1) == len(df2), "Cached data should have same length"

        # Cache hit should use much less memory
        assert second_peak < first_peak * 0.3, (
            f"Cache hit used {second_peak / 1024 / 1024:.1f}MB, "
            f"expected < {first_peak * 0.3 / 1024 / 1024:.1f}MB"
        )


# =============================================================================
# Profiling Script (for manual runs)
# =============================================================================


def _run_profiling_report() -> None:
    """Generate a memory profiling report when run directly."""
    import gc
    import tracemalloc

    from analysis import (
        fluctuation_and_decomposition_analysis,
        location_analysis,
    )
    from utils.get_data_util import get_all_locations

    def measure_peak_memory(func: Callable) -> tuple[object, float]:
        """Measure peak memory usage of a function."""
        gc.collect()
        tracemalloc.start()
        try:
            result = func()
            _, peak = tracemalloc.get_traced_memory()
            return result, peak
        finally:
            tracemalloc.stop()
            gc.collect()

    print("Memory Profiling Report")
    print("=" * 60)
    print(f"Hard Limit: {MEMORY_LIMIT_MB}MB | Target: {MEMORY_TARGET_MB}MB")
    print("=" * 60)

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
            "plot_seasonal_decomposition",
            fluctuation_and_decomposition_analysis.plot_seasonal_decomposition,
        ),
        (
            "plot_daily_temperature_range",
            location_analysis.plot_daily_temperature_range,
        ),
        (
            "plot_daily_median_temperature",
            location_analysis.plot_daily_median_temperature,
        ),
    ]

    for name, func in tests:
        print(f"\n{name}:")
        try:
            _, peak_memory = measure_peak_memory(func)
            peak_mb = peak_memory / 1024 / 1024

            if peak_mb > MEMORY_LIMIT_MB:
                status = "❌ EXCEEDS LIMIT"
            elif peak_mb > MEMORY_TARGET_MB:
                status = "⚠️  Above target"
            else:
                status = "✅ PASS"

            print(f"  Peak: {peak_mb:.1f}MB {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    _run_profiling_report()
