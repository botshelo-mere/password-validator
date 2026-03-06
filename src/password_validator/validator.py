class PasswordValidator:
    '''Simple password validator (core logic v0.1.0)'''
    def __init__(self, min_length=16, max_length=20, special_chars="!@#$%^&*", allow_spaces=False):
        '''
        Initialize the validator
        '''
        self.min_length = min_length
        self.max_length = max_length
        self.special_chars = special_chars
        self.allow_spaces = allow_spaces
            
    def _valid_length(self, password):
        return self.min_length <= len(password) <= self.max_length
    
    def _has_spaces(self, password):
        return not self.allow_spaces and any(char.isspace() for char in password)
    
    def _has_upper(self, password):
        return any(char.isupper() for char in password)
    
    def _has_lower(self, password):
        return any(char.islower() for char in password)
    
    def _has_digit(self, password):
        return any(char.isdigit() for char in password)
    
    def _has_special(self, password):
        return any(char in self.special_chars for char in password)
    
    def validate(self, password):
        '''
        Validate a password
        Return list of error messages (empty if valid)
        '''
        errors = []

        # Edge case 1: Handle non-string input
        if not isinstance(password, str):
            return ["Password must be a string."]
        
        # Edge case 2: Handle empty password
        if not password:
            return ["Password cannot be empty."]


        if not self._valid_length(password):
            errors.append(
                f"Invalid length: must be {self.min_length}-{self.max_length} characters long"
            )
 
        if self._has_spaces(password):
            errors.append("Spaces not allowed.")

        if not self._has_upper(password):
            errors.append("Missing uppercase.")

        if not self._has_lower(password):
            errors.append("Missing lowercase.")

        if not self._has_digit(password):
            errors.append("Missing digit.")

        if not self._has_special(password):
            errors.append(f"Missing special character (one of {self.special_chars}).")

        return errors
