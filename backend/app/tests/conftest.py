import os
import pytest
from httpx import AsyncClient



os.environ.update({
    "KEYCLOAK_URL": "http://test",
    "KEYCLOAK_REALM": "test",
    "KEYCLOAK_CLIENT_ID": "test-client",
    "KEYCLOAK_CLIENT_SECRET": "test-secret",
    "KEYCLOAK_USERNAME": "admin",
    "KEYCLOAK_PASSWORD": "admin",
    "BASE_HOSTNAME": "http://localhost:3000",
})


from app.main import app
from app.core.rate_limiter import limiter




limiter.enabled = False


@pytest.fixture
async def async_client():
    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:
        yield client
