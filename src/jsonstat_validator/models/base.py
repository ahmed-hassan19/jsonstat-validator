"""Base model for JSON-stat models."""

from __future__ import annotations

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, RootModel, field_serializer


class JSONStatBaseModel(BaseModel):
    """Base model for all JSON-stat models with common configuration."""

    def model_dump(
        self, *, exclude_none: bool = True, by_alias: bool | None = True, **kwargs
    ) -> dict:
        """Override model_dump to set exclude_none=True by default."""
        return super().model_dump(
            exclude_none=exclude_none, by_alias=by_alias, **kwargs
        )

    @field_serializer("href", check_fields=False, return_type=str)
    def serialize_any_url(self, href: AnyUrl | None) -> str | None:
        """Convert AnyUrl to string, if it exists."""
        return str(href) if href else None

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        serialize_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
    )


class JSONStatSchema(RootModel):
    """JSON-stat response."""

    root: Dataset | Dimension | Collection = Field(  # noqa: F821
        ...,
        discriminator="class_",
    )

    def model_dump(
        self, *, exclude_none: bool = True, by_alias: bool | None = True, **kwargs
    ) -> dict:
        """Override model_dump to set exclude_none=True by default."""
        return super().model_dump(
            exclude_none=exclude_none, by_alias=by_alias, **kwargs
        )

    @field_serializer("href", check_fields=False, return_type=str)
    def serialize_any_url(self, href: AnyUrl | None) -> str | None:
        """Convert AnyUrl to string, if it exists."""
        return str(href) if href else None
