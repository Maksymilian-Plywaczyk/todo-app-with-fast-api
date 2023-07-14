import pytest
from fastapi.testclient import TestClient


# TODO add tests using database
@pytest.mark.unit
def test_login(client: TestClient) -> None:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    request_login_body = {"username": "plywak12@gmail.com", "password": "haslo123"}
    response = client.post("api/v1/token/", data=request_login_body, headers=headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["token_type"] == "bearer"
    assert len(response_data["access_token"]) != 0
