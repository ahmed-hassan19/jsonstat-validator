"""
Test the official JSON-stat samples and collections.

This test suite validates the official JSON-stat samples provided by the JSON-stat
website: https://json-stat.org/samples/. For efficiency purposes, all sample-files
are downloaded and saved in the jsonstat_validator/tests/samples directory.
"""

import glob
import json
from pathlib import Path

import pytest

from jsonstat_validator import validate_jsonstat

# Get the path to the samples directory
TESTS_DIR = Path(__file__).parent
SAMPLES_DIR = TESTS_DIR / "samples"

# Find all JSON files in the samples directory
official_samples_files = glob.glob(str(SAMPLES_DIR / "**" / "*.json"), recursive=True)


def load_json_file(file_path):
    """Load a JSON file and return the parsed JSON object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("sample_path", official_samples_files)
def test_official_sample(sample_path):
    """Test that official JSON-stat samples validate successfully."""
    try:
        # Load the JSON file
        data = load_json_file(sample_path)

        # Validate the JSON-stat object
        result = validate_jsonstat(data)
        assert result is True, f"Failed to validate {sample_path}"
    except ValueError as e:
        pytest.fail(f"Failed to validate {sample_path}: {e}")


if __name__ == "__main__":
    # This allows running the tests directly with python
    # Run pytest with the following options:
    # -v: verbose output (show test names)
    # -s: don't capture stdout (allow print statements to be shown)
    # __file__: run tests only in this file
    pytest.main(["-vs", __file__])
