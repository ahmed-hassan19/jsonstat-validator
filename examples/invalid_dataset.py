#!/usr/bin/env python3
"""Example script to create an invalid JSON-stat object/file.

The object is based on the valid example in `examples/validate_dataset.py`,
but with missing the required `dimension` field.
"""

from jsonstat_validator.validator import Dataset


def validate_invalid_dataset_from_file():
    """Validate a JSON-stat dataset from a JSON file."""
    invalid_dataset_dict = {
        "version": "2.0",
        "class": "dataset",
        "href": "https://json-stat.org/samples/order.json",
        "label": "Demo of value ordering: what does not change, first",
        "id": ["A", "B", "C"],
        "size": [3, 2, 4],
        "value": [
            "A1B1C1",
            "A1B1C2",
            "A1B1C3",
            "A1B1C4",
            "A1B2C1",
            "A1B2C2",
            "A1B2C3",
            "A1B2C4",
            "A2B1C1",
            "A2B1C2",
            "A2B1C3",
            "A1B1C4",
            "A2B2C1",
            "A2B2C2",
            "A2B2C3",
            "A2B2C4",
            "A3B1C1",
            "A3B1C2",
            "A3B1C3",
            "A3B1C4",
            "A3B2C1",
            "A3B2C2",
            "A3B2C3",
            "A3B2C4",
        ],
    }

    try:
        Dataset(**invalid_dataset_dict)
        print("✅ Valid JSON-stat dataset!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    validate_invalid_dataset_from_file()
