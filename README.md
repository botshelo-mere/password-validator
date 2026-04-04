# FortifyPass - Real-World Password Security for Developers

## Need better password validation in your project?

Most rules either let weak passwords through or frustrate users into abondoning.

Send me a code snippet or repo link of your current signup/auth flow.
I'll review it async and show specific improvements using `FortifyPass` (written feedback + code suggestions)

Free for the first 5 people this week. Just DM me on X [@botshelo_dev](https://x.com/botshelo_dev) or reply here.

---

[![PyPI version](https://img.shields.io/badge/pypi-v0.2.1-blue.svg)](https://pypi.org/project/fortifypass/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/botshelo-mere/fortifypass)
[![zxcvbn powered](https://img.shields.io/badge/strength-zxcvbn%20powered-purple.svg)](https://github.com/dwolfhub/zxcvbn-python)

> Every day, companies get breached because someone picked `123456` or `password`. Users think complexity is optional. Developers hope nobody notices. Security teams cry. FortifyPass guarantees your users pick passwords that actually protect them - real-world strong, actinable, and verifiable

## Why Everyone will Agree

- **Weak passwords are everywhere** - your users do it, your friends do it, your systems get hacked.
- **Length or character checks don't cut it** - hackers exploit patterns, common words, and sequences.
- **Feedback is terrible in almost every validator** - users ignore it, reuse passwords, and risk breaches skyrocket.

Your system is only as secure as the weakest password. FortifyPass fixes that.

## Why You'll Want This

FortifyPass doesn't just validate - it forces strong passwords and explains why:
- Real-world strength scoring powered by `zxcvbn`
- **Policy enforcement**: uppercase, lowercase, digits, special, characters, banned words
- **Actionable feedback**: your users actually learn to make secure passwords
- **Plug-and-Play**: works in Python, CLI, scripts, and future APIs

---

## Quick Demo

### Interactive CLI Mode

Run `fortifypass` directly in your terminal for real-time feedback

![Interactive CLI Demo](assets/demo-cli-interactive.png)

### Non-Interactive / Pipe mode

For automated workflows, pipe passwords directly. Output is JSON with validation results

![Pipe Mode Demo](assets/demo-pipe-usage1.png)

Validate passwords programmatically in scripts and pipelines

![Pipe Mode Demo](assets/demo-pipe-usage2.png)

---

## Installation

### Using pip (standard)

``` bash
pip install fortifypass
```

### Using uv (fast alternative)

Install `uv` (if not already) or see [official installation guides](https://docs.astral.sh/uv/getting-started/installation/)
```
pip install uv
```

``` bash
uv add fortifypass
```

if you're working in a project:
``` bash
uv sync
```

### From Source

```bash
git clone https://github.com/botshelo-mere/fortifypass.git
cd fortifypass

# Using pip
pip install .

# Using uv
uv sync
```

### Dev / Testing

```bash
# Using pip
pip install "fortifypass[dev]"

# Using uv
uv sync --extra dev
```
---

## Quick Start

### Library Usage

```python
from fortifypass import PasswordValidator

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
    banned_words=["password", "admin", "secret"]
)

valid, errors = validator.validate("Admin123!")
# valid=False → "Contains a banned word"
```

---

## Configuration Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `min_length` | `int` | `12` | Minimum password length |
| `max_length` | `int` | `64` | Maximum password length |
| `require_uppercase` | `bool` | `True` | Require at least one uppercase letter |
| `require_lowercase` | `bool` | `True` | Require at least one lowercase letter |
| `require_digit` | `bool` | `True` | Require at least one digit |
| `require_special` | `bool` | `True` | Require at least one special character |
| `special_chars` | `str` | `"!@#$%^&*"` | Set of allowed special characters |
| `allow_spaces` | `bool` | `False` | Whether whitespace is permitted |
| `banned_words` | `list[str] \| None` | `None` | Case-insensitive list of forbidden words |
| `min_score` | `int` | `0` | Minimum zxcvbn score (0-4) |

> `ValueError` is raised on construction if `min_length <= 0` or `max_length < min_length`.  
> `ValueError` is raised on construction if `min_score < 0` or not `0 <= min_score <= 4`.

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
| `policy_passed` | `bool` | Policy Compliance |
| `strength_passed` | `bool` | `score` >= `min_core` |
| `errors` | `list[str]` | Policy error messages |
| `score` | `int` | zxcvbn score 0–4 |
| `label` | `str` | Strength label |
| `feedback` | `list[str]` | zxcvbn feedback |

---

## CLI Usage

### Interactive Mode
``` bash
fortifypass 

# Or use uv
uv run fortifypass
```

- Password input is hidden (no echo).
- Type `.exit()` to quit.
- Press `Ctrl+C` to interrupt.

### Non-Interactive / Pipe Mode

Pipe a password directly — output is JSON, exit code is `0` for score ≥ 3, `1` otherwise:

```bash
echo "Str0ngP@ssw0rd!" | fortifypass
```

Ideal for shell scripts and CI pipelines:

```bash
echo "$PASSWORD" | fortifypass && echo "Password accepted" || echo "Password rejected"
```

> Exit code is 0 only if the password passes **both policy and strength requirements**

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

## Development

### Running Tests

```bash
# All tests
uv run pytest

# With coverage report
uv run pytest --cov=fortifypass --cov-report=term-missing

# Verbose output
uv run pytest -v

# Run a specific test function
uv run pytest tests/test_validator.py::Testvalidate::test_validate_valid_password
```

### Running Benchmarks

```bash
uv run pytest tests/test_performance_benchmarks.py --benchmark-only
```

### Code Coverage

```bash
uv run pytest --cov=fortifypass --cov-branch --cov-report=html
# Open htmlcov/index.html in your browser
```

> **NOTE**: `uv run pytest` works because `pytest` is installed in the uv environment. Do not run `python test_validator.py` direclty - the test framework will not discover functions.

---

## Version History

| Version | Changes |
|---|---|
| **v0.2.1** | Fixed password score display issue, improved CLI output formatting, enhanced feedback, internal improvements for stability |
| **v0.2.0** | Added zxcvbn strength estimation, `evaluate()` API, banned words, full type annotations, colorama CLI, pipe mode, comprehensive test suite |
| **v0.1.1** | Infrastructure improvements, packaging fixes |
| **v0.1.0** | Initial public release |

---

## License

This project is licensed under the MIT License — see [LICENSE.md](https://github.com/botshelo-mere/fortifypass/blob/main/LICENSE.md) for details.

---

## Author

**Botshelo Mere**  
GitHub: [botshelo-mere](https://github.com/botshelo-mere)