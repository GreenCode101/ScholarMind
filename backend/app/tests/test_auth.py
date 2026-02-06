from fastapi.testclient import TestClient

from app.main import app
from app.routers.v1 import auth


client = TestClient(app)


class DummyResponse:
    def __init__(self, status_code: int, payload=None, headers=None, text: str = ""):
        self.status_code = status_code
        self._payload = payload or {}
        self.headers = headers or {}
        self.text = text

    def json(self):
        return self._payload


class DummyAsyncClient:
    def __init__(self, responses):
        self._responses = responses
        self._post_index = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        response = self._responses[self._post_index]
        self._post_index += 1
        return response

    async def put(self, *args, **kwargs):
        return DummyResponse(status_code=204)


def test_login_success(monkeypatch):
    token_response = DummyResponse(
        status_code=200,
        payload={
            "access_token": "access-token",
            "expires_in": 3600,
            "refresh_token": "refresh-token",
            "refresh_expires_in": 7200,
            "token_type": "Bearer",
        },
    )

    monkeypatch.setattr(
        auth.httpx,
        "AsyncClient",
        lambda: DummyAsyncClient([token_response]),
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "access-token"


def test_login_invalid_credentials(monkeypatch):
    failed_token_response = DummyResponse(status_code=401, text="Unauthorized")

    monkeypatch.setattr(
        auth.httpx,
        "AsyncClient",
        lambda: DummyAsyncClient([failed_token_response]),
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid credentials"}


def test_signup_success(monkeypatch):
    create_user_response = DummyResponse(
        status_code=201,
        headers={
            "Location": "http://keycloak.local/admin/realms/test/users/new-user-id",
        },
    )

    monkeypatch.setattr(auth, "get_admin_token", lambda: "fake-admin-token")
    monkeypatch.setattr(
        auth.httpx,
        "AsyncClient",
        lambda: DummyAsyncClient([create_user_response]),
    )

    response = client.post(
        "/v1/auth/signup",
        json={
            "email": "new.user@example.com",
            "username": "new-user",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "User created successfully. Verification email sent.",
        "user_id": "new-user-id",
    }


def test_signup_create_user_failure(monkeypatch):
    failed_create_user_response = DummyResponse(status_code=400, text="Bad Request")

    monkeypatch.setattr(auth, "get_admin_token", lambda: "fake-admin-token")
    monkeypatch.setattr(
        auth.httpx,
        "AsyncClient",
        lambda: DummyAsyncClient([failed_create_user_response]),
    )

    response = client.post(
        "/v1/auth/signup",
        json={
            "email": "new.user@example.com",
            "username": "new-user",
            "password": "password123",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"message": "Failed to create the user"}
