"""Link model for JSON-stat."""

from __future__ import annotations

from typing import Literal

from pydantic import AnyUrl, Field

from jsonstat_validator.models.base import JSONStatBaseModel


class Link(JSONStatBaseModel):
    """Model for a link.

    It is used to provide a list of links related to a dataset or a dimension,
    sorted by relation.
    """

    type: str | None = Field(
        default=None,
        description=(
            "It describes the media type of the accompanying href. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )
    href: AnyUrl | None = Field(default=None, description="It specifies a URL.")
    class_: Literal["dataset", "dimension", "collection"] | None = Field(
        default=None,
        alias="class",
        description=(
            "It describes the class of the resource referenced "
            "in the link. Not required when the resource referenced "
            "in the link is a JSON-stat resource."
        ),
    )
    label: str | None = Field(
        default=None,
        description=(
            "It provides a human-readable label for the link. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )
