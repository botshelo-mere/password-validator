import pytest  
import time  
import threading  
from unittest.mock import patch  
from password_validator import PasswordValidator 
from password_validator.validator import zxcvbn  # for mocking  

class TestPasswordValidator:  
    """Comprehensive tests for PasswordValidator."""  

    # ===== Initialization =====  
    def test_default_init(self):  
        v = PasswordValidator()  
        assert v.min_length == 12  
        assert v.max_length == 64  
        assert v.require_uppercase is True  
        assert v.require_lowercase is True  
        assert v.require_digit is True  
        assert v.require_special is True  
        assert v.allow_spaces is False  
        assert v.banned_words == []  

    def test_custom_init(self):  
        banned = ["password", "admin"]  
        v = PasswordValidator(  
            min_length=8,  
            max_length=32,  
            require_uppercase=False,  
            require_lowercase=False,  
            require_digit=True,  
            require_special=True,  
            special_chars="!@#",  
            allow_spaces=True,  
            banned_words=banned,  
        )  
        assert v.min_length == 8  
        assert v.max_length == 32           
        assert v.require_uppercase is False  
        assert v.require_lowercase is False  
        assert v.require_digit is True  
        assert v.require_special is True  
        assert v.special_chars == "!@#"  
        assert v.allow_spaces is True  
        assert v.banned_words == ["password", "admin"]  

    def test_invalid_length_constraints(self):  
        with pytest.raises(ValueError):  
            PasswordValidator(min_length=0)  
        with pytest.raises(ValueError):  
            PasswordValidator(min_length=-8)   
        with pytest.raises(ValueError):  
            PasswordValidator(min_length=20, max_length=10)  

    # ===== Validation =====  
    def test_validate_valid_password(self):  
        v = PasswordValidator()  
        valid, errors = v.validate("Str0ngP@ssw0rd!")  
        assert valid is True  
        assert errors == []  

    def test_validate_with_spaces_not_allowed(self):  
        v = PasswordValidator(allow_spaces=False)  
        valid, errors = v.validate("has space")  
        assert valid is False  
        assert any("spaces" in err.lower() for err in errors)  

    def test_validate_with_spaces_allowed(self):  
        # Disable other requirements to focus on spaces only  
        v = PasswordValidator(  
            allow_spaces=True,  
            require_uppercase=False,  
            require_digit=False,  
            require_special=False  
        )  
        valid, errors = v.validate("space allowed")  
        assert valid is True  
        assert errors == []  

    def test_validate_min_length(self):  
        v = PasswordValidator(min_length=12)  
        valid, errors = v.validate("short")  
        assert valid is False  
        assert any("min_length" in err.lower() or "at least" in err.lower() for err in errors)  

    def test_validate_max_length(self):  
        # Set min_length <= max_length to avoid ValueError  
        v = PasswordValidator(min_length=1, max_length=8)  
        valid, errors = v.validate("this is too long")  
        assert valid is False  
        assert any("max_length" in err.lower() or "exceed" in err.lower() for err in errors)  

    def test_validate_uppercase_required(self):  
        v = PasswordValidator(require_uppercase=True)  
        valid, errors = v.validate("lowercase123")  
        assert valid is False  
        assert any("uppercase" in err.lower() for err in errors)  

    def test_validate_lowercase_required(self):  
        v = PasswordValidator(require_lowercase=True)  
        valid, errors = v.validate("UPPERCASE123")  
        assert valid is False  
        assert any("lowercase" in err.lower() for err in errors)  

    def test_validate_digit_required(self):  
        v = PasswordValidator(require_digit=True)  
        valid, errors = v.validate("NoDigitsHere")  
        assert valid is False  
        assert any("digit" in err.lower() for err in errors)  

    def test_validate_special_required(self):  
        v = PasswordValidator(require_special=True)  
        valid, errors = v.validate("NoSpecial123")  
        assert valid is False  
        assert any("special" in err.lower() for err in errors)  

    def test_validate_special_chars_custom(self):  
        v = PasswordValidator(require_special=True, special_chars="!@#")  
        valid, errors = v.validate("has$special")  
        assert valid is False  
        assert any("special" in err.lower() for err in errors)  

    def test_validate_banned_word(self):  
        v = PasswordValidator(banned_words=["password", "secret"])  
        valid, errors = v.validate("MySecret123")  
        assert valid is False  
        assert any("banned" in err.lower() for err in errors)  

    def test_validate_banned_word_case_insensitive(self):  
        v = PasswordValidator(banned_words=["password"])  
        valid, errors = v.validate("MyPASSWORD123")  
        assert valid is False  
        assert any("banned" in err.lower() for err in errors)  

    def test_validate_empty_password(self):  
        v = PasswordValidator()  
        valid, errors = v.validate("")  
        assert valid is False  
        assert any("empty" in err.lower() for err in errors)  

    def test_validate_non_string_input(self):  
        v = PasswordValidator()  
        with pytest.raises(ValueError):  
            v.validate(123)  

    # ===== estimate_strength =====
    def test_estimate_strength_empty(self):  
        v = PasswordValidator()  
        result = v.estimate_strength("")  
        assert result["score"] == 0  
        assert result["label"] == "Very Weak"  
        assert any("empty" in msg.lower() for msg in result["feedback"])  

    def test_estimate_strength_weak(self):  
        v = PasswordValidator()  
        result = v.estimate_strength("password")  
        assert result["score"] <= 1  
        assert result["label"] in ["Very Weak", "Weak"]  

    def test_estimate_strength_strong(self):  
        v = PasswordValidator()  
        result = v.estimate_strength("CorrectHorseBatteryStaple!")  
        assert result["score"] >= 3  
        assert result["label"] in ["Strong", "Very Strong"]  

    def test_estimate_strength_structure(self):  
        v = PasswordValidator()  
        result = v.estimate_strength("Test123!")  
        # Only the keys returned by estimate_strength are expected  
        expected_keys = {"score", "label", "feedback"}  
        assert expected_keys.issubset(result.keys())  

    def test_estimate_strength_zxcvbn_exception(self):  
        """Gracefully handle zxcvbn throwing an exception."""  
        with patch('password_validator.validator.zxcvbn', side_effect=Exception("zxcvbn crashed")):  
            v = PasswordValidator()  
            result = v.estimate_strength("any")  
            assert result["score"] == 0  
            assert result["label"] == "Very Weak"  
            assert any("error" in msg.lower() for msg in result["feedback"])  

    def test_estimate_strength_malformed_zxcvbn_output(self):  
        """Handle incomplete zxcvbn response gracefully."""  
        with patch('password_validator.validator.zxcvbn', return_value={"score": 2}):   
            v = PasswordValidator()  
            result = v.estimate_strength("any")  
            assert "feedback" in result   
            assert isinstance(result["feedback"], list) 

    # ===== evaluate() =====  
    def test_evaluate_valid(self):  
        v = PasswordValidator()  
        result = v.evaluate("Str0ngP@ssw0rd!")  
        assert result["valid"] is True  
        assert result["errors"] == []  
        assert "score" in result  
        assert "label" in result  
        assert "feedback" in result   

    def test_evaluate_invalid(self):  
        v = PasswordValidator(require_digit=True)  
        result = v.evaluate("NoDigit")  
        assert result["valid"] is False  
        assert any("digit" in err.lower() for err in result["errors"])  

    # ===== Edge Cases =====  
    def test_edge_case_very_long_password(self):  
        # Disable other requirements to focus on length  
        v = PasswordValidator(  
            min_length=1,  
            max_length=100,  
            require_uppercase=False,  
            require_lowercase=False,  
            require_digit=False,  
            require_special=False  
        )  
        long_pwd = "A" * 99 + "1"  # exactly 100 chars, contains digit  
        valid, errors = v.validate(long_pwd)  
        assert valid is True  
        assert errors == []  

    def test_edge_case_password_exactly_min_length(self):  
        v = PasswordValidator(min_length=8)  
        valid, errors = v.validate("Abc123!@")  
        assert valid is True  
        assert errors == []  

    def test_edge_case_password_exceeds_max_length(self):  
        # Set min_length <= max_length to avoid ValueError  
        v = PasswordValidator(min_length=1, max_length=10)  
        valid, errors = v.validate("this is too long")  
        assert valid is False  
        assert any("exceed" in err.lower() for err in errors)  

    def test_edge_case_banned_word_embedded(self):  
        v = PasswordValidator(banned_words=["secret"])  
        valid, errors = v.validate("supersecretpassword")  
        assert valid is False  
        assert any("banned" in err.lower() for err in errors)  

    def test_edge_case_multiple_errors(self):  
        # Disable min_length and special requirement to focus on uppercase and digit  
        v = PasswordValidator(  
            min_length=1,  
            require_uppercase=True,  
            require_digit=True,  
            require_special=False  
        )  
        valid, errors = v.validate("lowercase")  
        assert valid is False  
        assert len(errors) == 2  
        assert any("uppercase" in err.lower() for err in errors)  
        assert any("digit" in err.lower() for err in errors)  

    # ===== Performance Tests =====  
    def test_performance_complex_pattern(self):  
        """Stress zxcvbn with realistic worst-case patterns."""  
        v = PasswordValidator()  
        tricky = "CorrectHorseBatteryStaple123!CorrectHorseBatteryStaple"  
        start = time.time()  
        v.estimate_strength(tricky)  
        elapsed = time.time() - start  
        assert elapsed < 2.0  # zxcvbn should handle within 2 seconds  

    def test_performance_many_iterations(self):  
        v = PasswordValidator()  
        passwords = ["password", "123456", "CorrectHorseBatteryStaple!", "P@ssw0rd"]  
        start = time.time()  
        for pwd in passwords * 100:  
            v.evaluate(pwd)  
        elapsed = time.time() - start  
        assert elapsed < 5.0  # should be fast  

    # ===== Concurrency Test =====
    def test_concurrent_evaluations(self):  
        """Multiple threads calling evaluate simultaneously should be safe."""  
        v = PasswordValidator()  
        results = []  
        lock = threading.Lock()  

        def worker(pwd):  
            try:  
                res = v.evaluate(pwd)  
                with lock:  
                    results.append(res)  
            except Exception as e:  
                with lock:  
                    results.append(e)  

        threads = []  
        # Use a password that satisfies all default requirements  
        valid_pwd = "Valid123!Pass"  # length 12, uppercase, lowercase, digit, special  
        for _ in range(50):  
            t = threading.Thread(target=worker, args=(valid_pwd,))  
            t.start()  
            threads.append(t)  

        for t in threads:  
            t.join()  

        # All results should be identical and error‑free  
        assert all(isinstance(r, dict) and r["valid"] for r in results)  

    # ===== Real‑world Passwords =====  
    def test_real_world_weak_passwords(self):  
        v = PasswordValidator()  
        weak = ["password", "123456", "qwerty", "admin", "letmein"]  
        for pwd in weak:  
            valid, _ = v.validate(pwd)  
            assert isinstance(valid, bool)  # ensure no crash  

    def test_real_world_strong_passphrase(self):  
        v = PasswordValidator()  
        strong = "correct horse battery staple"  
        valid, errors = v.validate(strong)  
        assert valid is False  # fails uppercase/digit  
        strength = v.estimate_strength(strong)  
        assert strength["score"] >= 3  # zxcvbn rates it high  

    def test_real_world_typical_user_password(self):  
        v = PasswordValidator()  
        pwd = "MySecurePassword123!"  
        valid, errors = v.validate(pwd)  
        assert valid is True  
        strength = v.estimate_strength(pwd)  
        assert strength["score"] >= 3