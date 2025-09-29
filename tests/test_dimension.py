"""Test cases for the Dimension model."""

import copy

import pytest

from jsonstat_validator.models.dimension import Dimension
from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat

# --- Valid base structure ---
MINIMAL_DIMENSION = {
    "version": "2.0",
    "class": "dimension",
    "category": {"index": ["male", "female"]},
}


class TestDimensionValidCases:
    """Test cases for valid Dimension objects."""

    def test_dimension_with_label(self) -> None:
        """Test that a dimension with label validates successfully."""
        dimension = copy.deepcopy(MINIMAL_DIMENSION)
        dimension["label"] = "Gender"
        assert validate_jsonstat(dimension) is True

    def test_single_category_dimension(self) -> None:
        """Test that a single category dimension validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {"index": ["total"]},
        }
        assert validate_jsonstat(dimension) is True

    def test_multi_level_category_hierarchy(self) -> None:
        """Test that multi-level category hierarchy validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["total", "male", "female"],
                "child": {"male": ["boy"], "female": ["girl"]},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_position_validation(self) -> None:
        """Test that unit position validation works correctly."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "gdp": {
                        "decimals": 1,
                        "symbol": "$",
                        "position": "start",
                    },
                    "pop": {
                        "decimals": 0,
                        "symbol": "people",
                        "position": "end",
                    },
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_coordinates_validation(self) -> None:
        """Test that coordinates validation works correctly."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["north", "south"],
                "coordinates": {"north": [45.0, -75.0], "south": [25.0, -80.0]},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_child_parent_validation_valid(self) -> None:
        """Test that child-parent validation works for valid references."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["total", "male", "female", "boy", "girl"],
                "child": {"male": ["boy"], "female": ["girl"]},
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_category_validation_valid(self) -> None:
        """Test that unit-category validation works for valid references."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "gdp": {"decimals": 1, "symbol": "$"},
                    "pop": {"decimals": 0, "symbol": "people"},
                },
            },
        }
        assert validate_jsonstat(dimension) is True


class TestDimensionInvalidCases:
    """Test cases for invalid Dimension objects."""

    def test_invalid_unit_position(self) -> None:
        """Test that invalid unit position fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "gdp": {
                        "decimals": 1,
                        "symbol": "$",
                        "position": "invalid",  # Invalid position
                    },
                },
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_invalid_coordinates_format(self) -> None:
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

    def test_invalid_child_parent_reference(self) -> None:
        """Test that invalid child-parent reference fails validation."""
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

    def test_invalid_unit_category_reference(self) -> None:
        """Test that invalid unit-category reference fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "invalid_category": {"decimals": 1},  # Not in index
                },
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)


class TestDimensionClassValues:
    """Test cases for class values in Dimension objects."""

    def test_valid_class_value(self) -> None:
        """Test that valid class value is accepted."""
        model = Dimension.model_validate(MINIMAL_DIMENSION)
        assert model.class_ == "dimension"

    def test_invalid_class_value(self) -> None:
        """Test that an invalid class value fails validation."""
        data = copy.deepcopy(MINIMAL_DIMENSION)
        data["class"] = "invalid_class"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_invalid_updated_date_format(self) -> None:
        """Test that invalid updated date format fails validation."""
        data = copy.deepcopy(MINIMAL_DIMENSION)
        data["updated"] = "invalid-date-format"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_dimension_missing_category_and_href(self) -> None:
        """Test that dimension without category or href fails validation."""
        data = {
            "version": "2.0",
            "class": "dimension",
            # Missing both category and href
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_dataset_dimension_invalid_updated_date(self) -> None:
        """Test that DatasetDimension with invalid updated date fails validation."""
        # This tests the DatasetDimension.validate_updated_date method
        from jsonstat_validator.models.dimension import DatasetDimension

        data = {"category": {"index": ["test"]}, "updated": "invalid-date-format"}
        with pytest.raises(JSONStatValidationError):
            DatasetDimension.model_validate(data)

    def test_dimension_valid_updated_date(self) -> None:
        """Test that valid updated date passes validation."""
        data = copy.deepcopy(MINIMAL_DIMENSION)
        data["updated"] = "2023-01-01T00:00:00Z"
        assert validate_jsonstat(data) is True

    def test_dataset_dimension_valid_updated_date(self) -> None:
        """Test that DatasetDimension with valid updated date passes validation."""
        from jsonstat_validator.models.dimension import DatasetDimension

        data = {"category": {"index": ["test"]}, "updated": "2023-01-01T00:00:00Z"}
        dimension = DatasetDimension.model_validate(data)
        assert dimension.updated == "2023-01-01T00:00:00Z"

    def test_dataset_dimension_missing_category_and_href(self) -> None:
        """Test that DatasetDimension without category or href fails validation."""
        from jsonstat_validator.models.dimension import DatasetDimension

        data = {}  # No category or href
        with pytest.raises(JSONStatValidationError):
            DatasetDimension.model_validate(data)
