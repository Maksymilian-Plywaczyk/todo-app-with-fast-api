import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_singup(client: TestClient):
    headers = {"Content-Type": "application/json"}
    url = "api/v1/signup/"
    request_singup_body = {
        "full_name": "User example",
        "email": "user@example.com",
        "is_active": True,
        "password": "admin123",
    }
    response = client.post(url, json=request_singup_body, headers=headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["full_name"] == "User example"
    assert response_data["email"] == "user@example.com"
