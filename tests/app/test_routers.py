"""Module defining tests for URL shortener API endpoints."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient) -> None:
    """Test successful creation of shortened URL."""
    response = await client.post("/url", json={"target_url": "https://example.com"})
    assert response.status_code == status.HTTP_201_CREATED
    assert "key" in response.json()


@pytest.mark.asyncio
async def test_create_duplicate_url(client: AsyncClient) -> None:
    """Test handling of duplicate URL creation."""
    url = "https://example.com"
    await client.post("/url", json={"target_url": url})
    response = await client.post("/url", json={"target_url": url})
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_forward_to_target_url(client: AsyncClient) -> None:
    """Test successful URL redirection."""
    create_response = await client.post(
        "/url", json={"target_url": "https://example.com"}
    )
    key = create_response.json()["key"]
    response = await client.get(f"/{key}", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://example.com"


@pytest.mark.asyncio
async def test_forward_to_nonexistent_url(client: AsyncClient) -> None:
    """Test handling of nonexistent URL key."""
    response = await client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_deactivate_url(client: AsyncClient) -> None:
    """Test successful URL deactivation."""
    create_response = await client.post(
        "/url", json={"target_url": "https://example.com"}
    )
    key = create_response.json()["key"]
    response = await client.delete(f"/{key}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_deactivate_nonexistent_url(client: AsyncClient) -> None:
    """Test handling of nonexistent URL deactivation."""
    response = await client.delete("/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
