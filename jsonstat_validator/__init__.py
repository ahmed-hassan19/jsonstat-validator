"""JSON-stat validator.

A validator for the JSON-stat 2.0 format, a simple lightweight JSON format
for data dissemination. It is based in a cube model that arises from the
evidence that the most common form of aggregated data dissemination is the
tabular form. In this cube model, datasets are organized in dimensions,
dimensions are organized in categories.

For more information on JSON-stat, see: https://json-stat.org/
"""

from jsonstat_validator.models import (
    Category,
    Collection,
    Dataset,
    Dimension,
    JSONStatBaseModel,
    JSONStatSchema,
)
from jsonstat_validator.validator import validate_jsonstat

__version__ = "0.2.2"
__all__ = [
    "Category",
    "Collection",
    "Dataset",
    "Dimension",
    "JSONStatBaseModel",
    "JSONStatSchema",
    "validate_jsonstat",
]
