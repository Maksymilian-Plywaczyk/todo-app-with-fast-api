import pytest
from fastapi.testclient import TestClient

# TODO make a pytest fixture with will return bearer token
#  for endpoints which need authorization


class TestLogin:
    @pytest.fixture
    def get_bearer_token(self, client: TestClient) -> str:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_login_body = {"username": "plywak12@gmail.com", "password": "haslo123"}
        response = client.post(
            url="api/v1/token/", data=request_login_body, headers=headers
        )
        response_data = response.json()
        assert response.status_code == 200
        token = response_data["access_token"]
        return token

    @pytest.mark.unit
    def test_login(self, client: TestClient) -> None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        request_login_body = {"username": "plywak12@gmail.com", "password": "haslo123"}
        response = client.post(
            url="api/v1/token/", data=request_login_body, headers=headers
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["token_type"] == "bearer"
        assert len(response_data["access_token"]) != 0

    @pytest.mark.unit
    def test_login_wrong_password(self, client: TestClient) -> None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        request_login_body = {"username": "plywak12@gmail.com", "password": "haslo1234"}
        response = client.post(
            url="api/v1/token/", data=request_login_body, headers=headers
        )
        response_data = response.json()
        assert response.status_code == 401
        assert response_data["detail"] == "Incorrect email or password"

    @pytest.mark.unit
    def test_incorrect_reset_password(self, client: TestClient, get_bearer_token: str):
        incorrect_bearer_token = get_bearer_token + "blablabla"
        request_body = {"token": incorrect_bearer_token, "new_password": "haslo1234"}
        response = client.post(url="api/v1/reset-password/", json=request_body)
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["detail"] == "Invalid token"

    @pytest.mark.unit
    def test_correct_reset_password(self, client: TestClient, get_bearer_token: str):
        request_body = {"token": get_bearer_token, "new_password": "haslo1234"}
        response = client.post(url="api/v1/reset-password/", json=request_body)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "Password updated successfully"
