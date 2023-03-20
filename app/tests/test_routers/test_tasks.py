import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_read_user_tasks(client: TestClient, user_id: int = 1):
    response = client.get(f"/user/{user_id}/tasks/")
    assert response.status_code == 200


@pytest.mark.unit
def test_delete_user_task(client: TestClient, task_id: int = 1):
    response = client.delete(f"/user/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["task_title"] == "Clean room"
