import logging
from typing import List, Tuple, Dict, Any, Optional
from zxcvbn import zxcvbn

logger = logging.getLogger(__name__)

MAX_ZXCVBN_LEN = 72

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
    ):
        
        # Defensive Config Validation
        if min_length <= 0 or max_length < min_length:
            raise ValueError("Invalid length constraints")

        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.special_chars = special_chars
        self.allow_spaces = allow_spaces
        self.banned_words = [w.lower() for w in (banned_words or [])]

    # ===== Validation =====
    def validate(self, pwd: str) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        if not isinstance(pwd, str):
            raise ValueError("Password must be a string")

        if not pwd:
            return False, ["Password cannot be empty"]

        if not self.allow_spaces and any(c.isspace() for c in pwd):
            errors.append("Password must not contain spaces")

        if len(pwd) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")

        if len(pwd) > self.max_length:
            errors.append(f"Password cannot exceed {self.max_length} characters")

        if self.require_uppercase and not any(c.isupper() for c in pwd):
            errors.append("Missing uppercase letter")

        if self.require_lowercase and not any(c.islower() for c in pwd):
            errors.append("Missing lowercase letter")

        if self.require_digit and not any(c.isdigit() for c in pwd):
            errors.append("Missing digit")

        if self.require_special and not any(c in self.special_chars for c in pwd):
            errors.append("Missing special character")

        if self._contains_banned_word(pwd):
            errors.append("Contains a banned word")

        return len(errors) == 0, errors

    def _contains_banned_word(self, pwd: str) -> bool:
        pwd_lower = pwd.lower()
        return any(word in pwd_lower for word in self.banned_words)

    # ===== Strength (zxcvbn) =====    
    def estimate_strength(self, pwd: str) -> Dict[str, Any]:
        """
        Uses zxcvbn for realistic password strength estimation.
        Truncates passwords >72 characters to prevent ValueError.
        Always returns a dictionary, even if zxcvbn misbehaves.
        """
        if not isinstance(pwd, str) or not pwd:
            return {"score": 0, "label": "Very Weak", "feedback": ["Empty or invalid password"]}

        truncated_pwd = pwd[:MAX_ZXCVBN_LEN]

        try:
            result = zxcvbn(truncated_pwd)
            
            # Defensive: ensure result is a dict
            if not isinstance(result, dict):
                raise ValueError(f"Unexpected zxcvbn result type: {type(result)}")
        except Exception as e:
            return {"score": 0, "label": "Very Weak", "feedback": [f"Strength calculation error: {str(e)}"]}

        labels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
        score = result.get("score", 0) if isinstance(result, dict) else 0

        feedback = []
        fb_dict = result.get("feedback", {}) if isinstance(result, dict) else {}
        warning = fb_dict.get("warning")
        suggestions = fb_dict.get("suggestions", [])

        if warning:
            feedback.append(warning)
        feedback.extend(suggestions)

        return {"score": score, "label": labels[score], "feedback": feedback}
    
    # ===== Public API =====
    def evaluate(self, pwd: str) -> Dict[str, Any]:
        valid, errors = self.validate(pwd)
        strength = self.estimate_strength(pwd)
        
        return {
            "valid": valid,
            "errors": errors,
            "score": strength["score"],
            "label": strength["label"],
            "feedback": strength["feedback"]
            }
