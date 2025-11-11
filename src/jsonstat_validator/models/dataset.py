"""Dataset model for JSON-stat."""

from __future__ import annotations

from collections import Counter
from typing import Annotated, Literal

from pydantic import AnyUrl, Field, field_validator, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.dimension import DatasetDimension
from jsonstat_validator.models.link import Link, LinkRelationType
from jsonstat_validator.utils import JSONStatValidationError, is_valid_iso_date

ValueType = list[float | int | str | None] | dict[str, float | int | str | None]
StatusType = str | list[str] | dict[str, str] | None


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
        """Dataset role-wide validation checks.

        - At least one role must be provided.
        - Each dimension can only be referenced in one role.
        """
        if not self.time and not self.geo and not self.metric:
            raise JSONStatValidationError("At least one role must be provided.")
        if (
            self.time
            and self.geo
            and self.metric
            and len(set(self.time + self.geo + self.metric))
            != len(self.time + self.geo + self.metric)
        ):
            raise JSONStatValidationError(
                "Each dimension can only be referenced in one role."
            )
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
    class_: Annotated[
        Literal["dataset"], Field(alias="class", serialization_alias="class")
    ] = Field(
        default="dataset",
        description=(
            "JSON-stat supports several classes of responses. "
            "Possible values of class are: dataset, dimension and collection."
        ),
    )
    href: AnyUrl | None = Field(
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
    value: ValueType = Field(
        description=(
            "It contains the data sorted according to the dataset dimensions. "
            "It usually takes the form of an array where missing values are "
            "expressed as nulls."
        ),
    )
    status: StatusType = Field(
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
            raise JSONStatValidationError(
                f"Updated date: '{v}' is an invalid ISO 8601 format."
            )
        return v

    @field_validator("link", mode="before")
    @classmethod
    def validate_link_relations(cls, data: dict | str | None) -> dict | str | None:
        """Validate that additional properties match allowed link relation types."""
        if not isinstance(data, dict):
            return data

        allowed_types = {e.value for e in LinkRelationType}
        invalid_keys = [key for key in data if key not in allowed_types]
        if invalid_keys:
            raise JSONStatValidationError(
                f"Invalid link relation types: {invalid_keys}. Must be one of: {allowed_types}"
            )
        return data

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
                raise JSONStatValidationError(
                    f"Dimension(s): {', '.join(duplicates)} referenced in multiple roles. Each dimension can only be referenced in one role."
                )
        return v

    @model_validator(mode="after")
    def validate_dataset(self) -> Dataset:
        """Dataset-wide validation checks."""
        # siez, id: length must match
        if len(self.size) != len(self.id):
            raise JSONStatValidationError(
                f"Size array length ({len(self.size)}) must match ID array length ({len(self.id)})"
            )

        # size: non-negative
        if any((s is None) or (s < 0) for s in self.size):
            raise JSONStatValidationError(
                "All `size` values must be non-negative integers."
            )
        # id: unique
        if len(set(self.id)) != len(self.id):
            raise JSONStatValidationError("Dimension IDs in `id` must be unique.")

        # dimension: no missing, no extras
        missing_dims = [dim_id for dim_id in self.id if dim_id not in self.dimension]
        if missing_dims:
            raise JSONStatValidationError(
                f"Missing dimension definitions: {', '.join(missing_dims)}"
            )

        extra_dims = [dim_id for dim_id in self.dimension if dim_id not in self.id]
        if extra_dims:
            raise JSONStatValidationError(
                f"Unexpected dimensions not listed in `id`: {', '.join(extra_dims)}"
            )

        # role membership (if role provided)
        if self.role:
            role_dims = []
            for group in (
                (self.role.time or []),
                (self.role.geo or []),
                (self.role.metric or []),
            ):
                role_dims.extend(group)
            unknown_role_dims = [d for d in role_dims if d not in self.id]
            if unknown_role_dims:
                raise JSONStatValidationError(
                    f"Role references unknown dimensions: {', '.join(unknown_role_dims)}"
                )

        # status: when array, length must match value length or be single value
        if isinstance(self.status, list) and len(self.status) not in (
            len(self.value),
            1,
        ):
            raise JSONStatValidationError(
                f"Status list must match value length ({len(self.value)}) or be single value"
            )

        # align size[i] with inline category counts when available
        for i, dim_id in enumerate(self.id):
            dim = self.dimension[dim_id]
            if dim.category:
                idx = dim.category.index
                if isinstance(idx, list) or isinstance(idx, dict):  # noqa: SIM101
                    expected_size = len(idx)
                elif dim.category.label:
                    expected_size = 1  # constant dimension
                else:
                    expected_size = None
                if expected_size is not None and self.size[i] != expected_size:
                    raise JSONStatValidationError(
                        f"`size[{i}]` for dimension '{dim_id}' must equal number of categories ({expected_size})"
                    )

        # link: only collections may use 'item' relation
        if self.link and "item" in self.link:
            raise JSONStatValidationError(
                "Only collections may use 'item' relation in 'link'."
            )
        return self
