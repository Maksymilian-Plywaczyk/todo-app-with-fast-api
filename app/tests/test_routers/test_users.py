import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_users(client: TestClient, skip: int = 0, limit: int = 2):
    response = client.get(f"/users?skip={skip}&limit={limit}")
    assert response.status_code == 200
