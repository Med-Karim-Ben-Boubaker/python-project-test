import pytest
from fastapi.testclient import TestClient
from ..main import app

@pytest.fixture(scope="module")
def test_client():
    # Test client is used to simulate HTTP requests to the FastAPI application
    with TestClient(app) as client:
        yield client
