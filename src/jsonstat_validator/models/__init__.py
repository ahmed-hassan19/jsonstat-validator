"""Models package for JSON-stat Validator.

This package contains all the Pydantic models for JSON-stat objects.
The main public API is exposed through the parent package.
"""

from __future__ import annotations

# Import all models to make them available when importing the models package
from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.category import Category
from jsonstat_validator.models.collection import Collection
from jsonstat_validator.models.dataset import Dataset, DatasetRole
from jsonstat_validator.models.dimension import DatasetDimension, Dimension
from jsonstat_validator.models.link import Link
from jsonstat_validator.models.unit import Unit

__all__ = [
    "Category",
    "Collection",
    "Dataset",
    "DatasetDimension",
    "DatasetRole",
    "Dimension",
    "JSONStatBaseModel",
    "JSONStatSchema",
    "Link",
    "Unit",
]
