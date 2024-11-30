import pytest
from httpx import AsyncClient
from uuid import UUID
from app.main import app
from app.models.token import PlatformEnum

pytestmark = pytest.mark.asyncio

async def test_create_token(client):
    """Test creating a new token."""
    response = await client.post(
        "/api/v1/tokens",
        json={
            "user_id": "test_user",
            "token": "test_fcm_token",
            "platform": "fcm"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["token"] == "test_fcm_token"
    assert data["platform"] == "fcm"
    assert UUID(data["id"])  # Verify it's a valid UUID

async def test_create_duplicate_token(client):
    """Test creating a duplicate token returns the existing one."""
    # Create first token
    response1 = await client.post(
        "/api/v1/tokens",
        json={
            "user_id": "test_user",
            "token": "test_fcm_token",
            "platform": "fcm"
        }
    )
    assert response1.status_code == 200
    data1 = response1.json()

    # Try to create duplicate token
    response2 = await client.post(
        "/api/v1/tokens",
        json={
            "user_id": "test_user",
            "token": "test_fcm_token",
            "platform": "fcm"
        }
    )
    assert response2.status_code == 200
    data2 = response2.json()

    # Verify both responses have the same ID
    assert data1["id"] == data2["id"]

async def test_get_user_tokens(client):
    """Test retrieving user tokens."""
    # Create two tokens for the same user
    tokens = [
        {
            "user_id": "test_user",
            "token": "test_fcm_token1",
            "platform": "fcm"
        },
        {
            "user_id": "test_user",
            "token": "test_apns_token1",
            "platform": "apns"
        }
    ]

    for token in tokens:
        response = await client.post("/api/v1/tokens", json=token)
        assert response.status_code == 200

    # Get user tokens
    response = await client.get("/api/v1/tokens/test_user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {token["token"] for token in data} == {"test_fcm_token1", "test_apns_token1"}

async def test_delete_token(client):
    """Test deleting a token."""
    # Create a token
    response = await client.post(
        "/api/v1/tokens",
        json={
            "user_id": "test_user",
            "token": "test_token_delete",
            "platform": "fcm"
        }
    )
    assert response.status_code == 200
    token_id = response.json()["id"]

    # Delete the token
    response = await client.delete(f"/api/v1/tokens/{token_id}")
    assert response.status_code == 200

    # Verify token is deleted
    response = await client.get("/api/v1/tokens/test_user")
    assert response.status_code == 200
    data = response.json()
    assert not any(token["id"] == token_id for token in data)

async def test_delete_nonexistent_token(client):
    """Test deleting a non-existent token."""
    response = await client.delete(f"/api/v1/tokens/{UUID(int=0)}")
    assert response.status_code == 404

async def test_invalid_platform(client):
    """Test creating a token with invalid platform."""
    response = await client.post(
        "/api/v1/tokens",
        json={
            "user_id": "test_user",
            "token": "test_token",
            "platform": "invalid_platform"
        }
    )
    assert response.status_code == 422  # Validation error