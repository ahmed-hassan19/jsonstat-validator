# Changelog

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