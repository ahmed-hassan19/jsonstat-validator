"""
JSON-stat validator.

A validator for the JSON-stat 2.0 format, a simple lightweight format for data
interchange. It provides a way to exchange data associated to dimensions,
following the cube model that is so common in statistical offices.

For more information on JSON-stat, see: https://json-stat.org/
"""

from jsonstat_validator.validator import (
    Category,
    Collection,
    Dataset,
    DatasetRole,
    Dimension,
    JSONStatSchema,
    Link,
    Unit,
    validate_jsonstat,
)

__version__ = "0.1.0"
__all__ = [
    "Dataset",
    "Dimension",
    "Collection",
    "Link",
    "Unit",
    "Category",
    "DatasetRole",
    "JSONStatSchema",
    "validate_jsonstat",
]
