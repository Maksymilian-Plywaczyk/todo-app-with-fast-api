import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestUser:
    @pytest.fixture
    def get_user_bearer_token(self, client: TestClient):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_login_body = {"username": "admin@op.pl", "password": "haslo"}
        response = client.post(
            url="api/v1/token/", data=request_login_body, headers=headers
        )
        response_data = response.json()
        assert response.status_code == 200
        token = response_data["access_token"]
        return token

    @pytest.mark.unit
    def test_create_user(self, client: TestClient):
        response = client.post(
            "api/v1/signup/",
            json={
                "full_name": "Maks",
                "email": "admin@op.pl",
                "password": "haslo",
                "is_active": True,
            },
        )
        data = response.json()
        assert data["full_name"] == "Maks"
        assert data["email"] == "admin@op.pl"
        assert data["is_active"] is True
        assert response.status_code == 200

    @pytest.mark.unit
    def test_get_me(self, client: TestClient, get_user_bearer_token: str):
        response = client.get(
            "api/v1/users/me",
            headers={"Authorization": f"Bearer {get_user_bearer_token}"},
        )
        data = response.json()
        assert data["full_name"] == "Maks"
        assert data["email"] == "admin@op.pl"
        assert response.status_code == 200

    @pytest.mark.unit
    def test_unauthorized_me(self, client: TestClient):
        response = client.get("api/v1/users/me")
        data = response.json()
        assert data["detail"] == "Not authenticated"
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.unit
    def test_incorrect_token_get_me(self, client, get_user_bearer_token):
        response = client.get(
            "api/v1/users/me",
            headers={"Authorization": f"Bearer {get_user_bearer_token}+1"},
        )
        data = response.json()
        assert data["detail"] == "Could not validate credentials"
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.unit
    def test_get_users(self, client: TestClient, skip: int = 0, limit: int = 2):
        response = client.get(f"api/v1/users?skip={skip}&limit={limit}")
        data = response.json()
        for person in data:
            if person["full_name"] == "Maks Pływaczyk":
                assert person["full_name"] == "Maks Pływaczyk"
                assert person["email"] == "plywak12@gmail.com"
            if person["full_name"] == "Maks":
                assert person["full_name"] == "Maks"
                assert person["email"] == "admin@op.pl"

        assert response.status_code == 200

    @pytest.mark.unit
    def test_delete_user(self, client: TestClient, user_id: int = 1):
        response = client.delete(f'api/v1/users/delete_user/{user_id}')
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "User deleted successfully"
