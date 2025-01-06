"""Module defining unit tests for utility functions."""

import string

import pytest

from app.utils import generate_random_key


def test_generate_random_key_length() -> None:
    """Verify generated key has correct length."""
    assert len(generate_random_key(10)) == 10


def test_generate_random_key_characters() -> None:
    """Verify key contains only valid characters."""
    key = generate_random_key(20)
    valid_chars = set(string.ascii_letters + string.digits)
    assert all(c in valid_chars for c in key)


def test_generate_random_key_randomness() -> None:
    """Verify different calls generate different keys."""
    assert generate_random_key(10) != generate_random_key(10)


def test_generate_random_key_invalid_length() -> None:
    """Verify function raises error for invalid length."""
    with pytest.raises(AssertionError):
        generate_random_key(0)


def test_generate_random_key_invalid_type() -> None:
    """Verify function raises error for invalid type."""
    with pytest.raises(AssertionError):
        generate_random_key("10")  # type: ignore
