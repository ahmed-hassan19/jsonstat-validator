"""Category model for JSON-stat."""

from __future__ import annotations

from pydantic import Field, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel
from jsonstat_validator.models.unit import Unit
from jsonstat_validator.utils import JSONStatValidationError


class Category(JSONStatBaseModel):
    """Category of a dimension.

    It is used to describe the possible values of a dimension.
    """

    index: list[str] | dict[str, int] | None = Field(
        default=None,
        description=(
            "It is used to order the possible values (categories) of a dimension. "
            "The order of the categories and the order of the dimensions themselves "
            "determine the order of the data in the value array. While the dimensions "
            "order has only this functional role (and therefore any order chosen by "
            "the provider is valid), the categories order has also a presentation "
            "role: it is assumed that the categories are sorted in a meaningful order "
            "and that the consumer can rely on it when displaying the information. "
            "- index is required unless the dimension is a constant dimension "
            "(dimension with a single category). When a dimension has only one "
            "category, the index property is indeed unnecessary. In the case that "
            "a category index is not provided, a category label must be included."
        ),
    )
    label: dict[str, str] | None = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    child: dict[str, list[str]] | None = Field(
        default=None,
        description=(
            "It is used to describe the hierarchical relationship between different "
            "categories. It takes the form of an object where the key is the ID of "
            "the parent category and the value is an array of the IDs of the child "
            "categories. It is also a way of exposing a certain category as a total."
        ),
    )
    coordinates: dict[str, list[float | int]] | None = Field(
        default=None,
        description=(
            "It can be used to assign longitude/latitude geographic coordinates "
            "to the categories of a dimension with a geo role. It takes the form "
            "of an object where keys are category IDs and values are an array of "
            "two numbers (longitude, latitude)."
        ),
    )
    unit: dict[str, Unit] | None = Field(
        default=None,
        description=(
            "It can be used to assign unit of measure metadata to the categories "
            "of a dimension with a metric role."
        ),
    )
    note: dict[str, list[str]] | None = Field(
        default=None,
        description=(
            "note allows to assign annotations to datasets (array), dimensions "
            "(array) and categories (object). To assign annotations to individual "
            "data, use status: https://json-stat.org/full/#status."
        ),
    )

    @model_validator(mode="after")
    def validate_category(self) -> Category:
        """Category-wide validation checks."""
        # index, label: at least one of index or label is required
        if self.index is None and self.label is None:
            raise JSONStatValidationError(
                "At least one of `index` or `label` is required."
            )

        # index, label: same keys if both are dictionaries
        if self.index and self.label and isinstance(self.label, dict):
            index_keys = (
                set(self.index) if isinstance(self.index, list) else set(self.index)
            )
            if index_keys != set(self.label):
                raise JSONStatValidationError(
                    "`index` and `label` must have the same keys."
                )

        # index list: unique IDs
        if isinstance(self.index, list) and len(set(self.index)) != len(self.index):
            raise JSONStatValidationError(
                "Category IDs in `index` list must be unique."
            )

        # coordinates: keys must be valid categories
        # and values must be length-2 lists of numbers (longitude, latitude).
        if self.coordinates:
            for key, value in self.coordinates.items():
                if (self.index and key not in self.index) or (
                    self.label and key not in self.label
                ):
                    raise JSONStatValidationError(
                        f"Trying to set coordinates for category ID: {key} "
                        "but it is not defined neither in `index` nor in `label`."
                    )
                if not isinstance(value, list) or len(value) != 2:
                    raise JSONStatValidationError(
                        f"Coordinates for category {key} must be a list of 2 numbers: (longitude, latitude)."
                    )

        # child: references an existing parent
        if self.child:
            valid_ids = (
                set(self.index)
                if isinstance(self.index, list)
                else set(self.index or [])
            )
            valid_ids |= set(self.label or [])
            for parent, children in self.child.items():
                if parent not in valid_ids:
                    raise JSONStatValidationError(
                        f"Invalid parent: {parent} in the `child` field."
                    )
                for ch in children:
                    if ch not in valid_ids:
                        raise JSONStatValidationError(
                            f"Invalid child: {ch} in `child[{parent}]`."
                        )

        # unit: keys must exist
        if self.unit:
            valid_ids = (
                set(self.index)
                if isinstance(self.index, list)
                else set(self.index or [])
            )
            valid_ids |= set(self.label or [])
            for key in self.unit:
                if key not in valid_ids:
                    raise JSONStatValidationError(
                        f"Invalid unit: {key} in the `unit` field."
                    )
        return self
