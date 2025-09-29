"""Utility functions for JSON-stat validator."""

from datetime import datetime


class JSONStatValidationError(Exception):
    """Exception raised for JSON-stat validation errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def is_valid_iso_date(date_string: str) -> bool:
    """Check if a date string is in ISO 8601 format."""
    try:
        datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True
