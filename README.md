# password-validator

[![PyPI version](https://img.shields.io/badge/pypi-v0.2.0-blue.svg)](https://pypi.org/project/password-validator/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/botshelo-mere/password-validator)
[![zxcvbn powered](https://img.shields.io/badge/strength-zxcvbn%20powered-purple.svg)](https://github.com/dwolfhub/zxcvbn-python)

A modern, policy-driven password validation library for Python — powered by
[zxcvbn](https://github.com/dwolfhub/zxcvbn-python) for realistic strength
estimation and fully configurable rule enforcement with a built-in CLI.

---

## Features

- **Policy validation** — enforce length, character classes, spaces, and banned words
- **Realistic strength scoring** — zxcvbn rates passwords 0–4 with human-readable labels
- **Unified `evaluate()` API** — combines validation + strength in one call
- **CLI interface** — interactive (colored) and non-interactive (JSON pipe) modes
- **Resilient design** — defensive constructor, graceful zxcvbn exception handling
- **Thread-safe** — safe to share a single `PasswordValidator` across threads
- **Typed** — full `typing` annotations throughout

---

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/botshelo-mere/password-validator.git
cd password-validator

# Create virtual environment and install dependencies
uv sync
```

### Using pip

```bash
pip install password-validator
```

### Dev / Testing

```bash
# Install with development extras (pytest, pytest-cov, pytest-benchmark, jsonschema)
uv sync --extra dev
# or
pip install "password-validator[dev]"
```

---

## Quick Start

### Library Usage

```python
from password_validator import PasswordValidator

# Default policy: 12–64 chars, upper, lower, digit, special required
validator = PasswordValidator()

# --- validate() → (bool, list[str]) ---
valid, errors = validator.validate("Str0ngP@ssw0rd!")
print(valid)   # True
print(errors)  # []

valid, errors = validator.validate("weak")
print(valid)   # False
print(errors)  # ['Password must be at least 12 characters long', ...]

# --- estimate_strength() → dict ---
strength = validator.estimate_strength("Str0ngP@ssw0rd!")
print(strength["score"])    # 3
print(strength["label"])    # 'Strong'
print(strength["feedback"]) # []

# --- evaluate() — combines both in one call ---
result = validator.evaluate("Str0ngP@ssw0rd!")
# {
#   "valid": True,
#   "errors": [],
#   "score": 3,
#   "label": "Strong",
#   "feedback": []
# }
```

### Custom Policy

```python
validator = PasswordValidator(
    min_length=8,
    max_length=32,
    require_uppercase=True,
    require_lowercase=True,
    require_digit=True,
    require_special=True,
    special_chars="!@#$%",
    allow_spaces=False,
    banned_words=["password", "admin", "secret"],
)

valid, errors = validator.validate("Admin123!")
# valid=False → "Contains a banned word"
```

---

## Configuration Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `min_length` | `int` | `12` | Minimum password length (must be ≥ 1) |
| `max_length` | `int` | `64` | Maximum password length (must be ≥ `min_length`) |
| `require_uppercase` | `bool` | `True` | Require at least one uppercase letter |
| `require_lowercase` | `bool` | `True` | Require at least one lowercase letter |
| `require_digit` | `bool` | `True` | Require at least one digit |
| `require_special` | `bool` | `True` | Require at least one special character |
| `special_chars` | `str` | `"!@#$%^&*"` | Set of accepted special characters |
| `allow_spaces` | `bool` | `False` | Whether whitespace is permitted |
| `banned_words` | `list[str] \| None` | `None` | Case-insensitive list of forbidden words |

> `ValueError` is raised on construction if `min_length <= 0` or `max_length < min_length`.

---

## API Reference

### `PasswordValidator.validate(pwd: str) → Tuple[bool, List[str]]`

Runs all configured policy rules against the password.

- Returns `(True, [])` if all rules pass.
- Returns `(False, [<error messages>])` if any rule fails.
- Raises `ValueError` if `pwd` is not a `str`.

### `PasswordValidator.estimate_strength(pwd: str) → Dict[str, Any]`

Uses zxcvbn to estimate password strength.

- Passwords longer than 72 characters are truncated before scoring (zxcvbn limit).
- Always returns a dictionary — never raises.

| Key | Type | Description |
|---|---|---|
| `score` | `int` | 0 (Very Weak) → 4 (Very Strong) |
| `label` | `str` | Human-readable label |
| `feedback` | `list[str]` | Warnings and suggestions from zxcvbn |

### `PasswordValidator.evaluate(pwd: str) → Dict[str, Any]`

Combines `validate()` and `estimate_strength()` into a single result.

| Key | Type | Description |
|---|---|---|
| `valid` | `bool` | Whether all policy rules passed |
| `errors` | `list[str]` | Policy error messages |
| `score` | `int` | zxcvbn score 0–4 |
| `label` | `str` | Strength label |
| `feedback` | `list[str]` | zxcvbn feedback |

---

## CLI Usage

### Interactive Mode

```bash
uv run password-validator
```

```
Password Validator v0.2.0 (zxcvbn powered)
Type .exit() to quit

Enter password: ········
✓ Valid password

Strength: Strong
  • Use a longer keyboard pattern with more turns
```

- Type `.exit()` to quit.
- Press `Ctrl+C` to interrupt.
- Password input is hidden (no echo).

### Non-Interactive / Pipe Mode

Pipe a password directly — output is JSON, exit code is `0` for score ≥ 3, `1` otherwise:

```bash
echo "Str0ngP@ssw0rd!" | password-validator
```

```json
{
  "valid": true,
  "errors": [],
  "score": 3,
  "label": "Strong",
  "feedback": []
}
```

Ideal for shell scripts and CI pipelines:

```bash
echo "$PASSWORD" | password-validator && echo "Password accepted" || echo "Password rejected"
```

---

## Project Structure

```
password-validator/
├── pyproject.toml                  # Project configuration
├── .gitignore
├── README.md
├── LICENSE.md
├── src/
│   └── password_validator/
│       ├── __init__.py             # Public API  (__version__, __all__)
│       ├── validator.py            # Core validation + zxcvbn strength logic
│       └── cli.py                  # CLI interface (colorama)
└── tests/
    ├── __init__.py
    ├── test_validator.py           # Validator unit tests
    ├── test_cli.py                 # CLI unit tests
    └── test_performance_benchmarks.py  # pytest-benchmark performance tests
```

---

## Development

### Running Tests

```bash
# All tests
uv run pytest

# With coverage report
uv run pytest --cov=password_validator --cov-report=term-missing

# Verbose output
uv run pytest -v
```

### Running Benchmarks

```bash
uv run pytest tests/test_performance_benchmarks.py --benchmark-only
```

### Code Coverage

```bash
uv run pytest --cov=password_validator --cov-branch --cov-report=html
# Open htmlcov/index.html in your browser
```

---

## Strength Score Labels

| Score | Label | Meaning |
|---|---|---|
| 0 | Very Weak | Trivially crackable |
| 1 | Weak | Easy to crack |
| 2 | Moderate | Some resistance |
| 3 | Strong | Good security |
| 4 | Very Strong | Excellent security |

Scoring is provided by [zxcvbn](https://github.com/dwolfhub/zxcvbn-python), which
models real-world cracking strategies (dictionary attacks, keyboard patterns, etc.)
rather than simple character-class rules.

---

## Version History

| Version | Changes |
|---|---|
| **v0.2.0** | Added zxcvbn strength estimation, `evaluate()` API, banned words, full type annotations, colorama CLI, pipe mode, comprehensive test suite |
| **v0.1.1** | Infrastructure improvements, packaging fixes |
| **v0.1.0** | Initial public release |

---

## License

This project is licensed under the MIT License — see [LICENSE.md](LICENSE.md) for details.

---

## Author

**Botshelo Mere**
GitHub: [botshelo-mere](https://github.com/botshelo-mere)