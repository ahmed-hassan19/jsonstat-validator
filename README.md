# JSON-stat Validator

[![PyPI version](https://img.shields.io/pypi/v/jsonstat-validator.svg)](https://pypi.org/project/jsonstat-validator/)
[![Python Version](https://img.shields.io/pypi/pyversions/jsonstat-validator.svg)](https://pypi.org/project/jsonstat-validator/)
[![License](https://img.shields.io/github/license/ahmed-hassan19/jsonstat-validator.svg)](https://github.com/ahmed-hassan19/jsonstat-validator/blob/main/LICENSE)

A Python validator for the JSON-stat 2.0 standard format, based on Pydantic.

JSON-stat is a simple lightweight format for data interchange. It is a JSON format for data dissemination that allows the representation of statistical data in a way that is both simple and convenient for data processing. With this validator, you can ensure your data conforms to the official [JSON-stat 2.0 specification](https://json-stat.org/full/).

## Disclaimer

This is a non-official implementation of the JSON-stat validator. The official validator can be found at [json-stat.org/format/validator/](https://json-stat.org/format/validator/).

Please note that this implementation is intentionally more strict than the official validator, as it applies all limitations and logical rules mentioned in the specification. For example:

```json
{
    "id": ["country", "year", "age", "concept", "sex"],
    "size": [1, 2]
}
```

This dataset would be considered valid by the official JSON-stat validator tool, but will fail validation in this package because it violates the rule in the `dataset.size` section of the specification stating that: `size has the same number of elements and in the same order as in id`.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Usage Examples](#usage-examples)
  - [Creating and Validating a Dimension](#creating-and-validating-a-dimension)
  - [Creating and Validating a Dataset](#creating-and-validating-a-dataset)
  - [Creating and Validating a Collection](#creating-and-validating-a-collection)
  - [Converting Between Python Models and JSON](#converting-between-python-models-and-json)
  - [Validating Existing JSON-stat Files](#validating-existing-json-stat-files)
- [Testing](#testing)
- [Development](#development)
  - [Local Development Setup](#local-development-setup)
  - [Creating a New Release](#creating-a-new-release)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Installation

```bash
pip install jsonstat-validator
```

## Quick Start

Validate a JSON-stat object with a single function call. See the `samples/quickstart.py` file for a complete example.

## Key Features

- Validates JSON-stat data against the [full 2.0 specification](https://json-stat.org/full)
- Provides models for all major JSON-stat classes: **Dataset**, **Dimension**, **Collection**
- Built on Pydantic for robust type validation and detailed error messages
- Provides tests against the [official JSON-stat samples](https://json-stat.org/samples/collection.json) and custom fine-grained tests

## Usage Examples

All examples can be found in the `samples/` directory.

### Creating and Validating a Dimension

A dimension represents a variable in your dataset, such as gender, time, or geography. See `samples/dimension_example.py` for the complete implementation.

### Creating and Validating a Dataset

Datasets are the main class in JSON-stat, representing statistical data with dimensions. Check out `samples/dataset_example.py` for a comprehensive example.

### Creating and Validating a Collection

Collections are containers for multiple datasets and dimensions. Refer to `samples/collection_example.py` for details.

### Converting Between Python Models and JSON

Convert your models to JSON or create models from existing JSON. The `samples/conversion_example.py` file demonstrates this functionality.

### Validating Existing JSON-stat Files

Validate JSON-stat files against the 2.0 specification. See `samples/validation_example.py` for implementation details.

## Testing

The validator has been thoroughly tested with all official JSON-stat samples from the [JSON-stat website](https://json-stat.org/samples/).

To run tests:

```bash
# Install development dependencies
pip install jsonstat-validator[dev]

# Run all tests
pytest

# Run specific tests
pytest tests/test_official_samples.py
```

## Development

### Local Development Setup

For local development:

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/jsonstat-validator.git
cd jsonstat-validator

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Creating a New Release

1. Create a new release on GitHub with a tag in the format `vX.Y.Z`

The GitHub Actions workflow will automatically:
- Run tests
- Build the package
- Update version numbers in both `__init__.py` and `pyproject.toml`
- Publish the package to PyPI
- Update the CHANGELOG.md with the release date and commit messages

## Contributing

We welcome contributions to the JSON-stat Validator! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For more details, please see our [CONTRIBUTING.md](.github/CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- [JSON-stat](https://json-stat.org/) - For creating and maintaining the JSON-stat standard
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For the data validation framework
