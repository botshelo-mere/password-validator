# Password Validator

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/botshelo-mere/password-validator)

A modular, rule-based password validation engine written in Python with both library and CLI interfaces.

## Overview

The Password Validator provides customizable security rules for password validation, supporting:
- Configurable length requirements
- Character class validation (uppercase, lowercase, digits, special characters)
- Optional space restrictions
- Both programmatic API and command-line interface
- Comprehensive test coverage

## Quick Start

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for fast, isolated Python environment management.

### Installation

1. **Install uv** (if not already installed):
   ```bash
   # Via pip
   pip install uv
   
   # Or follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/)
   ```

2. **Clone and setup the project**:
   ```bash
   git clone https://github.com/botshelo-mere/password-validator.git
   cd password-validator
   
   # Create and sync the isolated environment
   uv lock
   uv sync
   ```

## Usage

### Command Line Interface

Run the CLI tool interactively:

```bash
# Development mode
uv run python -m password_validator.cli

# Or after installation
uv run validate-password
```

The CLI will:
- Display current password requirements
- Prompt for password input securely (no echo)
- Show validation errors or success message
- Loop until valid password is entered or user exits (Ctrl+C)

### Library Usage

Use the validator in your Python code:

```python
from password_validator import PasswordValidator

# Create validator with custom rules
validator = PasswordValidator(
    min_length=12,
    max_length=32,
    special_chars="!@#$%",
    allow_spaces=True
)

# Validate password
errors = validator.validate("My Password1!")

if not errors:
    print("Password is valid!")
else:
    print("Password invalid:", errors)
```

### Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_length` | 16 | Minimum password length |
| `max_length` | 20 | Maximum password length |
| `special_chars` | "!@#$%^&*" | Allowed special characters |
| `allow_spaces` | False | Whether spaces are permitted |

## Project Structure

```
password-validator/
├── src/
│   └── password_validator/
│       ├── __init__.py          # Public API
│       ├── cli.py              # CLI interface
│       └── validator.py        # Core validation logic
├── tests/
│   └── test_validator.py       # Test suite
├── pyproject.toml              # Project configuration
├── README.md                  
├── LICENSE.md                  
└── .gitignore                  
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/test_validator.py::test_valid_password
```

### Test Coverage

The test suite validates:
- Length boundaries (min/max)
- Character class requirements
- Space restrictions
- Multiple rule violations
- Type validation and edge cases
- Configuration toggles

## Version History

- **v0.1.1** - Infrastructure improvements and documentation updates
- **v0.1.0** - Initial public release

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Author

**Botshelo Mere**  
GitHub: [botshelo-mere](https://github.com/botshelo-mere)