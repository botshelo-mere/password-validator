import pytest
from fortifypass import PasswordValidator


@pytest.fixture
def validator():
    """Provide a default validator instance for benchmarks."""
    return PasswordValidator()


# ===== Benchmark: validate() =====
def test_benchmark_validate_valid(validator, benchmark):
    """Benchmark validate() with a valid password."""
    pwd = "Str0ngP@ssw0rd!"
    benchmark(validator.validate, pwd)


def test_benchmark_validate_invalid(validator, benchmark):
    """Benchmark validate() with an invalid password (fails multiple rules)."""
    pwd = "weak"
    benchmark(validator.validate, pwd)


# ===== Benchmark: estimate_strength() =====
def test_benchmark_estimate_strength_weak(validator, benchmark):
    """Benchmark estimate_strength() with a weak password."""
    pwd = "password"
    benchmark(validator.estimate_strength, pwd)


def test_benchmark_estimate_strength_strong(validator, benchmark):
    """Benchmark estimate_strength() with a strong passphrase."""
    pwd = "CorrectHorseBatteryStaple!"
    benchmark(validator.estimate_strength, pwd)


def test_benchmark_estimate_strength_long(validator, benchmark):
    """
    Benchmark estimate_strength() with a very long password.
    This stresses the zxcvbn truncation logic.
    """
    pwd = "A" * 100 + "1!"   # 102 chars, truncated to 72
    benchmark(validator.estimate_strength, pwd)


# ===== Benchmark: evaluate() (combines validation + strength) =====
def test_benchmark_evaluate_valid(validator, benchmark):
    """Benchmark evaluate() with a valid password."""
    pwd = "Str0ngP@ssw0rd!"
    benchmark(validator.evaluate, pwd)


def test_benchmark_evaluate_invalid(validator, benchmark):
    """Benchmark evaluate() with an invalid password."""
    pwd = "weak"
    benchmark(validator.evaluate, pwd)


# ====== Optional: parametrized benchmark for multiple password types =====
@pytest.mark.parametrize(
    "pwd,description",
    [
        ("password", "common weak"),
        ("123456", "numeric only"),
        ("CorrectHorseBatteryStaple!", "strong passphrase"),
        ("Str0ngP@ssw0rd!", "complex valid"),
        ("A" * 100 + "1!", "very long"),
    ]
)
def test_benchmark_evaluate_param(validator, benchmark, pwd, description):
    """Benchmark evaluate() with different password types."""
    # Use a lambda to pass the password to benchmark
    benchmark(validator.evaluate, pwd)