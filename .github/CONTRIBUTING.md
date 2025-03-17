# Contributing to JSON-stat Validator

Thank you for your interest in contributing to the JSON-stat Validator! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please be respectful and considerate of others.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include details about your environment (OS, Python version, package version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- An explanation of why this enhancement would be useful
- Any relevant examples or mockups

### Pull Requests

- Follow the Python style guide (PEP 8)
- Include appropriate tests
- Update documentation as needed
- End all files with a newline

## Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Local Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/jsonstat-validator.git
cd jsonstat-validator

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Style Guidelines

### Python Style Guide

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following specifications:

- Maximum line length: 90 characters
- Use 4 spaces for indentation (no tabs)
- Use docstrings for all public modules, functions, classes, and methods

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Additional Notes

### Issue and Pull Request Labels

This project uses labels to categorize issues and pull requests:

- `bug`: Something isn't working
- `documentation`: Improvements or additions to documentation
- `enhancement`: New feature or request
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

Thank you for contributing to the JSON-stat Validator!
