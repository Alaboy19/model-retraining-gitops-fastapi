import pytest
from fastapi.testclient import TestClient

from app_model import app


@pytest.fixture
def client():
    return TestClient(app)


def test_predict(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
