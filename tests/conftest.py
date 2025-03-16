"""Configuration file for pytest."""

import pytest


def pytest_collection_modifyitems(items):
    """Add custom markers to test items."""
    for item in items:
        if "samples" in item.nodeid:
            item.add_marker(pytest.mark.samples)
