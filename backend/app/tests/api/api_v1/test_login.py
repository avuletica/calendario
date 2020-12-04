from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import crud
from config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_USER_EMAIL,
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
