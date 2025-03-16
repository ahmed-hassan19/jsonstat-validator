"""Custom test cases for the JSON-stat validator tool."""

import copy
from datetime import datetime

import pytest

from jsonstat_validator import Collection, Dataset, Dimension, validate_jsonstat


# --- Helper functions ---
def current_iso8601():
    """Return the current ISO 8601 datetime as a string."""
    return datetime.now().isoformat()


# --- Valid base structures ---
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

MINIMAL_DIMENSION = {
    "version": "2.0",
    "class": "dimension",
    "category": {"index": ["male", "female"]},
}

MINIMAL_COLLECTION = {
    "version": "2.0",
    "class": "collection",
    "link": {
        "item": [
            {
                "class": "dataset",
                "href": "https://json-stat.org/samples/oecd.json",
                "label": "Unemployment rate in the OECD countries 2003-2014",
            }
        ]
    },
}


class TestValidCases:
    """Test cases for valid JSON-stat objects."""

    def test_minimal_dataset(self):
        """Test that a minimal dataset validates successfully."""
        assert validate_jsonstat(MINIMAL_DATASET) is True

    def test_sparse_dataset_values(self):
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

    def test_dataset_with_roles(self):
        """Test that a dataset with roles validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["role"] = {
            "time": ["time"],
            "geo": ["geo"],
        }
        assert validate_jsonstat(data) is True

    def test_dimension_with_label(self):
        """Test that a dimension with a label validates successfully."""
        data = copy.deepcopy(MINIMAL_DIMENSION)
        data["label"] = "Gender"
        data["category"]["label"] = {"male": "Male", "female": "Female"}
        assert validate_jsonstat(data) is True

    def test_collection_with_nested_items(self):
        """Test that a collection with nested items validates successfully."""
        data = copy.deepcopy(MINIMAL_COLLECTION)
        data["link"]["item"].append(
            {
                "class": "collection",
                "href": "https://json-stat.org/samples/collection.json",
                "label": "A nested collection",
            }
        )
        assert validate_jsonstat(data) is True


class TestInvalidCases:
    """Test cases for invalid JSON-stat objects."""

    def test_missing_required_field(self):
        """Test that a dataset missing a required field fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        del data["id"]
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_size_length_mismatch(self):
        """Test that a dataset with mismatched size and id length fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["size"] = [2, 3, 4]  # One more than id length
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_invalid_status_format(self):
        """Test that a dataset with an invalid status format fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["status"] = ["a", "b", "c"]  # Too few elements
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_missing_dimension_definition(self):
        """Test that a dataset with a missing dimension definition fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["id"] = ["time", "geo", "metric"]  # Added a new dimension
        data["size"] = [2, 3, 2]  # Updated size accordingly
        # But the dimension is not defined
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_invalid_collection_link_key(self):
        """Test that a collection with an invalid link key fails validation."""
        data = copy.deepcopy(MINIMAL_COLLECTION)
        # Collections must use 'item' as the relation type
        data["link"] = {"invalid_key": data["link"]["item"]}
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_category_missing_index_and_label(self):
        """Test that a category missing both index and label fails validation."""
        dimension = copy.deepcopy(MINIMAL_DIMENSION)
        # Remove index and don't provide label
        del dimension["category"]["index"]
        with pytest.raises(ValueError):
            validate_jsonstat(dimension)


class TestTypeValidation:
    """Test cases for type validation in JSON-stat objects."""

    @pytest.mark.parametrize(
        "field,value",
        [
            ("version", 2.0),  # Should be a string
            ("class", "invalid_class"),  # Invalid class value
            ("size", ["not_number"]),  # Should be integers
            ("id", "not_list"),  # Should be a list
            ("value", "not_array_or_dict"),  # Should be array or dict
        ],
    )
    def test_invalid_types(self, field, value):
        """Test that invalid types fail validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data[field] = value
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_link_validation(self):
        """Test that link validation works correctly."""
        collection = copy.deepcopy(MINIMAL_COLLECTION)
        # Invalid URL format
        collection["link"]["item"][0]["href"] = "invalid-url"
        with pytest.raises(ValueError):
            validate_jsonstat(collection)


