import pytest
from fastapi.testclient import TestClient

from app.crud.users import create_new_user
from app.schemas.users import UserCreate


class TestLogin:
    # TODO fix error with inactive user
    @pytest.fixture(scope="session", autouse=True)
    def new_inactive_user(self, db_session):
        create_new_user(
            db=db_session,
            user=UserCreate(
                full_name="In active user type",
                email="inactive@gmail.com",
                password="inactive",
                is_active=False,
            ),
        )

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

    @pytest.fixture
    def get_inactive_bearer_token(self, client: TestClient) -> str:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_login_body = {"username": "inactive@gmail.com", "password": "inactive"}
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
    def test_incorrect_reset_password_inactive_user(
        self, client, get_inactive_bearer_token: str
    ):
        request_body = {"token": get_inactive_bearer_token, "new_password": "haslo1234"}
        response = client.post(url="api/v1/reset-password/", json=request_body)
        response_data = response.json()
        assert response.status_code == 400
        assert response_data["detail"] == "User is not active."

    @pytest.mark.unit
    def test_correct_reset_password(self, client: TestClient, get_bearer_token: str):
        request_body = {"token": get_bearer_token, "new_password": "haslo1234"}
        response = client.post(url="api/v1/reset-password/", json=request_body)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "Password updated successfully"
