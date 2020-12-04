from typing import Dict

from fastapi.testclient import TestClient

from config import settings


def get_user_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_USER_EMAIL,
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
