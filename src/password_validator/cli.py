import sys
import json
import getpass
from colorama import init, Fore, Style
from password_validator.validator import PasswordValidator, MAX_ZXCVBN_LEN

# Initialize Colorama
init(autoreset=True)

def main():
    validator = PasswordValidator()

    # Handle piped input (non-interactive)
    if not sys.stdin.isatty():
        pwd = sys.stdin.read().strip()
        
        result = validator.evaluate(pwd)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["score"] >= 3 else 1)

    # Interactive mode
    print(Fore.CYAN + Style.BRIGHT + "Password Validator v0.2.0 (zxcvbn powered)")
    print(Fore.CYAN + "Type .exit() to quit\n")

    while True:
        try:
            pwd = getpass.getpass("Enter password: ")
        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "Program interrupted by user.")
            return
        except EOFError:
            print("\n" + Fore.YELLOW + "Input stream closed.")
            return

        if pwd == ".exit()":
            print(Fore.YELLOW + "Goodbye.")
            return

        result = validator.evaluate(pwd)

        # Validation output
        if result["valid"]:
            print(Fore.GREEN + Style.BRIGHT + "✓ Valid password")
        else:
            print(Fore.RED + Style.BRIGHT + "✗ Invalid password")
            for err in result["errors"]:
                print(Fore.RED + Style.BRIGHT + f"  • {err}")

        # Strength output
        score_color = {
            0: Fore.RED + Style.BRIGHT,
            1: Fore.RED + Style.BRIGHT,
            2: Fore.YELLOW + Style.BRIGHT,
            3: Fore.GREEN + Style.BRIGHT,
            4: Fore.GREEN + Style.BRIGHT,
        }[result["score"]]

        print(f"\n{score_color }Strength: {result['label']}")
        for msg in result["feedback"]:
            print(Fore.YELLOW + f"  • {msg}")

        print()

if __name__ == "__main__":
    main()