class TestClassValues:
    """Test cases for class values in JSON-stat objects."""

    @pytest.mark.parametrize(
        "model_class,input_data,expected",
        [
            (Dataset, MINIMAL_DATASET, "dataset"),
            (Dimension, MINIMAL_DIMENSION, "dimension"),
            (Collection, MINIMAL_COLLECTION, "collection"),
        ],
    )
    def test_class_values(self, model_class, input_data, expected):
        """Test that class values are validated correctly."""
        model = model_class.model_validate(input_data)
        assert model.class_ == expected

    def test_invalid_class_value(self):
        """Test that an invalid class value fails validation."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["class"] = "invalid_class"
        with pytest.raises(ValueError):
            validate_jsonstat(data)


class TestComplexStructures:
    """Test cases for complex JSON-stat structures."""

    def test_nested_collections(self):
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
                                }
                            ]
                        },
                    },
                ]
            },
        }
        assert validate_jsonstat(collection) is True

    def test_multi_level_category_hierarchy(self):
        """Test that a multi-level category hierarchy validates successfully."""
        dimension = copy.deepcopy(MINIMAL_DIMENSION)
        dimension["category"]["index"] = ["total", "a", "a1", "a2", "b", "b1", "b2"]
        dimension["category"]["child"] = {
            "total": ["a", "b"],
            "a": ["a1", "a2"],
            "b": ["b1", "b2"],
        }
        assert validate_jsonstat(dimension) is True

    def test_mixed_value_status_formats(self):
        """Test that a dataset with mixed value and status formats validates."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = {
            "0:0": 1,
            "0:1": 2,
            "0:2": 3,
            "1:0": 4,
            "1:1": 5,
            "1:2": 6,
        }
        data["status"] = {"0:0": "a", "1:1": "b"}
        assert validate_jsonstat(data) is True


class TestEdgeCases:
    """Test cases for edge cases in JSON-stat objects."""

    def test_empty_dataset_values(self):
        """Test that a dataset with empty values validates successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = []
        data["size"] = []
        data["id"] = []
        data["dimension"] = {}
        assert validate_jsonstat(data) is True

    def test_single_category_dimension(self):
        """Test that a dimension with a single category validates without index."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {"label": {"a": "A"}},
        }
        assert validate_jsonstat(dimension) is True

    def test_iso8601_datetime_format(self):
        """Test that ISO 8601 datetime formats are validated correctly."""
        data = copy.deepcopy(MINIMAL_DATASET)
        # Valid formats
        data["updated"] = "2022-01-01T12:30:45Z"
        assert validate_jsonstat(data) is True
        data["updated"] = "2022-01-01T12:30:45+01:00"
        assert validate_jsonstat(data) is True
        # Invalid format
        data["updated"] = "01/01/2022"
        with pytest.raises(ValueError):
            validate_jsonstat(data)

    def test_extension_fields(self):
        """Test that extension fields are allowed in JSON-stat objects."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["extension"] = {"custom_field": "custom_value"}
        assert validate_jsonstat(data) is True

    def test_mixed_value_types(self):
        """Test that datasets with mixed value types validate successfully."""
        data = copy.deepcopy(MINIMAL_DATASET)
        data["value"] = [1, "2", 3.0, None, 5, 6]
        assert validate_jsonstat(data) is True

    def test_unit_position_validation(self):
        """Test that unit position is validated correctly."""
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

        # Invalid position value
        dimension["category"]["unit"]["gdp"]["position"] = "invalid"
        with pytest.raises(ValueError):
            validate_jsonstat(dimension)

    def test_coordinates_validation(self):
        """Test that coordinates are validated correctly."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["US", "CA", "MX"],
                "coordinates": {
                    "US": [-98.5795, 39.8282],
                    "CA": [-106.3468, 56.1304],
                    "MX": [-102.5528, 23.6345],
                },
            },
        }
        assert validate_jsonstat(dimension) is True
        # Invalid coordinates format
        dimension["category"]["coordinates"]["US"] = [-98.5795]  # Missing latitude
        with pytest.raises(ValueError):
            validate_jsonstat(dimension)

    def test_child_parent_validation(self):
        """Test that child references to parent categories are validated."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["total", "a", "b"],
                "child": {"total": ["a", "b"]},
            },
        }
        assert validate_jsonstat(dimension) is True
        # Invalid parent reference
        dimension["category"]["child"] = {"invalid_parent": ["a", "b"]}
        with pytest.raises(ValueError):
            validate_jsonstat(dimension)

    def test_unit_category_validation(self):
        """Test that unit references to categories are validated."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp", "pop"],
                "unit": {
                    "gdp": {"decimals": 1},
                    "pop": {"decimals": 0},
                },
            },
        }
        assert validate_jsonstat(dimension) is True
        # Invalid category reference
        dimension["category"]["unit"] = {"invalid_category": {"decimals": 1}}
        with pytest.raises(ValueError):
            validate_jsonstat(dimension)

    def test_multi_role_validation(self):
        """Test that dimensions referenced in multiple roles are validated."""
        data = copy.deepcopy(MINIMAL_DATASET)
        # Valid: different dimensions in different roles
        data["role"] = {
            "time": ["time"],
            "geo": ["geo"],
        }
        assert validate_jsonstat(data) is True
        # Invalid: same dimension in multiple roles
        data["role"] = {
            "time": ["time", "geo"],
            "geo": ["geo"],
        }
        with pytest.raises(ValueError):
            validate_jsonstat(data)
