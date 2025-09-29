"""Test cases for the Dataset model."""

import copy
from typing import Any

import pytest

from jsonstat_validator.models.dataset import Dataset
from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat

# ruff: noqa: ANN401

# --- Valid base structure ---
MINIMAL_DATASET = {
    "version": "2.0",
    "class": "dataset",
    "id": ["time", "geo"],
    "size": [2, 3],
    "value": [1, 2, 3, 4, 5, 6],
    "dimension": {
        "time": {"category": {"index": ["2020", "2021"]}},
        "geo": {"category": {"index": {"US": 0, "EU": 1, "AS": 2}}},
    },
}


class TestDatasetValidCases:
    """Test cases for valid Dataset objects."""

    def test_minimal_dataset(self) -> None:
        """Test that a minimal dataset validates successfully."""
        assert validate_jsonstat(MINIMAL_DATASET) is True

    def test_sparse_dataset_values(self) -> None:
        """Test that a dataset with sparse values validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = {
            "0:0": 1,
            "0:1": 2,
            "0:2": 3,
            "1:0": 4,
            "1:1": 5,
            "1:2": 6,
        }
        assert validate_jsonstat(data) is True

    def test_dataset_with_roles(self) -> None:
        """Test that a dataset with roles validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["role"] = {
            "time": ["time"],
            "geo": ["geo"],
        }
        assert validate_jsonstat(data) is True

    def test_empty_dataset_values(self) -> None:
        """Test that a dataset with empty values validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = []
        data["size"] = [0]
        data["id"] = ["empty"]
        data["dimension"] = {"empty": {"category": {"index": []}}}
        assert validate_jsonstat(data) is True

    def test_iso8601_datetime_format(self) -> None:
        """Test that ISO8601 datetime format validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["dimension"]["time"]["category"]["index"] = [
            "2020-01-01T00:00:00Z",
            "2021-01-01T00:00:00Z",
        ]
        assert validate_jsonstat(data) is True

    def test_extension_fields(self) -> None:
        """Test that extension fields are allowed."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["extension"] = {"custom_field": "custom_value"}
        assert validate_jsonstat(data) is True

    def test_mixed_value_types(self) -> None:
        """Test that mixed value types validate successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = [1, 2.5, None, 4, "5", 6]
        assert validate_jsonstat(data) is True

    def test_mixed_value_status_formats(self) -> None:
        """Test that mixed value and status formats validate successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = [1, 2, 3, 4, 5, 6]
        data["status"] = ["a", "b", "c", "d", "e", "f"]
        assert validate_jsonstat(data) is True


class TestDatasetInvalidCases:
    """Test cases for invalid Dataset objects."""

    def test_missing_required_field(self) -> None:
        """Test that missing required fields fail validation."""
        data = {"version": "2.0", "class": "dataset"}
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_size_length_mismatch(self) -> None:
        """Test that size/id length mismatch fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["size"] = [2]  # Should match length of id
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_missing_dimension_definition(self) -> None:
        """Test that missing dimension definition fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        del data["dimension"]["time"]
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)


class TestDatasetTypeValidation:
    """Test cases for Dataset type validation."""

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("version", 2.0),
            ("size", "value1"),
            ("id", "not_list"),
            ("value", "not_array_or_dict"),
        ],
    )
    def test_invalid_types(self, field: str, value: Any) -> None:
        """Test that invalid types fail validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data[field] = value
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)


class TestDatasetClassValues:
    """Test cases for class values in Dataset objects."""

    def test_valid_class_value(self) -> None:
        """Test that valid class value is accepted."""
        model = Dataset.model_validate(MINIMAL_DATASET)
        assert model.class_ == "dataset"

    def test_invalid_class_value(self) -> None:
        """Test that an invalid class value fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["class"] = "invalid_class"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_empty_dataset_role_validation(self) -> None:
        """Test that empty role fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["role"] = {}  # Empty role
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_invalid_updated_date_format(self) -> None:
        """Test that invalid updated date format fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["updated"] = "invalid-date-format"
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_duplicate_dimension_in_roles(self) -> None:
        """Test that duplicate dimension in roles fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["role"] = {
            "time": ["time"],
            "geo": ["time"],  # time appears in both roles
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)

    def test_status_length_mismatch(self) -> None:
        """Test that status length mismatch fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["status"] = ["A", "B"]  # Should match value length (6) or be 1
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(data)
