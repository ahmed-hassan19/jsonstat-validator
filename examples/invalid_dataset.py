#!/usr/bin/env python3
"""Example script to create an invalid JSON-stat object/file.

The object/file is based on the valid example in `examples/validate_dataset.py`,
but with missing the required `dimension` field.
"""

import json

from jsonstat_validator.validator import Dataset


def validate_invalid_dataset_from_file():
    """Validate a JSON-stat dataset from a JSON file."""
    try:
        with open("tests/samples/order_invalid.json", "r") as f:
            dataset_dict = json.load(f)
    except FileNotFoundError:
        print("❌ Dataset file not found")
        return

    try:
        Dataset(**dataset_dict)
        print("✅ Valid JSON-stat dataset!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    validate_invalid_dataset_from_file()
