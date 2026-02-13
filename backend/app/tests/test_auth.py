from unittest.mock import AsyncMock

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Response

from app.main import app
from app.core.config import kcsettings
from app.routers.v1 import auth

@pytest.fixture
def client():
    """
    Creates a fresh TestClient for every test.
    Prevents state leaking between tests.
    VERY important when running pytest-xdist.
    """
    return TestClient(app)


@respx.mock
def test_login_success(client):

    respx.post(kcsettings.KEYCLOAK_TOKEN_URL).mock(
        return_value=Response(
            200,
            json={
                "access_token": "token",
                "expires_in": 3600,
                "refresh_token": "refresh",
                "refresh_expires_in": 7200,
                "token_type": "Bearer",
            },
        )
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "user@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token"


@respx.mock
def test_login_invalid_credentials(client):

    respx.post(kcsettings.KEYCLOAK_TOKEN_URL).mock(
        return_value=Response(401, json={"error": "invalid_grant"})
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "user@example.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid credentials"}



@respx.mock
def test_signup_success(client, monkeypatch):

    monkeypatch.setattr(
        auth.kc_admin,
        "get_admin_token",
        AsyncMock(return_value="admin-token"),
    )

    trigger_email = AsyncMock()
    monkeypatch.setattr(auth.kc_admin, "trigger_email_action", trigger_email)

    respx.post(kcsettings.KEYCLOAK_USERS_URL()).mock(
        return_value=Response(
            201,
            headers={
                "Location": f"{kcsettings.KEYCLOAK_USERS_URL()}/new-user-id"
            },
        )
    )

    response = client.post(
        "/v1/auth/signup",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "secret",
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == "new-user-id"

    trigger_email.assert_awaited_once()


@respx.mock
def test_signup_user_creation_failure(client, monkeypatch):

    monkeypatch.setattr(
        auth.kc_admin,
        "get_admin_token",
        AsyncMock(return_value="admin-token"),
    )

    respx.post(kcsettings.KEYCLOAK_USERS_URL()).mock(
        return_value=Response(400)
    )

    response = client.post(
        "/v1/auth/signup",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "secret",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"message": "Failed to create the user"}



@respx.mock
def test_refresh_success(client):

    respx.post(kcsettings.KEYCLOAK_TOKEN_URL).mock(
        return_value=Response(
            200,
            json={"access_token": "new-token"},
        )
    )

    response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": "refresh"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "new-token"


@respx.mock
def test_refresh_invalid_token(client):

    respx.post(kcsettings.KEYCLOAK_TOKEN_URL).mock(
        return_value=Response(400)
    )

    response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": "bad"},
    )

    assert response.status_code == 401

@respx.mock
def test_logout_success(client):

    respx.post(kcsettings.KEYCLOAK_LOGOUT_URL).mock(
        return_value=Response(204)
    )

    response = client.post(
        "/v1/auth/logout",
        json={"refresh_token": "refresh"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}


@respx.mock
def test_logout_failure(client):

    respx.post(kcsettings.KEYCLOAK_LOGOUT_URL).mock(
        return_value=Response(400)
    )

    response = client.post(
        "/v1/auth/logout",
        json={"refresh_token": "refresh"},
    )

    assert response.status_code == 400



def test_password_reset_user_not_found(client, monkeypatch):

    monkeypatch.setattr(
        auth.kc_admin,
        "get_admin_token",
        AsyncMock(return_value="admin-token"),
    )

    monkeypatch.setattr(
        auth.kc_admin,
        "get_user_id_by_email",
        AsyncMock(return_value=None),
    )

    response = client.post(
        "/v1/auth/password-reset/request",
        json={"email": "missing@example.com"},
    )

    assert response.status_code == 404


def test_password_reset_success(client, monkeypatch):

    monkeypatch.setattr(
        auth.kc_admin,
        "get_admin_token",
        AsyncMock(return_value="admin-token"),
    )

    monkeypatch.setattr(
        auth.kc_admin,
        "get_user_id_by_email",
        AsyncMock(return_value="user-123"),
    )

    trigger_email = AsyncMock()
    monkeypatch.setattr(auth.kc_admin, "trigger_email_action", trigger_email)

    response = client.post(
        "/v1/auth/password-reset/request",
        json={"email": "user@example.com"},
    )

    assert response.status_code == 200
    trigger_email.assert_awaited_once()
