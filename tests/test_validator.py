import pytest
from password_validator import PasswordValidator

@pytest.fixture
def validator():
    return PasswordValidator()

def test_valid_password(validator):
    password = "StrongPassword1!"
    errors = validator.validate(password)
    assert errors == []

def test_too_short(validator):
    password = "Short1!"
    errors = validator.validate(password)
    expected_error = f"Invalid length: must be {validator.min_length}-{validator.max_length} characters long"
    assert expected_error in errors

def test_too_long(validator):
    password = "A" * (validator.max_length + 1)
    errors = validator.validate(password)
    expected_error = f"Invalid length: must be {validator.min_length}-{validator.max_length} characters long"
    assert expected_error in errors

def test_missing_uppercase(validator):
    password = "lowercasepassword1!"
    errors = validator.validate(password)
    assert "Missing uppercase." in errors

def test_missing_lowercase(validator):
    password = "UPPERCASEPASSWORD1!"
    errors = validator.validate(password)
    assert "Missing lowercase." in errors

def test_missing_digit(validator):
    password = "NoDigitsPassword!"
    errors = validator.validate(password)
    assert "Missing digit." in errors

def test_missing_special(validator):
    password = "NoSpecialCharacter1A"
    errors = validator.validate(password)
    assert f"Missing special character (one of {validator.special_chars})." in errors

def test_spaces_not_allowed(validator):
    password = "Valid PassWord1!"
    errors = validator.validate(password)
    assert "Spaces not allowed." in errors

def test_non_string_input(validator):
    errors = validator.validate(12345)
    assert errors == ["Password must be a string."]

def test_empty_password(validator):
    errors = validator.validate("")
    assert errors == ["Password cannot be empty."]

def test_multiple_failures(validator):
    password = "short"
    errors = validator.validate(password)
    assert len(errors) > 1
    assert "Missing uppercase." in errors
    assert "Missing digit." in errors

def test_allow_spaces_enabled():
    validator = PasswordValidator(allow_spaces=True)
    password = "Valid PassWord!1"
    errors = validator.validate(password)
    assert errors == []