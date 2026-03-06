# Password Validator v0.1.1

A modular, rule-based password validation engine written in Python.  
**v0.1.1 Update.** Project now with `uv` to provide an isolated, reproducible environment! 
This ensures consistent behavior across machines without touching system Python.

---
## Features (v0.1.1)

- Validate password length, uppercase, lowercase, digits, special characters 
- Optional space restriction 
- CLI interface using `getpass` (interactive input) 
- Fully tested with `pytest` 
- uv environment for isolated, reproducible Python setup

---
## Project Structure

```text
password-validator/ 
    |
    ├── src/
    |    └── password_validator/
    |           |
    |           ├── __init__.py     
    |           ├── cli.py      
    |           └── validator.py      
    ├── tests/
    |   |
    |   └── test_validator.py       
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE.md
    └──.gitignore
```

---
## Installation and usage with `uv`

This project is designed to be run with `uv` - a fast Python package and project manager that keeps your system Python clean. 

1. Install `uv` (if not already)

Windows PowerShell:
``` PowerShell
pip install uv
```
or see [official installation guide](https://docs.astra.sh/uv/getting-started/installation/)

Verify:
```PowerShell
uv --version
```

2. Clone and enter the repository:

``` bash
git clone https://github.com/botshelo-mere/password-validator.git
cd password-validator
```

3. Setup the project environment

Create and synchronize the isolated Python environments
``` bash
uv lock
uv sync
```

## Running the CLI

There are two ways to interactively validate a password:

**Option 1 (Development / Debugging)**
``` bash
uv run python -m password_validator.cli
```

**Option 2 (Intalled / User-Friendly)**
``` bash
uv run validate-password
```

You will be prompted to enter a password.  
The program will:
- Display all violated rules at once
- Continue prompting until a valid password is entered
- Exit gracefully on Ctrl+C or input interruption

*Option 1 is safer for devs. Option 2 is shorter and works afer environment setup.*

## Running Tests

To execute the full test suite:
``` bash 
uv run pytest
```

The test suite verifies:
- Length boundaries (min and max)
- Character class requirements
- Space restrictions
- Multiple simultaneous rule violations
- Type validation
- Empty input handling
- Configuration toggles

### Library Usage Example

You can use the validator directly in Python code:
``` python
from password_validator import PasswordValidator
validator = PasswordValidator(min_length=12, allow_spaces=True) 
errors = validator.validate("My Password1!") 
if not errors: 
    print("Password is valid!") 
else: 
    print("Password invalid:", errors) 
```

#### Configuration Options
`PasswordValidator` supports:
- min_length and max_length (The minimum and maximum required length of characters)
- special_chars="!@#$%^&*" (Allowed special characters)
- allow_spaces=False (Whether spaces are permitted)

---
## Development Notes

- Use uv run pytest to run all tests
- CLI uses getpass — passwords are not echoed
- Validator logic is pure library, no automatic printing
- Ready for future features (v0.2.0: configurable rules, dictionary check, entropy and repeat sequences detection)

---
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

---
## Development Status

Alpha (v0.1.1)

This version improves infrastructure and packaging but does not change core validation logic.