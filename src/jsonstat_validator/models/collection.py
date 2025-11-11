"""Collection model for JSON-stat."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AnyUrl, Field, field_validator, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel, JSONStatSchema
from jsonstat_validator.models.link import Link, LinkRelationType
from jsonstat_validator.utils import JSONStatValidationError, is_valid_iso_date


class Collection(JSONStatBaseModel):
    """JSON-stat collection."""

    version: str = Field(
        default="2.0",
        description=(
            "It declares the JSON-stat version of the response. The goal "
            "of this property is to help clients parsing that particular response."
        ),
    )

    class_: Annotated[
        Literal["collection"], Field(alias="class", serialization_alias="class")
    ] = Field(
        default="collection",
        description="It declares the class of the response.",
    )
    label: str | None = Field(
        default=None,
        description="It provides a human-readable label for the collection.",
    )
    href: AnyUrl | None = Field(
        default=None,
        description="It specifies a URL.",
    )
    updated: str | None = Field(
        default=None,
        description="It contains the update time of the collection.",
    )
    link: dict[str, list[Link | JSONStatSchema]] | None = Field(
        default=None,
        description=(
            "The items of the collection can be of any class "
            "(datasets, dimensions, collections)."
        ),
    )
    source: str | None = Field(
        default=None,
        description="It contains a language-dependent short text describing the source "
        "of the collection.",
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
        description="Extension allows JSON-stat to be extended for particular needs. "
        "Providers are free to define where they include this property and "
        "what children are allowed in each case.",
    )

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: str | None) -> str | None:
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            error_message = f"Updated date: '{v}' is an invalid ISO 8601 format."
            raise JSONStatValidationError(error_message)
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
                f"Invalid link relation types: {invalid_keys}. Must be one of: "
            )
        return data

    @model_validator(mode="after")
    def validate_collection(self) -> Collection:
        if not self.link:
            return self
        if "item" not in self.link:
            raise JSONStatValidationError(
                "Collection links must use 'item' relation type."
            )
        # Values must be lists
        for rel, entries in self.link.items():
            if not isinstance(entries, list):
                raise JSONStatValidationError(f"Relation '{rel}' must be a list.")
        return self
