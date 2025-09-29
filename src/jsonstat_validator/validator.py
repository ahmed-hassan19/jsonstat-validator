"""Validator for JSON-stat."""

from pydantic import ValidationError

from jsonstat_validator.models.base import JSONStatSchema
from jsonstat_validator.utils import JSONStatValidationError


def format_error_location(loc: tuple) -> str:
    """Format error location to be more human-readable.

    Args:
        loc: Location tuple from ValidationError

    Returns:
        str: Formatted location string
    """
    parts = []
    for item in loc:
        if isinstance(item, int):
            parts.append(f"[{item}]")
        elif parts:
            parts.append(f".{item}")
        else:
            parts.append(item)
    return "".join(parts)


def format_validation_errors(e: ValidationError) -> str:
    """Format ValidationError to be more human-readable.

    Args:
        e: ValidationError instance

    Returns:
        str: Formatted error message
    """
    errors = []
    for error in e.errors():
        # Create a simplified error object without input and url fields
        loc = format_error_location(error["loc"])
        msg = error["msg"]
        type_str = error["type"]

        errors.append(f"Error at '{loc}': {msg} (type={type_str})")

    return "\n".join(errors)


def validate_jsonstat(data: dict) -> bool:
    """Validate a JSON-stat 2.0 object against the specification.

    Args:
        data: A dictionary containing JSON-stat data

    Returns:
        bool: True if valid, raises ValueError otherwise

    Raises:
        ValueError: If the data does not conform to the JSON-stat specification
                   with a user-friendly error message
    """
    try:
        JSONStatSchema.model_validate(data)
    except ValidationError as e:
        error_message = f"JSON-stat validation failed:\n{format_validation_errors(e)}"
        raise JSONStatValidationError(error_message) from e
    else:
        return True
