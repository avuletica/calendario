from fastapi.testclient import TestClient

from config import settings
from tests.utils.utils import random_email, random_lower_string


def test_registration(client: TestClient) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/registration",
        json=data,
    )
    assert r.status_code == 200


def test_registration_conflict(client: TestClient) -> None:
    data = {
        "email": settings.FIRST_USER_EMAIL,
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/registration",
        json=data,
    )
    assert r.status_code == 409
