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
    coordinates: dict[str, list[float]] | None = Field(
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
        # Ensure at least one of index or label fields is provided
        if self.index is None and self.label is None:
            error_message = "At least one of `index` or `label` is required."
            raise JSONStatValidationError(error_message)

        # Ensure index and label have the same keys if both are dictionaries
        if self.index and self.label and isinstance(self.label, dict):
            index_keys = (
                set(self.index) if isinstance(self.index, list) else set(self.index)
            )
            if index_keys != set(self.label):
                error_message = "`index` and `label` must have the same keys."
                raise JSONStatValidationError(error_message)

        # Ensure coordinates are a dictionary where keys are category IDs
        # and values are an array of two numbers (longitude, latitude).
        if self.coordinates:
            for key in self.coordinates:
                value = self.coordinates[key]
                if (self.index and key not in self.index) or (
                    self.label and key not in self.label
                ):
                    error_message = (
                        f"Trying to set coordinates for category ID: {key} "
                        "but it is not defined neither in `index` nor in `label`."
                    )
                    raise JSONStatValidationError(error_message)
                expected_length = 2
                if not isinstance(value, list) or len(value) != expected_length:
                    error_message = (
                        f"Coordinates for category {key} must be a list of "
                        f"{expected_length} numbers."
                    )
                    raise JSONStatValidationError(error_message)

        # Ensure child references an existing parent
        if self.child:
            for parent in self.child:
                if (self.index and parent not in self.index) or (
                    self.label and parent not in self.label
                ):
                    error_message = (
                        f"Invalid parent: {parent} in the `child` field. "
                        "It is not defined neither in `index` nor in `label`."
                    )
                    raise JSONStatValidationError(error_message)

        # Ensure unit references an existing category
        if self.unit:
            for key in self.unit:
                if (self.index and key not in self.index) or (
                    self.label and key not in self.label
                ):
                    error_message = (
                        f"Invalid unit: {key} in the `unit` field. "
                        "It is not defined neither in `index` nor in `label`."
                    )
                    raise JSONStatValidationError(error_message)
        return self
