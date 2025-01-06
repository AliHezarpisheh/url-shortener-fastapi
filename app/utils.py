"""Module defining application utilities."""

import random
import string


def generate_random_key(length: int) -> str:
    """Generate a random string of specified length using letters and digits."""
    assert isinstance(length, int) and length >= 1, "Length must be a positive integer"

    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
