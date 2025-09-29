"""Test cases for the Link model."""

import pytest

from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat


class TestLinkValidCases:
    """Test cases for valid Link objects within collections."""

    def test_link_with_dataset_item(self) -> None:
        """Test that a link with dataset item validates successfully."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/oecd.json",
                        "label": "OECD unemployment rate",
                    },
                ],
            },
        }
        assert validate_jsonstat(collection) is True

    def test_link_with_collection_item(self) -> None:
        """Test that a link with collection item validates successfully."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "collection",
                        "href": "https://json-stat.org/samples/collection.json",
                        "label": "Sample collection",
                    },
                ],
            },
        }
        assert validate_jsonstat(collection) is True

    def test_link_with_multiple_items(self) -> None:
        """Test that a link with multiple items validates successfully."""
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
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/canada.json",
                    },
                ],
            },
        }
        assert validate_jsonstat(collection) is True


class TestLinkInvalidCases:
    """Test cases for invalid Link objects within collections."""

    def test_link_with_invalid_href(self) -> None:
        """Test that a link with invalid href fails validation."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "dataset",
                        "href": "invalid-url",  # Invalid URL format
                    },
                ],
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(collection)

    def test_link_with_invalid_relation_type(self) -> None:
        """Test that a link with invalid relation type fails validation."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "dataset",
                        "href": "https://json-stat.org/samples/oecd.json",
                        "rel": "invalid_relation",  # Invalid relation type
                    },
                ],
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(collection)

    def test_link_with_invalid_class(self) -> None:
        """Test that a link with invalid class fails validation."""
        collection = {
            "version": "2.0",
            "class": "collection",
            "link": {
                "item": [
                    {
                        "class": "invalid_class",  # Invalid class
                        "href": "https://json-stat.org/samples/oecd.json",
                    },
                ],
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(collection)
