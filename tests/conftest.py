"""Configuration file for pytest."""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Add custom markers to test items."""
    for item in items:
        if "samples" in item.nodeid:
            item.add_marker(pytest.mark.samples)
