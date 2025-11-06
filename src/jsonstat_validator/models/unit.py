"""Unit model for JSON-stat."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from jsonstat_validator.models.base import JSONStatBaseModel


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

    label: str = Field(default="")
    decimals: int = Field(
        description=(
            "It contains the number of unit decimals (integer). "
            "If unit is present, decimals is required."
        ),
    )
    symbol: str | None = Field(
        default=None,
        description=(
            "It contains a possible unit symbol to add to the value "
            "when it is displayed (like '€', '$' or '%')."
        ),
    )
    position: Literal["start", "end"] = Field(
        default="end",
        description=(
            "where the unit symbol should be written (before or after the value). "
            "Default is end."
        ),
    )
    base: str | None = Field(
        default=None,
        description=("It is the base unit (person, gram, euro, etc.)."),
    )
    type: str | None = Field(
        default=None,
        description=(
            "This property should probably help deriving new data from the data. "
            "It should probably help answering questions like: does it make sense "
            "to add two different cell values? Some possible values of this "
            "property could be count or ratio. Some might also consider as "
            "possible values things like currency, mass, length, time, etc."
        ),
    )
    multiplier: int | float | None = Field(
        default=None,
        description=(
            "It is the unit multiplier. It should help comparing data with the "
            "same base unit but different multiplier. If a decimal system is used, "
            "it can be expressed as powers of 10 (0=1, 1=10, -1=0.1, etc.)."
        ),
    )
    adjustment: str | None = Field(
        default=None,
        description=(
            "A code to express the time series adjustment (for example, "
            "seasonally adjusted or adjusted by working days) or indices "
            "adjustment (for example, chain-linked indices)."
        ),
    )
