import sys
import json
import jsonschema
import pytest
from io import StringIO
from unittest.mock import patch
from fortifypass.cli import main

# Define the expected JSON schema for non‑interactive output
CLI_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "valid": {"type": "boolean"},
        "errors": {"type": "array", "items": {"type": "string"}},
        "score": {"type": "integer", "minimum": 0, "maximum": 4},
        "label": {"type": "string"},
        "feedback": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["valid", "errors", "score", "label", "feedback"],
}

class TestCLI:
    """Tests for the command line interface."""

    # ===== Non‑interactive (piping) =====
    def test_non_interactive_valid_password(self, capsys):
        sys.stdin = StringIO("Str0ngP@ssw0rd!")
        with patch('sys.stdin.isatty', return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        out, _ = capsys.readouterr()
        result = json.loads(out.strip())
        jsonschema.validate(instance=result, schema=CLI_OUTPUT_SCHEMA)
        assert result["valid"] is True
        assert result["score"] >= 3

    def test_non_interactive_invalid_password(self, capsys):
        sys.stdin = StringIO("password")
        with patch('sys.stdin.isatty', return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

        out, _ = capsys.readouterr()
        result = json.loads(out.strip())
        jsonschema.validate(instance=result, schema=CLI_OUTPUT_SCHEMA)
        assert result["valid"] is False
        assert result["score"] <= 1

    def test_non_interactive_exit_code_matches_validity(self):
        # Valid password -> exit 0
        sys.stdin = StringIO("Str0ngP@ssw0rd!")
        with patch('sys.stdin.isatty', return_value=False):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0

        # Invalid password -> exit non‑zero
        sys.stdin = StringIO("weak")
        with patch('sys.stdin.isatty', return_value=False):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code != 0

    # ---------- Interactive mode ----------
    def test_interactive_valid_password(self, capsys, monkeypatch):
        inputs = iter(["Str0ngP@ssw0rd!", ".exit()"])
        # Mock getpass to print the prompt and return the next input
        def mock_getpass(prompt):
            print(prompt, end='')  # mimic real getpass output
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()  # Should not raise SystemExit

        out, _ = capsys.readouterr()
        #output: "✓ Strong against common attacks"
        assert "✓ Strong against common attacks" in out
        assert "Strength:" in out
        assert "Goodbye." in out

    def test_interactive_invalid_password(self, capsys, monkeypatch):
        inputs = iter(["short", ".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "✗ Does not meet policy requirements" in out
        assert any("min_length" in line.lower() or "at least" in line.lower() for line in out.splitlines())
        assert "Goodbye." in out

    def test_interactive_multiple_attempts(self, capsys, monkeypatch):
        inputs = iter(["short", "Str0ngP@ssw0rd!", ".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "✗ Does not meet policy requirements" in out   # first attempt
        assert "✓ Strong against common attacks" in out       # second attempt
        assert "Goodbye." in out

    def test_interactive_exit_command(self, capsys, monkeypatch):
        inputs = iter([".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "Goodbye." in out
        assert "Enter password:" in out   # prompt should be printed before exit

    def test_interactive_keyboard_interrupt(self, capsys, monkeypatch):
        def raise_keyboard_interrupt(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr('getpass.getpass', raise_keyboard_interrupt)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "Program interrupted by user." in out

    # ===== Edge Cases =====
    def test_interactive_empty_password(self, capsys, monkeypatch):
        inputs = iter(["", ".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "✗ Does not meet policy requirements" in out
        assert any("empty" in line.lower() for line in out.splitlines())
        assert "Goodbye." in out

    def test_interactive_long_password(self, capsys, monkeypatch):
        # Use a password that is both policy-compliant AND strong
        strong_pwd = "CorrectHorseBatteryStap13!"  # 26 chars, strong
        inputs = iter([strong_pwd, ".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "✓ Strong against common attacks" in out
        assert "Strength:" in out

    # ===== Real‑world usage =====
    def test_real_world_common_weak_password(self, capsys, monkeypatch):
        inputs = iter(["password123", ".exit()"])
        def mock_getpass(prompt):
            print(prompt, end='')
            return next(inputs)
        monkeypatch.setattr('getpass.getpass', mock_getpass)
        monkeypatch.setattr('sys.stdin.isatty', lambda: True)

        main()

        out, _ = capsys.readouterr()
        assert "✗ Does not meet policy requirements" in out
        assert any("uppercase" in line.lower() for line in out.splitlines())