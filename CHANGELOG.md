# Changelog

## [Unreleased]

## v0.4.0 (2025-11-06)

### Changed

- Improved validation logic for the `Dataset` model.
- Improved validation logic for the `Dimension` model.
- Improved validation logic for the `Unit` model.
- Improved validation logic for the `Link` model.
- Modified affected tests in `test_dimension.py` and `test_unit.py` accordingly.

### Added

- Added `Extension` model.
- Added `link/LinkRelationType` model for link relation types according to [IANA link relation names](https://www.iana.org/assignments/link-relations/link-relations.xhtml).

### Fixed

- Changed type of `href` field from `str` to `AnyUrl` in the `Dataset` model.
- Fixed required `decimals` field in the `Unit` model.
- Set default value for `position` field in the `Unit` model to `end`.
- Fixed validation logic for the `link` field in the `Dataset`, `Dimension` and `Collection` models.
- Fixed child members not in `index`.


## v0.3.1 (2025-11-05)

### Added
- Expose the `Link` model for public import.


## v0.3.1 (2025-11-05)

### Changed

- Improved validation logic for the `Dataset` model.
- Improved validation logic for the `Dimension` model.
- Improved validation logic for the `Unit` model.

### Added

- Added `Extension` model.

### Fixed

- Changed type of `href` field from `str` to `AnyUrl` in the `Dataset` model.
- Fixed required `decimals` field in the `Unit` model.
- Set default value for `position` field in the `Unit` model to `end`.

## v0.3.0 (2025-09-30)

### Changed

- Migrated to `src` layout for better package isolation.
- Refactored `tests/` into a test file per model.
- Replaced **pip** with **uv** for project management and publishing to **pypi**.
- Replaced **Black** and **isort** with **Ruff** for linting and formatting.

### Added

- Pre-commit configuration with **Ruff** and **pre-commit** hooks.
- More tests to achieve near 100% test coverage.

### Fixed

- Raise an error for duplicate keys in the `index` field when it is a list.

## v0.2.2 (2025-07-20)

### Changed

- Expose the `JSONStatBaseModel` model for public import.

## v0.2.1 (2025-07-19)

### Changed

- Allow a dimension with empty dimension members (`category.index` and `category.label`).
- Expose the `Category` models for public import.

## v0.2.0 (2025-04-04)

### Added

- Added support for `note` and `source` fields in the `Collection` model.

### Changed

- Changed type of `category.note` from `List[str]` to `Dict[str, List[str]]` as stated in the [JSON-stat specification](https://json-stat.org/full/#note).

  > [note](https://json-stat.org/full/#note) allows to assign annotations to datasets (array), dimensions (array) and categories (object).
  >
- Modified `model_config.extra` from `ignore` to `forbid` to prevent passing undefined fields (extra fields are only allowed within the `extension` object).

### Refactored

- Separated validation logic from model definitions for better maintainability and separation of concerns.
- Improved error reporting with more human-readable error messages.

## v0.1.6 [pre-release] (2025-03-28)

- Fix: add `extension` field to the `Collection` class.

## v0.1.5 [pre-release] (2025-03-28)

- Fix: add alias for `class_` field in `Link` class.

## v0.1.4 [pre-release] (2025-03-17)

- Add a check to enforce same `label` and `index` keys in the `Category` class if label is a `dict` and index is a `list`.

## v0.1.3 [pre-release] (2025-03-17)

- Add a check to enforce same `label` and `index` keys in the `Category` class if both are present and of type `dict`.

## v0.1.2 [pre-release] (2025-03-16)

Pre-release of the JSON-stat validator package

- Support for validating the JSON-stat 2.0 format data
- Pydantic models for Dataset, Dimension, and Collection
- Tests against the [official JSON-stat samples](https://json-stat.org/samples/collection.json) and custom fine-grained tests (see `tests/` folder)
- Example code snippets (see `examples/` folder)
