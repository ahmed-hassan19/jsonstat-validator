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

Additionally, we enforce the `role` field as required when `class=dataset`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Example Usage](#example-usage)
  - [Working with Models](#working-with-models)
- [Key Features](#key-features)
- [Testing](#testing)
- [Development](#development)
- [Contributing](#contributing)
- [Publishing](#publishing-for-maintainers)
- [License](#license)
- [Credits](#credits)

## Installation

**Using UV (recommended):**

```bash
uv add jsonstat-validator
```

**Using pip:**

```bash
pip install jsonstat-validator
```

## Usage

### Basic Usage

The simplest way to use the validator is with the `validate_jsonstat()` function:

```python
from jsonstat_validator import validate_jsonstat, JSONStatValidationError

try:
    validate_jsonstat(your_data)
    print("Data is valid!")
except JSONStatValidationError as e:
    print(f"Validation error: {e}")
```

### Example Usage

The validator provides detailed error messages:

```python
from jsonstat_validator import validate_jsonstat, JSONStatValidationError

invalid_data = {
    "version": "2.0",
    "class": "dataset",
    "id": ["time", "geo"],
    "size": [2],  # ❌ Size doesn't match id length!
    "value": [1, 2],
    "dimension": {}
}

try:
    validate_jsonstat(invalid_data)
except JSONStatValidationError as e:
    print(e)
    # Output: Size array length (1) must match ID array length (2)
```

### Working with Models

You can also work directly with the Pydantic models for more control:

```python
from jsonstat_validator import Dataset, Collection, Dimension

# Create a Dataset instance
dataset = Dataset(
    version="2.0",
    id=["time", "geo"],
    size=[2, 3],
    value=[1, 2, 3, 4, 5, 6],
    dimension={
        "time": {"category": {"index": ["2020", "2021"]}},
        "geo": {"category": {"index": {"US": 0, "EU": 1, "AS": 2}}},
    },
    role={"time": ["time"], "geo": ["geo"]}
)

# Access properties
print(dataset.id)  # ['time', 'geo']
print(dataset.size)  # [2, 3]

# Serialize back to dict
data_dict = dataset.model_dump()
```

## Key Features

- Validates JSON-stat data against the [full 2.0 specification](https://json-stat.org/full)
- Provides models for all major JSON-stat classes: **Dataset**, **Dimension**, **Collection**
- Built on Pydantic for robust type validation and detailed error messages
- Provides comprehensive test coverage with 109 tests organized into modular test files for each JSON-stat component

## Testing

The validator includes a comprehensive test suite with 109 tests organized into modular test files:

### Test Structure

- **Model-specific tests**: Each JSON-stat model has dedicated test files
  - `test_dataset.py` - Dataset validation tests
  - `test_collection.py` - Collection validation tests
  - `test_dimension.py` - Dimension validation tests
  - `test_category.py` - Category validation tests
  - `test_link.py` - Link validation tests
  - `test_unit.py` - Unit validation tests
- **Integration tests**: Cross-model validation scenarios in `test_custom.py`
- **Official samples**: Tests against all [official JSON-stat samples](https://json-stat.org/samples/) in `test_official_samples.py`
- **General validation**: Type and class validation tests in `test_validation.py`

### Running Tests

Using UV (recommended):

```bash
# Install with development dependencies
uv sync --dev

# Run all tests
uv run pytest -v

# Run tests for a specific model
uv run pytest tests/test_dataset.py

# Run official sample tests
uv run pytest tests/test_official_samples.py

# Run with coverage report
uv run pytest --cov=jsonstat_validator
```

Using pip:

```bash
# Install development dependencies
pip install jsonstat-validator[dev]

# Run all tests
pytest

# Run tests for a specific model
pytest tests/test_dataset.py

# Run official sample tests
pytest tests/test_official_samples.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=jsonstat_validator
```

## Development

To contribute to the project, set up your local development environment:

**Using UV (recommended):**

```bash
# Clone the repository
git clone https://github.com/ahmed-hassan19/jsonstat-validator.git
cd jsonstat-validator

# Install dependencies and create virtual environment
uv sync --dev

# Run tests
uv run pytest

# Run linter
uv run ruff check src/ tests/
```

**Using pip:**

```bash
# Clone the repository
git clone https://github.com/ahmed-hassan19/jsonstat-validator.git
cd jsonstat-validator

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

We welcome contributions to the JSON-stat Validator! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and ensure tests pass
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

For more details, please see our [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Publishing (for maintainers)

This project uses automated publishing to PyPI via GitHub Actions. Here's how to publish a new version:

#### One-Time Setup (for maintainers)

1. **Configure PyPI Trusted Publishing**:
   - Go to https://pypi.org/manage/project/jsonstat-validator/settings/
   - Add a trusted publisher with these exact settings:
     - **Owner**: `ahmed-hassan19`
     - **Repository**: `jsonstat-validator`
     - **Workflow**: `publish_to_pypi.yml`
     - **Environment**: `pypi`

2. **Create GitHub Environment**:
   - Go to repository Settings → Environments
   - Create an environment named `pypi`

#### Publishing Process

1. **Ensure tests pass locally**:
   ```bash
   uv run pytest tests/ -v
   uv run ruff check src/ tests/
   ```

2. **Create a GitHub Release**:
   - Go to [Releases](../../releases) → "Draft a new release"
   - Create a new tag: `vX.Y.Z` (e.g., `v0.3.0`)
   - Write release notes using this format:
     ```markdown
     ### Added
     - New feature X

     ### Changed
     - Updated Y

     ### Fixed
     - Fixed bug Z
     ```
   - Click "Publish release"

3. **Automatic Workflow** (takes ~2-3 minutes):
   - ✅ Runs all tests and linting
   - 🔄 Updates version in `pyproject.toml` and `__init__.py`
   - 📝 Updates `CHANGELOG.md` with your release notes
   - 📦 Builds wheel and source distribution
   - 🧪 Runs smoke tests on the build
   - 🚀 Publishes to PyPI using trusted publishing
   - 💾 Commits version/changelog updates back to `main`

#### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **Major** (`v1.0.0`): Breaking changes
- **Minor** (`v0.3.0`): New features, backward compatible
- **Patch** (`v0.2.3`): Bug fixes, backward compatible
- **Pre-release**: `v0.3.0-beta.1`, `v0.3.0-rc.1`

#### Troubleshooting

- **Tests fail**: Fix issues, push to `main`, create a new release
- **Version exists on PyPI**: Delete the GitHub release and create a new one with an incremented version
- **Trusted publishing fails**: Verify PyPI settings match exactly and the `pypi` environment exists

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- [JSON-stat](https://json-stat.org/) - For creating and maintaining the JSON-stat standard
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For the data validation framework
