import sys
import json
import getpass
from colorama import init, Fore, Style
from fortifypass.validator import PasswordValidator

# Initialize Colorama
init(autoreset=True)

def main():
    validator = PasswordValidator.secure()

    # Handle piped input (non-interactive)
    if not sys.stdin.isatty():
        pwd = sys.stdin.read().strip()
        
        result = validator.evaluate(pwd)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["valid"] else 1)

    # Interactive mode
    print(Fore.CYAN + Style.BRIGHT + "FortifyPass version 0.2.1")
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
        if not result["policy_passed"]:
            print(Fore.RED + Style.BRIGHT + "✗ Does not meet policy requirements")
            for err in result["errors"]:
                print(Fore.RED + Style.BRIGHT + f"  • {err}")

        if result["strength_passed"]:
            print(Fore.GREEN + Style.BRIGHT + "✓ Strong against common attacks")
        else:
            print(Fore.RED + Style.BRIGHT + "✗ Too weak against common attacks")

        # Strength output
        score_color = {
            0: Fore.RED + Style.BRIGHT,
            1: Fore.RED + Style.BRIGHT,
            2: Fore.YELLOW + Style.BRIGHT,
            3: Fore.GREEN + Style.BRIGHT,
            4: Fore.GREEN + Style.BRIGHT,
        }[result["score"]]

        print(f"\n{score_color }Score: {result['score']}/4")
        print(f"{score_color}Strength: {result['label']}")
        
        if result["feedback"]:
            print("\nFeedback:")
            for msg in result["feedback"]:
                print(Fore.YELLOW + f"  • {msg}")

        print()
        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()