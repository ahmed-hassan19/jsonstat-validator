"""Test cases for the Unit model."""

import pytest

from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat


class TestUnitValidCases:
    """Test cases for valid Unit objects within dimension categories."""

    def test_unit_with_decimals(self) -> None:
        """Test that a unit with decimals validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {
                    "gdp": {"decimals": 2},
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_with_symbol(self) -> None:
        """Test that a unit with symbol validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {
                    "gdp": {"symbol": "$"},
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_with_position_start(self) -> None:
        """Test that a unit with position 'start' validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {
                    "gdp": {
                        "symbol": "$",
                        "position": "start",
                    },
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_with_position_end(self) -> None:
        """Test that a unit with position 'end' validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["pop"],
                "unit": {
                    "pop": {
                        "symbol": "people",
                        "position": "end",
                    },
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_unit_with_all_properties(self) -> None:
        """Test that a unit with all properties validates successfully."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {
                    "gdp": {
                        "decimals": 1,
                        "symbol": "$",
                        "position": "start",
                    },
                },
            },
        }
        assert validate_jsonstat(dimension) is True

    def test_multiple_units(self) -> None:
        """Test that multiple units in a category validate successfully."""
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


class TestUnitInvalidCases:
    """Test cases for invalid Unit objects within dimension categories."""

    def test_unit_with_invalid_position(self) -> None:
        """Test that a unit with invalid position fails validation."""
        dimension = {
            "version": "2.0",
            "class": "dimension",
            "category": {
                "index": ["gdp"],
                "unit": {
                    "gdp": {
                        "symbol": "$",
                        "position": "invalid",  # Invalid position
                    },
                },
            },
        }
        with pytest.raises(JSONStatValidationError):
            validate_jsonstat(dimension)

    def test_unit_with_invalid_category_reference(self) -> None:
        """Test that a unit with invalid category reference fails validation."""
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
