from validator import PasswordValidator
import getpass

def display_requirements(validator):
      print("Password requirements:")
      print(f"- {validator.min_length}-{validator.max_length} characters long")
      print("- No spaces")
      print("- At least one uppercase, one lowercase, one digit")
      print(f"- At least one special character from: {validator.special_chars}\n")
            

def run_cli():
      validator = PasswordValidator()
      display_requirements(validator)
      # Loop until a valid password is entered or user exits
      while True:
            try:
                  password = getpass.getpass("Enter a password: ")
            except KeyboardInterrupt:
                  print("\nProgram interrupted by user.")
                  return
            except EOFError:
                  print("\nInput stream closed.")
                  return
                  
            errors = validator.validate(password)

            if errors:
                  for error in errors:
                        print(f"- {error}")
                  print()
            else:
                  print("\nPassword successfully created.")
                  break
