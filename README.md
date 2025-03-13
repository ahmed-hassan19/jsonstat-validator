# JSON-stat Validator

[![PyPI version](https://img.shields.io/pypi/v/jsonstat-validator.svg)](https://pypi.org/project/jsonstat-validator/)
[![Python Version](https://img.shields.io/pypi/pyversions/jsonstat-validator.svg)](https://pypi.org/project/jsonstat-validator/)
[![License](https://img.shields.io/github/license/ahmed-hassan19/jsonstat-validator.svg)](https://github.com/ahmed-hassan19/jsonstat-validator/blob/main/LICENSE)

A Python validator for the JSON-stat 2.0 standard format, based on Pydantic.

JSON-stat is a simple lightweight format for data interchange. It is a JSON format for data dissemination that allows the representation of statistical data in a way that is both simple and convenient for data processing. With this validator, you can ensure your data conforms to the official [JSON-stat 2.0 specification](https://json-stat.org/full/).

## Installation

```bash
pip install jsonstat-validator
```

## Usage

### Basic Validation

```python
import json
from jsonstat_validator import validate_jsonstat

# Load or define your JSON-stat object
# You can start by using one of the provided sample files
with open("jsonstat_validator/tests/samples/oecd.json", "r") as f:
    jsonstat_obj = json.load(f)

# Validate the data
try:
    validate_jsonstat(data)
    print("Valid JSON-stat object!")
except ValueError as e:
    print(f"Validation failed: {e}")
```

### Example JSON-stat Dataset

Here's a simplified example of a JSON-stat dataset representing unemployment data:

```json
{
  "version": "2.0",
  "class": "dataset",
  "label": "Unemployment rate sample",
  "source": "Sample data",
  "updated": "2023-01-15",
  "id": ["indicator", "area", "year"],
  "size": [1, 3, 2],
  "value": [5.8, 6.2, 7.1, 7.5, 4.2, 4.9],
  "role": {
    "time": ["year"],
    "geo": ["area"],
    "metric": ["indicator"]
  },
  "dimension": {
    "indicator": {
      "label": "Economic indicator",
      "category": {
        "label": {
          "UNR": "unemployment rate"
        },
        "unit": {
          "UNR": {
            "symbol": "%",
            "decimals": 1
          }
        }
      }
    },
    "year": {
      "label": "Year",
      "category": {
        "index": ["2020", "2021"]
      }
    },
    "area": {
      "label": "Country",
      "category": {
        "index": ["US", "JP", "EU"],
        "label": {
          "US": "United States",
          "JP": "Japan",
          "EU": "European Union"
        }
      }
    }
  }
}
```

## Features

- Validates JSON-stat data against the [full 2.0 specification](https://json-stat.org/full).
- Provides models for all major JSON-stat responses: **Dataset**, **Dimension**, **Collection**.
- Built on Pydantic for robust type validation and error messages.
- Provides tests against the [official JSON-stat samples](https://json-stat.org/samples/collection.json) as well as custom fine-grained tests.

## Testing

The validator has been thoroughly tested with all official JSON-stat samples from the [JSON-stat website](https://json-stat.org/samples/).

To run tests:

First, install the development dependencies:

```bash
pip install jsonstat-validator[dev]
```

Then run the tests:

```bash
pytest
```

To run a specific test file (e.g. test official samples only):

```bash
pytest tests/test_official_samples.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add some new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Credits

This package is maintained by Ahmed Hassan ([@ahmed-hassan19](https://github.com/ahmed-hassan19)) and was created for use at the Food and Agriculture Organization (FAO) of the United Nations.

The JSON-stat format was created by [Xavier Badosa](https://www.linkedin.com/in/badosa).
