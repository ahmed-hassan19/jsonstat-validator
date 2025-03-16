#!/usr/bin/env python
"""
Version bumping script for jsonstat-validator.

This script updates the version number in:
1. jsonstat_validator/__init__.py
2. pyproject.toml

Usage:
    python scripts/bump_version.py [major|minor|patch] [--dry-run]
"""

import argparse
import re
from pathlib import Path


def read_file(path):
    """Read a file and return its contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def bump_version(current_version, bump_type):
    """Bump the version number based on the bump type."""
    major, minor, patch = map(int, current_version.split("."))

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def update_init_file(new_version, dry_run=False):
    """Update the version in __init__.py file."""
    init_path = Path("jsonstat_validator/__init__.py")
    content = read_file(init_path)

    # Update version
    updated_content = re.sub(
        r'__version__ = "([^"]+)"', f'__version__ = "{new_version}"', content
    )

    if not dry_run:
        write_file(init_path, updated_content)
    return True


def update_pyproject_toml(new_version, dry_run=False):
    """Update the version in pyproject.toml file."""
    pyproject_path = Path("pyproject.toml")
    content = read_file(pyproject_path)

    # Update version
    updated_content = re.sub(
        r'version = "([^"]+)"', f'version = "{new_version}"', content
    )

    if not dry_run:
        write_file(pyproject_path, updated_content)
    return True


def update_setup_py(new_version, dry_run=False):
    """Update the version in setup.py file if it has a hardcoded version."""
    setup_path = Path("setup.py")
    if not setup_path.exists():
        return False

    content = read_file(setup_path)

    # Check if setup.py already uses dynamic versioning
    if re.search(r"version=version", content) or re.search(
        r"version_match = re.search", content
    ):
        print("setup.py already uses dynamic versioning, no update needed")
        return True

    # Update hardcoded version if present
    updated_content = re.sub(r'version="([^"]+)"', f'version="{new_version}"', content)

    if content != updated_content and not dry_run:
        write_file(setup_path, updated_content)
        print("Updated version in setup.py")
        return True

    return False


def get_current_version():
    """Get the current version from __init__.py."""
    init_path = Path("jsonstat_validator/__init__.py")
    content = read_file(init_path)

    match = re.search(r'__version__ = "([^"]+)"', content)
    if match:
        return match.group(1)

    raise ValueError("Could not determine current version from __init__.py")


def main():
    """Run the script."""
    parser = argparse.ArgumentParser(
        description="Bump the version number for jsonstat-validator"
    )
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump to perform",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    args = parser.parse_args()

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        new_version = bump_version(current_version, args.bump_type)
        print(f"New version: {new_version}")

        if args.dry_run:
            print("Dry run mode: No changes will be made")

        update_init_file(new_version, args.dry_run)
        update_pyproject_toml(new_version, args.dry_run)
        update_setup_py(new_version, args.dry_run)

        if args.dry_run:
            print(f"Would bump version to {new_version}")
            print("Would need to update CHANGELOG.md")
            tag_cmd = f"git tag v{new_version}"
            print(f"Would need to commit changes and create a new tag: {tag_cmd}")
        else:
            print(f"Successfully bumped version to {new_version}")
            print("Don't forget to update CHANGELOG.md!")
            tag_cmd = f"git tag v{new_version}"
            print(f"Commit the changes and create a new tag: {tag_cmd}")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
