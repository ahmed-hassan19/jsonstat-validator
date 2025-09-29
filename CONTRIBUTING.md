# Contributing to JSON-stat Validator

Thank you for your interest in contributing! We welcome contributions of all kinds - bug reports, feature requests, documentation improvements, and code contributions.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Development Setup

**Clone and install:**

```bash
# Clone the repository
git clone https://github.com/ahmed-hassan19/jsonstat-validator.git
cd jsonstat-validator

# Install with development dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

**Using pip instead:**

```bash
pip install -e ".[dev]"
pre-commit install
```

## Making Changes

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** - write code, add tests, update docs
5. **Test your changes** - ensure all tests pass
6. **Commit** with clear messages
7. **Push** to your fork and **submit a Pull Request**

## Code Quality

We use several tools to maintain code quality:

- **Ruff** - Linting and formatting
- **Pytest** - Testing
- **Pre-commit** - Automated checks before commits

### Running Checks

```bash
# Run tests
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=jsonstat_validator

# Run linter
uv run ruff check src/ tests/

# Run formatter
uv run ruff format src/ tests/

# Run pre-commit hooks manually
uv run pre-commit run --all-files
```

## Testing Guidelines

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for good test coverage (we currently have 109 tests)
- Place tests in the appropriate file in `tests/` directory

## Pull Request Guidelines

Before submitting your PR:

- [ ] All tests pass locally
- [ ] Code passes linting (`ruff check`)
- [ ] Code is formatted (`ruff format`)
- [ ] New features include tests
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive

## Reporting Issues

When reporting bugs or requesting features, please include:

- **Python version** and package version
- **Minimal example** to reproduce the issue
- **Expected behavior** vs actual behavior
- **Error messages** or stack traces if applicable

Use our issue templates:

- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)

## Questions?

If you have questions about contributing:

- Review the [README](README.md) for project overview
- Check existing issues and PRs
- Open an issue for discussion
- Contact the maintainer: <ahmedhassan.ahmed@fao.org>

Thank you for your contribution! 🚀
