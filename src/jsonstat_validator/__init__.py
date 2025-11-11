"""JSON-stat validator.

A validator for the JSON-stat 2.0 format, a simple lightweight JSON format
for data dissemination. It is based in a cube model that arises from the
evidence that the most common form of aggregated data dissemination is the
tabular form. In this cube model, datasets are organized in dimensions,
dimensions are organized in categories.

For more information on JSON-stat, see: https://json-stat.org/
"""

from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.category import Category
from jsonstat_validator.models.collection import Collection
from jsonstat_validator.models.dataset import Dataset
from jsonstat_validator.models.dimension import Dimension
from jsonstat_validator.models.link import Link
from jsonstat_validator.models.unit import Unit
from jsonstat_validator.utils import JSONStatValidationError
from jsonstat_validator.validator import validate_jsonstat

# Rebuild models to resolve forward references
Link.model_rebuild()
Collection.model_rebuild()
Dataset.model_rebuild()
Dimension.model_rebuild()
JSONStatSchema.model_rebuild()

__version__ = "0.4.5"
__all__ = [
    "Category",
    "Collection",
    "Dataset",
    "Dimension",
    "JSONStatBaseModel",
    "JSONStatSchema",
    "JSONStatValidationError",
    "Link",
    "Unit",
    "validate_jsonstat",
]
