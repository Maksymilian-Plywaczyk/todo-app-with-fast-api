import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_create_user(client: TestClient):
    response = client.post(
        "/signup/",
        json={"full_name": "Maks", "email": "admin@op.pl", "password": "haslo"},
    )
    data = response.json()
    assert data["full_name"] == "Maks"
    assert data["email"] == "admin@op.pl"
    assert response.status_code == 200


@pytest.mark.unit
def test_get_users(client: TestClient, skip: int = 0, limit: int = 2):
    response = client.get(f"/users?skip={skip}&limit={limit}")
    data = response.json()
    for person in data:
        assert person["full_name"] == "Maks"
    assert response.status_code == 200


@pytest.mark.unit
def test_create_new_user_task(client: TestClient, user_id: int = 1):
    response = client.post(
        f"/users/{user_id}/task",
        json={
            "task_title": "Clean room",
            "task_description": "Tomorrow clean whole bedroom",
            "task_piority": 1,
            "create_at": "2023-03-19",
            "is_completed": False,
            "finished_at": "2023-03-19",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task created successfully"


@pytest.mark.unit
def test_delete_user(client: TestClient, user_id: int = 1):
    response = client.delete(f'/delete_user/{user_id}')
    assert response.status_code == 200
