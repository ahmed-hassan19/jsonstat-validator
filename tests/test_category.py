"""Test cases for the Category model."""

import pytest

from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat


class TestCategoryValidCases:
    """Test cases for valid Category objects within dimensions."""

    def test_category_with_index_list(self) -> None:
        """Test that a category with index as list validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {"index": ["male", "female"]},
        }
        assert validate_jsonstat(dimension) is True

    def test_category_with_index_dict(self) -> None:
        """Test that a category with index as dict validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {"index": {"male": 0, "female": 1}},
        }
        assert validate_jsonstat(dimension) is True

    def test_category_with_labels(self) -> None:
        """Test that a category with labels validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["m", "f"],
                "label": {"m": "Male", "f": "Female"},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_category_with_coordinates(self) -> None:
        """Test that a category with coordinates validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["north", "south"],
                "coordinates": {"north": [45.0, -75.0], "south": [25.0, -80.0]},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_category_with_units(self) -> None:
        """Test that a category with units validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {"gdp": {"decimals": 2, "symbol": "$"}},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_category_with_child_hierarchy(self) -> None:
        """Test that a category with child hierarchy validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["total", "male", "female", "boy", "girl"],
                "child": {"male": ["boy"], "female": ["girl"]},
            },
        }
        assert validate_jsonstat(dimension) is True


class TestCategoryInvalidCases:
    """Test cases for invalid Category objects within dimensions."""

    def test_category_missing_index_and_label(self) -> None:
        """Test that a category missing both index and label fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {},  # No index or label
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_invalid_coordinates(self) -> None:
        """Test that invalid coordinates format fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["location"],
                "coordinates": {"location": "invalid"},  # Should be array
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_invalid_unit_reference(self) -> None:
        """Test that invalid unit reference fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "invalid_category": {"decimals": 1},  # Category not in index
                },
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_invalid_child_reference(self) -> None:
        """Test that invalid child reference fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["total", "male"],
                "child": {"female": ["girl"]},  # female not in index
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_coordinates_invalid_category_id(self) -> None:
        """Test that coordinates with invalid category ID fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["north", "south"],
                "coordinates": {"east": [45.0, -75.0]},  # east not in index
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_coordinates_wrong_length(self) -> None:
        """Test that coordinates with wrong length fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["location"],
                "coordinates": {"location": [45.0]},  # Should have 2 numbers
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_coordinates_not_list(self) -> None:
        """Test that coordinates with non-list value fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["location"],
                "coordinates": {"location": 45.0},  # Should be list
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_coordinates_invalid_with_labels(self) -> None:
        """Test that coordinates with invalid category ID fails when using labels."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "label": {"north": "North Region", "south": "South Region"},
                "coordinates": {"east": [45.0, -75.0]},  # east not in label
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_category_index_label_key_mismatch(self) -> None:
        """Test that mismatched keys between index and label fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["male", "female"],
                "label": {"m": "Male", "f": "Female"},  # Different keys
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)
