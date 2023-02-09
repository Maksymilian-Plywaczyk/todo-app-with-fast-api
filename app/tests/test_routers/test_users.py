import pytest
from crud.users import create_new_user
from fastapi.testclient import TestClient
from pydantic import EmailStr
from schemas.users import UserCreate


# TODO add test using database
# @pytest.fixture(autouse=True)
# def users(db):
#     create_new_user(
#         db,
#         user=UserCreate(
#             full_name="Maks Pływak",
#             email=EmailStr("example@gmail.com"),
#             password="haslo123",
#         ),
#     )
#
@pytest.mark.unit
def test_create_user(client: TestClient):
    response = client.post(
        "/singup/",
        json={"full_name": "Maks", "email": "admin@op.pl", "password": "haslo"},
    )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.unit
def test_users(client: TestClient, skip: int = 0, limit: int = 2):
    response = client.get(f"/users?skip={skip}&limit={limit}")
    data = response.json()
    for person in data:
        assert person["full_name"] == "Maks"
    assert response.status_code == 200
