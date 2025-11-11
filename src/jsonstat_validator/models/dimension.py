"""Dimension model for JSON-stat."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AnyUrl, Field, field_validator, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.category import Category
from jsonstat_validator.models.link import Link, LinkRelationType
from jsonstat_validator.utils import JSONStatValidationError, is_valid_iso_date


class Dimension(JSONStatBaseModel):
    """JSON-stat dimension.

    This is a full implementation of the dimension class
    according to the JSON-stat 2.0 specification: https://json-stat.org/full/#dimension.
    """

    version: str = Field(
        default="2.0",
        description=(
            "It declares the JSON-stat version of the response. The goal "
            "of this property is to help clients parsing that particular response."
        ),
    )
    class_: Annotated[
        Literal["dimension"], Field(alias="class", serialization_alias="class")
    ] = Field(
        default="dimension",
        description=(
            "JSON-stat supports several classes of responses. "
            "Possible values of class are: dataset, dimension and collection."
        ),
    )
    label: str | None = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    category: Category | None = Field(
        description=(
            "It is used to describe the possible values of a dimension. "
            "It is language-dependent."
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
    link: dict[str, list[Link | JSONStatSchema]] | None = Field(
        default=None,
        description=(
            "It is used to provide a list of links related to a dataset or a dimension, "
            "sorted by relation (see https://json-stat.org/full/#relationid)."
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
    updated: str | None = Field(
        default=None,
        description=(
            "It contains the update time of the dataset. It is a string representing "
            "a date in an ISO 8601 format recognized by the Javascript Date.parse "
            "method (see ECMA-262 Date Time String Format: "
            "https://262.ecma-international.org/6.0/#sec-date-time-string-format)."
        ),
    )
    source: str | None = Field(
        default=None,
        description=(
            "It contains a language-dependent short text describing the source "
            "of the dataset."
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

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: str | None) -> str | None:
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            raise JSONStatValidationError(
                f"Updated date: '{v}' is an invalid ISO 8601 format."
            )
        return v

    @model_validator(mode="after")
    def validate_link_relations(self) -> Dimension:
        if self.link and "item" in self.link:
            raise JSONStatValidationError(
                "Only collections may use 'item' relation in 'link'."
            )
        # Validate that category or href is provided
        if not self.category and not self.href:
            raise JSONStatValidationError(
                "A category is required if a reference (href) is not provided. "
                "For an example, see: https://json-stat.org/full/#href"
            )
        return self


class DatasetDimension(JSONStatBaseModel):
    """Dataset dimension.

    A dimension model for when the dimension is a child of a Dataset
    as it has different validation rules than a root Dimension.
    """

    version: str | None = Field(
        default=None,
        description=(
            "It declares the JSON-stat version of the response. The goal "
            "of this property is to help clients parsing that particular response."
        ),
    )
    class_: Annotated[str | None, Field(alias="class", exclude=True)] = Field(
        default="dataset_dimension",
        description=(
            "JSON-stat supports several classes of responses. "
            "Possible values of class are: dataset, dimension and collection. "
            "This is an addition to the standard JSON-stat classes to allow for "
            "different validation rules for dataset dimensions."
        ),
    )
    label: str | None = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    category: Category | None = Field(
        default=None,
        description=(
            "It is used to describe the possible values of a dimension. "
            "It is language-dependent."
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
    link: dict[str, list[Link | JSONStatSchema]] | None = Field(
        default=None,
        description=(
            "It is used to provide a list of links related to a dataset or a dimension, "
            "sorted by relation (see https://json-stat.org/full/#relationid)."
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
    updated: str | None = Field(
        default=None,
        description=(
            "It contains the update time of the dataset. It is a string representing "
            "a date in an ISO 8601 format recognized by the Javascript Date.parse "
            "method (see ECMA-262 Date Time String Format: "
            "https://262.ecma-international.org/6.0/#sec-date-time-string-format)."
        ),
    )
    source: str | None = Field(
        default=None,
        description=(
            "It contains a language-dependent short text describing the source "
            "of the dataset."
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

    @model_validator(mode="after")
    def validate_dataset_dimension(self) -> DatasetDimension:
        """Dataset dimension-wide validation checks."""
        if not self.category and not self.href:
            raise JSONStatValidationError(
                "A category is required if a reference (href) is not provided. "
                "For an example, see: https://json-stat.org/full/#href"
            )

        # link: only collections may use 'item' relation
        if self.link and "item" in self.link:
            raise JSONStatValidationError(
                "Only collections may use 'item' relation in 'link'."
            )
        return self
