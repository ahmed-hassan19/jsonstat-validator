"""
JSON-stat validator.

Validates JSON-stat data against the specification:
https://json-stat.org/full/
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    RootModel,
    ValidationError,
    field_serializer,
    field_validator,
    model_validator,
)

# pylint: disable=[useless-parent-delegation]


def is_valid_iso_date(date_string: str) -> bool:
    """Check if a date string is in ISO 8601 format."""
    try:
        datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


class JSONStatBaseModel(BaseModel):
    """Base model for all JSON-stat models with common configuration."""

    def model_dump(self, *, exclude_none: bool = True, by_alias: bool = True, **kwargs):
        """Override model_dump to set exclude_none=True by default."""
        return super().model_dump(exclude_none=exclude_none, by_alias=by_alias, **kwargs)

    @field_serializer("href", check_fields=False, return_type=str)
    def serialize_any_url(self, href: Optional[AnyUrl]) -> Optional[str]:
        """Convert AnyUrl to string, if it exists."""
        return str(href) if href else None


class Unit(JSONStatBaseModel):
    """Unit of measurement of a dimension.

    It can be used to assign unit of measure metadata to the categories
    of a dimension with a metric role.
    Four properties of this object are currently closed:
        decimals, label, symbol and position.
    Based on current standards and practices, other properties of this object could be:
        base, type, multiplier, adjustment.

        These properties are currently open. Data providers are free to use them
        on their own terms, although it is safer to do it under extension.
    """

    label: Optional[str] = Field(default=None)
    decimals: Optional[int] = Field(
        default=None,
        description=(
            "It contains the number of unit decimals (integer). "
            "If unit is present, decimals is required."
        ),
    )
    symbol: Optional[str] = Field(
        default=None,
        description=(
            "It contains a possible unit symbol to add to the value "
            "when it is displayed (like '€', '$' or '%')."
        ),
    )
    position: Optional[Literal["start", "end"]] = Field(
        default=None,
        description=(
            "where the unit symbol should be written (before or after the value). "
            "Default is end."
        ),
    )
    base: Optional[str] = Field(
        default=None,
        description=("It is the base unit (person, gram, euro, etc.)."),
    )
    type: Optional[str] = Field(
        default=None,
        description=(
            "This property should probably help deriving new data from the data. "
            "It should probably help answering questions like: does it make sense "
            "to add two different cell values? Some possible values of this "
            "property could be count or ratio. Some might also consider as "
            "possible values things like currency, mass, length, time, etc."
        ),
    )
    multiplier: Optional[Union[int, float]] = Field(
        default=None,
        description=(
            "It is the unit multiplier. It should help comparing data with the "
            "same base unit but different multiplier. If a decimal system is used, "
            "it can be expressed as powers of 10 (0=1, 1=10, -1=0.1, etc.)."
        ),
    )
    adjustment: Optional[str] = Field(
        default=None,
        description=(
            "A code to express the time series adjustment (for example, "
            "seasonally adjusted or adjusted by working days) or indices "
            "adjustment (for example, chain-linked indices)."
        ),
    )


class Category(JSONStatBaseModel):
    """Category of a dimension.

    It is used to describe the possible values of a dimension.
    """

    index: Optional[Union[List[str], Dict[str, int]]] = Field(
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
    label: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    child: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description=(
            "It is used to describe the hierarchical relationship between different "
            "categories. It takes the form of an object where the key is the ID of "
            "the parent category and the value is an array of the IDs of the child "
            "categories. It is also a way of exposing a certain category as a total."
        ),
    )
    coordinates: Optional[Dict[str, List[float]]] = Field(
        default=None,
        description=(
            "It can be used to assign longitude/latitude geographic coordinates "
            "to the categories of a dimension with a geo role. It takes the form "
            "of an object where keys are category IDs and values are an array of "
            "two numbers (longitude, latitude)."
        ),
    )
    unit: Optional[Dict[str, Unit]] = Field(
        default=None,
        description=(
            "It can be used to assign unit of measure metadata to the categories "
            "of a dimension with a metric role."
        ),
    )

    @model_validator(mode="after")
    def validate_category(self):
        """Category-wide validation checks."""
        # Ensure at least one of index or label fields is provided
        if not self.index and not self.label:
            raise ValueError("At least one of `index` or `label` is required.")

        # Ensure coordinates are a dictionary where keys are category IDs
        # and values are an array of two numbers (longitude, latitude).
        if self.coordinates:
            for key in self.coordinates:
                value = self.coordinates[key]
                if (self.index and key not in self.index) or (
                    self.label and key not in self.label
                ):
                    raise ValueError(
                        f"Trying to set coordinates for category ID: {key} "
                        "but it is not defined neither in `index` nor in `label`."
                    )
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError(
                        f"Coordinates for category {key} must be a list of two numbers."
                    )

        # Ensure child references an existing parent
        if self.child:
            for parent in self.child:
                if (self.index and parent not in self.index) or (
                    self.label and parent not in self.label
                ):
                    raise ValueError(
                        f"Invalid parent: {parent} in the `child` field. "
                        "It is not defined neither in `index` nor in `label`."
                    )

        # Ensure unit references an existing category
        if self.unit:
            for key in self.unit:
                value = self.unit[key]
                if (self.index and key not in self.index) or (
                    self.label and key not in self.label
                ):
                    raise ValueError(
                        f"Invalid unit: {key} in the `unit` field. "
                        "It is not defined neither in `index` nor in `label`."
                    )
        return self


class Link(JSONStatBaseModel):
    """Model for a link.

    It is used to provide a list of links related to a dataset or a dimension,
    sorted by relation.
    """

    type: Optional[str] = Field(
        default=None,
        description=(
            "It describes the media type of the accompanying href. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )
    href: Optional[AnyUrl] = Field(default=None, description="It specifies a URL.")
    class_: Optional[Literal["dataset", "dimension", "collection"]] = Field(
        default=None,
        description=(
            "It describes the class of the resource referenced "
            "in the link. Not required when the resource referenced "
            "in the link is a JSON-stat resource."
        ),
    )
    label: Optional[str] = Field(
        default=None,
        description=(
            "It provides a human-readable label for the link. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )


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
    class_: Literal["dimension"] = Field(
        default="dimension",
        alias="class",
        description=(
            "JSON-stat supports several classes of responses. "
            "Possible values of class are: dataset, dimension and collection."
        ),
    )
    label: Optional[str] = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    category: Category = Field(
        description=(
            "It is used to describe the possible values of a dimension. "
            "It is language-dependent."
        ),
    )
    href: Optional[AnyUrl] = Field(
        default=None,
        description=(
            "It specifies a URL. Providers can use this property to avoid "
            "sending information that is shared between different requests "
            "(for example, dimensions)."
        ),
    )
    link: Optional[Dict[str, List[Union[Link, JSONStatSchema]]]] = Field(
        default=None,
        description=(
            "It is used to provide a list of links related to a dataset or a dimension, "
            "sorted by relation (see relation ID)."
        ),
    )
    note: Optional[List[str]] = Field(
        default=None,
        description=(
            "Note allows to assign annotations to datasets (array), dimensions (array) "
            "and categories (object)."
        ),
    )
    updated: Optional[str] = Field(
        default=None,
        description=(
            "It contains the update time of the dataset. It is a string representing "
            "a date in an ISO 8601 format recognized by the Javascript Date.parse "
            "method (see ECMA-262 Date Time String Format: "
            "https://262.ecma-international.org/6.0/#sec-date-time-string-format)."
        ),
    )
    source: Optional[str] = Field(
        default=None,
        description=(
            "It contains a language-dependent short text describing the source "
            "of the dataset."
        ),
    )
    extension: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Extension allows JSON-stat to be extended for particular needs. "
            "Providers are free to define where they include this property and "
            "what children are allowed in each case."
        ),
    )

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: Optional[str]):
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            raise ValueError(f"Updated date: '{v}' is an invalid ISO 8601 format.")
        return v


class DatasetRole(JSONStatBaseModel):
    """Role of a dataset."""

    time: Optional[List[str]] = Field(
        default=None,
        description=(
            "It can be used to assign a time role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )
    geo: Optional[List[str]] = Field(
        default=None,
        description=(
            "It can be used to assign a spatial role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )
    metric: Optional[List[str]] = Field(
        default=None,
        description=(
            "It can be used to assign a metric role to one or more dimensions. "
            "It takes the form of an array of dimension IDs in which order does "
            "not have a special meaning."
        ),
    )


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
    href: Optional[AnyUrl] = Field(
        default=None,
        description=(
            "It specifies a URL. Providers can use this property to avoid "
            "sending information that is shared between different requests "
            "(for example, dimensions)."
        ),
    )
    label: Optional[str] = Field(
        default=None,
        description=(
            "It is used to assign a very short (one line) descriptive text to IDs "
            "at different levels of the response tree. It is language-dependent."
        ),
    )
    source: Optional[str] = Field(
        default=None,
        description=(
            "It contains a language-dependent short text describing the source "
            "of the dataset."
        ),
    )
    updated: Optional[str] = Field(
        default=None,
        description=(
            "It contains the update time of the dataset. It is a string representing "
            "a date in an ISO 8601 format recognized by the Javascript Date.parse "
            "method (see ECMA-262 Date Time String Format: "
            "https://262.ecma-international.org/6.0/#sec-date-time-string-format)."
        ),
    )
    id: List[str] = Field(description="It contains an ordered list of dimension IDs.")
    size: List[int] = Field(
        description=(
            "It contains the number (integer) of categories (possible values) "
            "of each dimension in the dataset. It has the same number of elements "
            "and in the same order as in id."
        ),
    )
    role: Optional[DatasetRole] = Field(
        default=None,
        description=(
            "It can be used to assign special roles to dimensions. "
            "At this moment, possible roles are: time, geo and metric. "
            "A role can be shared by several dimensions."
        ),
    )
    value: Union[
        List[Union[float, int, str, None]], Dict[str, Union[float, int, str, None]]
    ] = Field(
        description=(
            "It contains the data sorted according to the dataset dimensions. "
            "It usually takes the form of an array where missing values are "
            "expressed as nulls."
        ),
    )
    status: Optional[Union[str, List[str], Dict[str, str]]] = Field(
        default=None,
        description=(
            "It contains metadata at the observation level. When it takes an "
            "array form of the same size of value, it assigns a status to each "
            "data by position. When it takes a dictionary form, it assigns a "
            "status to each data by key."
        ),
    )

    dimension: Dict[str, Dimension] = Field(
        description=(
            "The dimension property contains information about the dimensions of "
            "the dataset. dimension must have properties (see dimension ID) with "
            "the same names of each element in the id array."
        ),
    )
    note: Optional[List[str]] = Field(
        default=None,
        description=(
            "Note allows to assign annotations to datasets (array), dimensions (array) "
            "and categories (object)."
        ),
    )
    extension: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Extension allows JSON-stat to be extended for particular needs. "
            "Providers are free to define where they include this property and "
            "what children are allowed in each case."
        ),
    )
    link: Optional[Dict[str, List[Union[Link, JSONStatSchema]]]] = Field(
        default=None,
        description=(
            "It is used to provide a list of links related to a dataset or a dimension, "
            "sorted by relation (see relation ID)."
        ),
    )

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: Optional[str]):
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            raise ValueError(f"Updated date: '{v}' is an invalid ISO 8601 format.")
        return v

    @field_validator("role", mode="after")
    @classmethod
    def validate_role(cls, v: Optional[DatasetRole]):
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
                raise ValueError(
                    f"Dimension(s): {', '.join(duplicates)} referenced in multiple "
                    "roles. Each dimension can only be referenced in one role."
                )
        return v

    @model_validator(mode="after")
    def validate_dataset(self):
        """Dataset-wide validation checks."""
        # Validate size matches id length

        if len(self.size) != len(self.id):
            raise ValueError(
                f"Size array length ({len(self.size)}) "
                f"must match ID array length ({len(self.id)})"
            )

        # Validate status format
        if isinstance(self.status, list):
            if len(self.status) not in (len(self.value), 1):
                raise ValueError(
                    "Status list must match value length "
                    f"({len(self.value)}) or be single value"
                )

        # Check all dimensions are defined
        missing_dims = [dim_id for dim_id in self.id if dim_id not in self.dimension]
        if missing_dims:
            raise ValueError(f"Missing dimension definitions: {', '.join(missing_dims)}")
        return self


class Collection(JSONStatBaseModel):
    """JSON-stat collection."""

    version: str = Field(
        default="2.0",
        description=(
            "It declares the JSON-stat version of the response. The goal "
            "of this property is to help clients parsing that particular response."
        ),
    )

    class_: Literal["collection"] = Field(
        default="collection",
        alias="class",
        description="It declares the class of the response.",
    )
    label: Optional[str] = Field(
        default=None,
        description="It provides a human-readable label for the collection.",
    )
    href: Optional[AnyUrl] = Field(
        default=None,
        description="It specifies a URL.",
    )
    updated: Optional[str] = Field(
        default=None,
        description="It contains the update time of the collection.",
    )
    link: Optional[Dict[str, List[Union[Link, JSONStatSchema]]]] = Field(
        default=None,
        description=(
            "The items of the collection can be of any class "
            "(datasets, dimensions, collections)."
        ),
    )

    @field_validator("updated", mode="after")
    @classmethod
    def validate_updated_date(cls, v: Optional[str]):
        """Validates the updated date is in ISO 8601 format."""
        if v and not is_valid_iso_date(v):
            raise ValueError(f"Updated date: '{v}' is an invalid ISO 8601 format.")
        return v

    @model_validator(mode="after")
    def validate_collection(self):
        """Collection-wide validation checks."""
        # Ensure collection links use correct relation type.
        if self.link and "item" not in self.link:
            raise ValueError("Collection links must use 'item' relation type")
        return self


class JSONStatSchema(RootModel):
    """JSON-stat response."""

    root: Union[Dataset, Dimension, Collection] = Field(
        ...,
        discriminator="class_",
    )

    def model_dump(self, *, exclude_none: bool = True, by_alias: bool = True, **kwargs):
        """Override model_dump to set exclude_none=True by default."""
        return super().model_dump(exclude_none=exclude_none, by_alias=by_alias, **kwargs)

    @field_serializer("href", check_fields=False, return_type=str)
    def serialize_any_url(self, href: Optional[AnyUrl]) -> Optional[str]:
        """Convert AnyUrl to string, if it exists."""
        return str(href) if href else None


def validate_jsonstat(data: Dict[str, Any]) -> bool:
    """
    Validate a JSON-stat 2.0 object against the specification.

    Args:
        data: A dictionary containing JSON-stat data

    Returns:
        bool: True if valid, raises ValueError otherwise

    Raises:
        ValueError: If the data does not conform to the JSON-stat specification
    """
    try:
        JSONStatSchema(**data)
        return True
    except ValidationError as e:
        raise ValueError(e) from e
