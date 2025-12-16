"""Pytest configuration for memory and performance tests.

This module configures pytest markers and provides fixtures
for memory profiling tests.
"""

from __future__ import annotations

import os
import platform

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )
    config.addinivalue_line(
        "markers",
        "memory: marks tests as memory profiling tests",
    )


def get_memory_limit_multiplier() -> float:
    """Adjust memory limits based on environment.

    CI environments and different architectures may have
    slightly different memory characteristics.
    """
    if os.environ.get("CI"):
        return 1.2  # Allow 20% variance in CI
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        return 1.1  # Apple Silicon variance
    return 1.0


@pytest.fixture
def memory_multiplier() -> float:
    """Get environment-adjusted memory multiplier."""
    return get_memory_limit_multiplier()


@pytest.fixture(autouse=True)
def reset_caches():
    """Reset caches before each test to ensure isolation."""
    yield
    # Clean up after test
    try:
        from analysis.location_analysis import clear_daylight_cache

        clear_daylight_cache()
    except (ImportError, AttributeError):
        pass

    try:
        from utils.get_data_util import clear_parquet_cache

        clear_parquet_cache()
    except (ImportError, AttributeError):
        pass
