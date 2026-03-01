import unittest
from validator import PasswordValidator


class TestPasswordValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = PasswordValidator()

    def test_valid_password(self):
        """A fully compliant password should return no errors."""
        password = "StrongPassword1!"
        errors = self.validator.validate(password)
        self.assertEqual(errors, [])

    def test_too_short(self):
        """Passwords shorter than the minimum length should fail."""
        password = "Short1!"
        errors = self.validator.validate(password)
        expected_error = (
            f"Invalid length: must be {self.validator.min_length}-{self.validator.max_length} characters long"
        )
        self.assertIn(expected_error, errors)

    def test_too_long(self):
        password = "A" * (self.validator.max_length + 1)
        errors = self.validator.validate(password)
        expected_error = (
            f"Invalid length: must be {self.validator.min_length}-{self.validator.max_length} characters long"
        )
        self.assertIn(expected_error, errors)
        
    def test_missing_uppercase(self):
        """Password without uppercase characters should fail."""
        password = "lowercasepassword1!"
        errors = self.validator.validate(password)
        self.assertIn("Missing uppercase.", errors)

    def test_missing_lowercase(self):
        """Password without lowercase characters should fail."""
        password = "UPPERCASEPASSWORD1!"
        errors = self.validator.validate(password)
        self.assertIn("Missing lowercase.", errors)

    def test_missing_digit(self):
        """Password without numeric characters should fail."""
        password = "NoDigitsPassword!"
        errors = self.validator.validate(password)
        self.assertIn("Missing digit.", errors)
        
    def test_missing_special_character(self):
        """Password without a required special character should fail."""
        password = "NoSpecialCharacter1A"
        errors = self.validator.validate(password)
        expected_error = (
            f"Missing special character (one of {self.validator.special_chars})."
        )
        self.assertIn(expected_error, errors)

    def test_spaces_not_allowed(self):
        """Passwords containing spaces should fail when spaces are disabled."""
        password = "Valid PassWord1!"
        errors = self.validator.validate(password)
        self.assertIn("Spaces not allowed.", errors)
    
    def test_non_string_input(self):
        """Non-string input should immediately return a type error."""
        errors = self.validator.validate(12345)
        self.assertEqual(errors, ["Password must be a string."])

    def test_empty_password(self):
        """Empty string input should return a specific empty error."""
        errors = self.validator.validate("")
        self.assertEqual(errors, ["Password cannot be empty."])

    def test_multiple_failures(self):
        """Password violating multiple rules should report all relevant errors."""
        password = "short"
        errors = self.validator.validate(password)
        
        self.assertGreater(len(errors), 1)
        self.assertIn("Missing uppercase.",errors)
        self.assertIn("Missing digit.",errors)
    
    def test_allow_spaces_enabled(self):
        validator = PasswordValidator(allow_spaces=True)
        password = "Valid PassWord!1"
        errors = validator.validate(password)
        self.assertEqual(errors, [])
        

if __name__ == "__main__":
    unittest.main()