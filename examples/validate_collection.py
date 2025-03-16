#!/usr/bin/env python3
"""Example script to create, validate, and dump a JSON-stat collection."""

import json
from pprint import pprint

from jsonstat_validator.validator import JSONStatSchema, validate_jsonstat


def create_and_validate_collection():
    """Create and validate a JSON-stat collection."""
    # Create a collection object from a JSON-stat object
    try:
        collection = JSONStatSchema(
            version="2.0",
            class_="collection",
            href="https://json-stat.org/samples/collection.json",
            label="JSON-stat Dataset Sample Collection",
            updated="2015-12-21",
            link={
                "item": [
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/oecd.json",
                        "label": "Unemployment rate in the OECD countries 2003-2014",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/canada.json",
                        "label": "Population by sex and age group. Canada. 2012",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/galicia.json",
                        "label": (
                            "Population by province of residence, place of birth, "
                            "age, gender and year in Galicia"
                        ),
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/us-gsp.json",
                        "label": "US States by GSP and population",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/us-unr.json",
                        "label": "Unemployment Rates by County, 2012 Annual Averages",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/us-labor.json",
                        "label": "Labor Force Data by County, 2012 Annual Averages",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/order.json",
                        "label": "Demo of value ordering: what does not change, first",
                    },
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/hierarchy.json",
                        "label": "Demo of hierarchical dimension",
                    },
                ]
            },
        )
        # If model creation is successful, the object is valid by default
        # No need to explicitly call model_validate or validate_jsonstat
        pprint(collection.model_dump())
        print("✅ Valid JSON-stat collection!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


def validate_collection_from_file():
    """Validate a JSON-stat collection from a JSON file."""

    # Load the collection from a JSON file
    try:
        with open("tests/samples/collection.json", "r") as f:
            collection_dict = json.load(f)
    except FileNotFoundError:
        print("❌ Collection file not found")
        return

    # Validate the collection
    try:
        validate_jsonstat(collection_dict)
        print("✅ Valid JSON-stat collection!")
    except ValueError as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    create_and_validate_collection()
    validate_collection_from_file()
