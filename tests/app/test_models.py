"""Module defining tests for URL model string representations."""

from app.models import Url


def test_url_str() -> None:
    """Test string representation of Url model."""
    url = Url(key="abc123", target_url="https://example.com", is_active=True, clicks=0)
    expected = "URL: https://example.com (Key: abc123, Active: True)"
    assert str(url) == expected


def test_url_repr() -> None:
    """Test repr representation of Url model."""
    url = Url(key="abc123", target_url="https://example.com", is_active=True, clicks=0)
    expected = (
        "<Url(key=abc123, target_url=https://example.com, is_active=True, clicks=0)>"
    )
    assert repr(url) == expected
