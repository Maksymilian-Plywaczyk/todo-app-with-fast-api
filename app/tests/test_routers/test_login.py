import os

import dotenv
import pytest
from fastapi.testclient import TestClient

dotenv.load_dotenv(dotenv.find_dotenv())


# TODO add tests using database
@pytest.mark.unit
def test_login(client: TestClient) -> None:
    # headers = {"Content-Type": "x-www-form-urlencoded"}

    request_login_body = {
        "username": os.getenv("ADMIN_USERNAME"),
        "password": os.getenv("ADMIN_PASSWORD"),
    }
    response = client.post("/login/", data=request_login_body)
    assert response.status_code == 200
