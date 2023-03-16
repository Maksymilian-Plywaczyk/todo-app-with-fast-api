import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_create_user(client: TestClient):
    response = client.post(
        "/singup/",
        json={"full_name": "Maks", "email": "admin@op.pl", "password": "haslo"},
    )
    data = response.json()
    assert data["full_name"] == "Maks"
    assert data["email"] == "admin@op.pl"
    assert response.status_code == 200


@pytest.mark.unit
def test_users(client: TestClient, skip: int = 0, limit: int = 2):
    response = client.get(f"/users?skip={skip}&limit={limit}")
    data = response.json()
    for person in data:
        assert person["full_name"] == "Maks"
    assert response.status_code == 200
