#!/usr/bin/env python
"""
Example script for validating JSON-stat files.

This example demonstrates how to use the jsonstat-validator package to validate
JSON-stat data files.
"""

import argparse
import json
import sys

from jsonstat_validator import validate_jsonstat


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate a JSON-stat file against the 2.0 specification"
    )
    parser.add_argument("file", help="Path to the JSON-stat file to validate")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed error information"
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    # Load the JSON file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{args.file}': {e}")
        sys.exit(1)

    # Validate the JSON-stat data
    try:
        validate_jsonstat(data)
        print(f"✅ Validation successful: '{args.file}' is a valid JSON-stat 2.0 file.")
        return 0
    except ValueError as e:
        print(f"❌ Validation failed: '{args.file}' is not a valid JSON-stat 2.0 file.")
        if args.verbose:
            print(f"Error details: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
