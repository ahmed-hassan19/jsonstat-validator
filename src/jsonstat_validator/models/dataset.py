"""Dataset model for JSON-stat."""

from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import Field, field_validator, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.dimension import DatasetDimension
from jsonstat_validator.models.link import Link
from jsonstat_validator.utils import JSONStatValidationError, is_valid_iso_date


class DatasetRole(JSONStatBaseModel):
    """Role of a dataset."""

    time: list[str] | None = Field(
        default=None,
        description=(
            "It can be used to assign a time role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )
    geo: list[str] | None = Field(
        default=None,
        description=(
            "It can be used to assign a spatial role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )
    metric: list[str] | None = Field(
        default=None,
        description=(
            "It can be used to assign a metric role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )

    @model_validator(mode="after")
    def validate_dataset_role(self) -> DatasetRole:
        """Dataset role-wide validation checks."""
        if not self.time and not self.geo and not self.metric:
            error_message = "At least one role must be provided."
            raise JSONStatValidationError(error_message)
        return self


class Dataset(JSONStatBaseModel):
    """JSON-stat dataset."""

    version: str = Field(
        default="2.0",
        description=(
            "It declares the JSON-stat version of the response. The goal "
            "of this property is to help clients parsing that particular response."
        ),
    )
    class_: Literal["dataset"] = Field(
        default="dataset",
        alias="class",
        description=(
            "JSON-stat supports several classes of responses. "
            "Possible values of class are: dataset, dimension and collection."
        ),
    )
    href: str | None = Field(
        default=None,
        description=(
            "It specifies a URL. Providers can use this property to avoid "
            "sending information that is shared between different requests "
            "(for example, dimensions)."
        ),
    )
    label: str | None = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    source: str | None = Field(
        default=None,
        description=(
            "It contains a language-dependent short text describing the source "
            "of the dataset."
        ),
    )
    updated: str | None = Field(
        default=None,
        description=(
            "It contains the update time of the dataset. It is a string representing "
            "a date in an ISO 8601 format recognized by the Javascript Date.parse "
            "method (see ECMA-262 Date Time String Format: "
            "https://262.ecma-international.org/6.0/#sec-date-time-string-format)."
        ),
    )
    id: list[str] = Field(description="It contains an ordered list of dimension IDs.")
    size: list[int] = Field(
        description=(
            "It contains the number (integer) of categories (possible values) "
            "of each dimension in the dataset. It has the same number of elements "
            "and in the same order as in id."
        ),
    )
    role: DatasetRole | None = Field(
        default=None,
        description=(
            "It can be used to assign special roles to dimensions. "
            "At this moment, possible roles are: time, geo and metric. "
            "A role can be shared by several dimensions."
            "We differ from the specification in that the role is required, not optional"
        ),
    )
    value: list[float | int | str | None] | dict[str, float | int | str | None] = Field(
        description=(
            "It contains the data sorted according to the dataset dimensions. "
            "It usually takes the form of an array where missing values are "
            "expressed as nulls."
        ),
    )
    status: str | list[str] | dict[str, str] | None = Field(
        default=None,
        description=(
            "It contains metadata at the observation level. When it takes an "
            "array form of the same size of value, it assigns a status to each "
            "data by position. When it takes a dictionary form, it assigns a "
            "status to each data by key."
        ),
    )

    dimension: dict[str, DatasetDimension] = Field(
        description=(
            "The dimension property contains information about the dimensions of "
            "the dataset. dimension must have properties "
            "(see https://json-stat.org/full/#dimensionid) with "
            "the same names of each element in the id array."
        ),
    )
    note: list[str] | None = Field(
        default=None,
        description=(
            "note allows to assign annotations to datasets (array), dimensions "
            "(array) and categories (object). To assign annotations to individual "
            "data, use status: https://json-stat.org/full/#status."
        ),
    )
    extension: dict | None = Field(
        default=None,
        description=(
            "Extension allows JSON-stat to be extended for particular needs. "
            "Providers are free to define where they include this property and "
            "what children are allowed in each case."
        ),
    )
    link: dict[str, list[Link | JSONStatSchema]] | None = Field(
        default=None,
        description=(
            "It is used to provide a list of links related to a dataset or a dimension, "
            "sorted by relation (see https://json-stat.org/full/#relationid)."
        ),
    )

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: str | None) -> str | None:
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            error_message = f"Updated date: '{v}' is an invalid ISO 8601 format."
            raise JSONStatValidationError(error_message)
        return v

    @field_validator("role", mode="after")
    @classmethod
    def validate_role(cls, v: DatasetRole | None) -> DatasetRole | None:
        """Validate that role references are valid."""
        if v:
            all_values = [
                value
                for values in v.model_dump().values()
                if values is not None
                for value in values
            ]
            duplicates = [
                item for item, count in Counter(all_values).items() if count > 1
            ]
            if duplicates:
                error_message = (
                    f"Dimension(s): {', '.join(duplicates)} referenced in multiple "
                    "roles. Each dimension can only be referenced in one role."
                )
                raise JSONStatValidationError(error_message)
        return v

    @model_validator(mode="after")
    def validate_dataset(self) -> Dataset:
        """Dataset-wide validation checks."""
        # Validate size matches id length

        if len(self.size) != len(self.id):
            error_message = (
                f"Size array length ({len(self.size)}) "
                f"must match ID array length ({len(self.id)})"
            )
            raise JSONStatValidationError(error_message)

        # Validate status format
        if isinstance(self.status, list) and len(self.status) not in (
            len(self.value),
            1,
        ):
            error_message = (
                "Status list must match value length "
                f"({len(self.value)}) or be single value"
            )
            raise JSONStatValidationError(error_message)

        # Check all dimensions are defined
        missing_dims = [dim_id for dim_id in self.id if dim_id not in self.dimension]
        if missing_dims:
            error_message = f"Missing dimension definitions: {', '.join(missing_dims)}"
            raise JSONStatValidationError(error_message)
        return self
