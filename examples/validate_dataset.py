#!/usr/bin/env python3
"""Example script to create, validate, and dump a JSON-stat dataset."""

import json
from pprint import pprint

from jsonstat_validator.validator import JSONStatSchema, validate_jsonstat


def create_and_validate_dataset():
    """Create and validate a JSON-stat dataset."""
    # Create a dataset object from a JSON-stat object
    try:
        dataset = JSONStatSchema(
            {
                "version": "2.0",
                "class": "dataset",
                "href": "https://json-stat.org/samples/order.json",
                "label": "Demo of value ordering: what does not change, first",
                "id": ["A", "B", "C"],
                "size": [3, 2, 4],
                "dimension": {
                    "A": {
                        "label": "A: 3-categories dimension",
                        "category": {"index": ["1", "2", "3"]},
                    },
                    "B": {
                        "label": "B: 2-categories dimension",
                        "category": {"index": ["1", "2"]},
                    },
                    "C": {
                        "label": "C: 4-categories dimension",
                        "category": {"index": ["1", "2", "3", "4"]},
                    },
                },
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
        )
        # If model creation is successful, the object is valid by default
        # No need to explicitly call model_validate or validate_jsonstat
        pprint(dataset.model_dump())
        print("✅ Valid JSON-stat dataset!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


def validate_dataset_from_file():
    """Validate a JSON-stat dataset from a JSON file."""

    # Load the dataset from a JSON file
    try:
        with open("tests/samples/order.json", "r") as f:
            dataset_dict = json.load(f)
    except FileNotFoundError:
        print("❌ Dataset file not found")
        return

    # Validate the dataset
    try:
        validate_jsonstat(dataset_dict)
        print("✅ Valid JSON-stat dataset!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    create_and_validate_dataset()
    validate_dataset_from_file()
