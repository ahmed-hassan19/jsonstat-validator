"""Test cases for the Collection model."""

import copy

import pytest

from jsonstat_validator.models.collection import Collection
from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat

# --- Valid base structure ---
MINIMAL_COLLECTION = {
    "version": "2.0",
    "class": "collection",
    "link": {
        "item": [
            {
                "class": "dataset",
                "href": "https://json-stat.org/samples/oecd.json",
                "label": "Unemployment rate in the OECD countries 2003-2014",
            },
        ],
    },
}


class TestCollectionValidCases:
    """Test cases for valid Collection objects."""

    def test_collection_with_nested_items(self) -> None:
        """Test that a collection with nested items validates successfully."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/oecd.json",
                    },
                    {
                        "class": "collection",
                        "href": "https://json-stat.org/samples/collection.json",
                    },
                ],
            },
        }
        assert validate_jsonstat(collection) is True

    def test_nested_collections(self) -> None:
        """Test that nested collections validate successfully."""
        # A collection containing a dataset and another collection
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/oecd.json",
                    },
                    {
                        "class": "collection",
                        "link": {
                            "item": [
                                {
                                    "class": "dataset",
                                    "href": "https://json-stat.org/samples/canada.json",
                                },
                            ],
                        },
                    },
                ],
            },
        }
        assert validate_jsonstat(collection) is True


class TestCollectionInvalidCases:
    """Test cases for invalid Collection objects."""

    def test_invalid_collection_link_key(self) -> None:
        """Test that invalid collection link key fails validation."""
        collection = copy.deepcopy(MINIMAL_COLLECTION)
        collection["link"]["invalid_key"] = "invalid"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(collection)

    def test_link_validation(self) -> None:
        """Test that invalid link structure fails validation."""
        collection = copy.deepcopy(MINIMAL_COLLECTION)
        collection["link"]["item"][0]["href"] = "invalid-url"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(collection)


class TestCollectionClassValues:
    """Test cases for class values in Collection objects."""

    def test_valid_class_value(self) -> None:
        """Test that valid class value is accepted."""
        model = Collection.model_validate(MINIMAL_COLLECTION)
        assert model.class_ == "collection"

    def test_invalid_class_value(self) -> None:
        """Test that an invalid class value fails validation."""
        data = copy.deepcopy(MINIMAL_COLLECTION)
        data["class"] = "invalid_class"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_invalid_updated_date_format(self) -> None:
        """Test that invalid updated date format fails validation."""
        data = copy.deepcopy(MINIMAL_COLLECTION)
        data["updated"] = "invalid-date-format"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_collection_missing_item_relation(self) -> None:
        """Test that collection without 'item' relation type fails validation."""
        data = copy.deepcopy(MINIMAL_COLLECTION)
        data["link"] = {"self": [{"href": "https://example.com"}]}
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)
