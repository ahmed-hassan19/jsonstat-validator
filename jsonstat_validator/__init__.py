"""
JSON-stat validator.

A validator for the JSON-stat 2.0 format, a simple lightweight JSON format
for data dissemination. It is based in a cube model that arises from the
evidence that the most common form of aggregated data dissemination is the
tabular form. In this cube model, datasets are organized in dimensions,
dimensions are organized in categories.

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

__version__ = "0.1.1"
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
