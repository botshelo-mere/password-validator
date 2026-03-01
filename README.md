# Password Validator v0.1.0

A modular, rule-based password validation engine written in Python.  
v0.1.0 delivers a stable core validation system with configurable rules,
a functional CLI interface, and full unit test coverage, ready to integrate
or experiment with in Python projects.

**Who is it for:** Developers, learners, and educators seeking a tested, configurable
password validation systems.

**Why it matters:** Enforces a strong structural rules, preventing weak passwords while
providing a foundation for more advanced security features. 

This release focuses strictly on deterministic rule enforcement - it does not
perform entropy analysis, pattern detection, or dictionary-based checks. 
Those improvements are reserved for future releases.

---
## Features (v0.1.0)

- Configurable minimum and maximum length
- Uppercase requirement
- Lowercase requirement
- Digit requirement
- Special character requirement
- Optional space restriction
- Multiple error reporting (returns all violations at once)
- Command-line interface (CLI)
- Unit tests using unittest

---
## Project Structure

```text
password-validator/ 
    |
    ├── validator.py        # Core validation engine 
    ├── cli.py      # Command-line interface 
    ├── main.py     # Application entry point 
    ├── test_validator.py       # Unit test suite 
    ├── README.md
    ├── LICENSE.md
    └──.gitgnore
```

---
## Default Validation Rules

By default, the validator enforces:
- Length: 16–20 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character from: !@#$%^&*
- Spaces are not allowed

These rules can be customized during initialization.

#### Example: Programmatic Usage

``` python
from validator import PasswordValidator 

validator = PasswordValidator() 
password = "StrongPassword1!" 
errors = validator.validate(password)

if errors:
    for error in errors: 
        print(error)
    print()
else: 
    print("Password is valid.") 
```

#### Custom configuration example:

```  python
validator = PasswordValidator(
    min_length=12,
    max_length=32,
    special_chars="!@#$%",
    allow_spaces=True
) 
```

---
## Installation

Clone the repository:
``` bash
git clone https://github.com/botshelo-mere/password-validator.git
cd password-validator
```

## Running the CLI

Run the application:
``` bash
python main.py 
```

You will be prompted to enter a password.  
The program will:
- Display all violated rules at once
- Continue prompting until a valid password is entered
- Exit gracefully on Ctrl+C or input interruption

## Running Tests

To execute the full test suite:
``` bash 
python -m unittest test_validator.py
```

The test suite verifies:
- Length boundaries (min and max)
- Character class requirements
- Space restrictions
- Multiple simultaneous rule violations
- Type validation
- Empty input handling
- Configuration toggles

All tests must pass before tagging a release.

---
## Design Principles

This project emphasizes:
- Clear separation of concerns
- Deterministic rule enforcement
- Explicit error reporting
- Incremental versioning
- Test-backed stability

It is intentionally minimal in scope at this stage.

---
## Scope Clarification

This is not:
- A password strength estimator
- An entropy analyzer
- A dictionary attack detector
- A cryptographic security tool
- A password manager

Future versions may introduce more advanced validation logic.

---
## Roadmap

### v0.1.0 – Core Validation Engine
- Stable rule enforcement
- Functional CLI
- Test coverage

### v0.2.0 – Enhanced Validation (Planned)
- Pattern repetition detection
- Basic entropy estimation
- Rule toggling system
- Improved configurability

### v0.3.0 – Password Generator (Planned)
- Secure random password generation
- Integration with validator

## Versioning

This project follows semantic versioning principles:
- MAJOR – Breaking changes
- MINOR – Feature additions
- PATCH – Fixes and improvements

Current version: v0.1.0

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.