import logging
from typing import List, Tuple, Dict, Any, Optional
from zxcvbn import zxcvbn
import re

logger = logging.getLogger(__name__)

MAX_ZXCVBN_LEN = 72
SEQUENCES = [
"abcdefghijklmnopqrstuvwxyz",
"0123456789",
]

KEYBOARD_PATTERNS = [
"qwerty", "asdfgh", "zxcvbn",
"123456", "654321"
]

class PasswordValidator:
    def __init__(
        self,
        min_length: int = 12,
        max_length: int = 64,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        special_chars: str = "!@#$%^&*",
        allow_spaces: bool = False,
        banned_words: Optional[List[str]] = None,
        min_score: int = 0
    ):
        
        # Defensive Config Validation
        if min_length <= 0 or max_length < min_length:
            raise ValueError("Invalid length constraints")
        
        if min_score < 0:
            raise ValueError("min_score must be > 0")
        
        if not (0 <= min_score <= 4):
            raise ValueError("min_score must be between 0 and 4")
        
        if not any([
            require_uppercase,
            require_lowercase,
            require_digit,
            require_special
        ]):
            raise ValueError("At least one character requirement must be enabled")

        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.special_chars = special_chars
        self.allow_spaces = allow_spaces
        self.banned_words = [w.lower() for w in (banned_words or [])]
        self.min_score = min_score
        
    # ===== Factory Presets =====
    @classmethod
    def secure(cls):
        return cls(min_length=12, min_score=3)

    @classmethod
    def strict(cls):
        return cls(min_length=16, min_score=4)

    @classmethod
    def relaxed(cls):
        return cls(
            min_length=8,
            require_uppercase=False,
            require_special=False,
            min_score=2
        )
        
    # =====  Pattern Detection =====
    def _detect_sequence_runs(self, pwd: str) -> bool:  
        p = pwd.lower()  
        for seq in SEQUENCES:  
            for i in range(len(seq) - 2):  
                for length in range(3, min(6, len(seq) - i + 1)):  
                    sub = seq[i:i+length]  
                    if sub in p or sub[::-1] in p:  
                        return True  
        return False  

    def _detect_keyboard_patterns(self, pwd: str) -> bool:  
        pwd_lower = pwd.lower()  
        return any(pattern in pwd_lower for pattern in KEYBOARD_PATTERNS)  

    def _has_repetition(self, pwd: str) -> bool:
        # aaa OR abab OR 1212
        return bool(re.search(r"(..+)\1", pwd) or re.search(r"(.)\1{2,}", pwd))
    
    # ===== Policy Validation =====
    def validate(self, pwd: str) -> Tuple[bool, List[str]]:
        if not isinstance(pwd, str):
            raise ValueError("Password must be a string")

        errors: List[str] = []

        if not pwd:
            return False, ["Password cannot be empty"]

        if not self.allow_spaces and any(c.isspace() for c in pwd):
            errors.append("Policy requirement: no spaces allowed")

        if len(pwd) < self.min_length:
            errors.append(f"Policy requirement: minimum length is {self.min_length}")

        if len(pwd) > self.max_length:
            errors.append(f"Policy requirement: maximum length is {self.max_length}")
            
        # Single pass classification
        has_digit = has_upper = has_lower = has_special = False
        
        for c in pwd:
            if c.isdigit():
                has_digit = True
            elif c.isupper():
                has_upper = True
            elif c.islower():
                has_lower = True
            elif c in self.special_chars:
                has_special = True

        if self.require_uppercase and not has_upper:
            errors.append("Policy requirement: add at least one uppercase letter")

        if self.require_lowercase and not has_lower:
            errors.append("Policy requirement: add at least one lowercase letter")

        if self.require_digit and not has_digit:
            errors.append("Policy requirement: add at least one digit")

        if self.require_special and not has_special:
            errors.append("Policy requirement: add at least one special character")

        if any(word in pwd.lower() for word in self.banned_words):
            errors.append("Policy requirement: contains a banned word")
        
        if self._detect_sequence_runs(pwd):  
            errors.append("Contains sequential pattern")  
            
        if self._detect_keyboard_patterns(pwd):  
            errors.append("Contains keyboard pattern")  
            
        if self._has_repetition(pwd):  
            errors.append("Contains repetition")  

        return len(errors) == 0, errors
   
    #===== Strength Estimation =====
    def estimate_strength(self, pwd: str) -> Dict[str, Any]:
        if not isinstance(pwd, str) or not pwd:
            return {"score": 0, "label": "Very Weak", "feedback": ["Empty or invalid password"]}

        truncated_pwd = pwd[:MAX_ZXCVBN_LEN]
        
        labels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
        score = 0 
        feedback = []

        try:
            result = zxcvbn(truncated_pwd)
            
            # Defensive: ensure result is a dict
            if not isinstance(result, dict):
                raise ValueError(f"Unexpected zxcvbn result type: {type(result)}")

            score = int(result.get("score", 0))
            score = max(0, min(score, 4))
            fb_dict = result.get("feedback", {})
            warning = fb_dict.get("warning")
            suggestions = fb_dict.get("suggestions", [])

            if warning:
                feedback.append(warning)
            feedback.extend(suggestions)
        
        except Exception as e:
            feedback.append(f"Strength calculation error: {str(e)}")
            score = 0
        
        return {"score": score, "label": labels[score], "feedback": feedback}
    
    # ===== Public API =====
    def evaluate(self, pwd: str) -> Dict[str, Any]:
        policy_passed, errors = self.validate(pwd)
        strength = self.estimate_strength(pwd)
        
        score = strength["score"]
        strength_passed = score >= self.min_score
        
        valid = policy_passed and strength_passed

        # Strength failure message. 
        if policy_passed and not strength_passed:
            errors.append(
                f"Password is too weak (score: {score}). Minimum required is {self.min_score}"
            )

        return {
            "valid": valid,
            "policy_passed": policy_passed,
            "strength_passed": strength_passed,
            "errors": errors,
            "score": strength["score"],
            "label": strength["label"],
            "feedback": strength["feedback"]
            }
