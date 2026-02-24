import time
import requests
import pytest
import allure

from config import BASE_URL


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def valid_ingredient_ids(base_url):
    with allure.step("GET /api/ingredients — получить валидные ID ингредиентов"):
        resp = requests.get(f"{base_url}/ingredients")
        resp.raise_for_status()
        data = resp.json()
        items = data if isinstance(data, list) else data.get("data", [])
        ids = [item["_id"] for item in items[:2]]
        assert len(ids) >= 2, "Нужно минимум 2 ингредиента для тестов"
        return ids


@pytest.fixture
def unique_user_data():
    ts = int(time.time() * 1000)
    return {
        "email": f"user_{ts}@test.example.com",
        "password": "SecurePass123",
        "name": f"User_{ts}",
    }


@pytest.fixture
def registered_user(base_url, unique_user_data):
    with allure.step("POST /api/auth/register — регистрация пользователя для фикстуры"):
        resp = requests.post(f"{base_url}/auth/register", json=unique_user_data)
        resp.raise_for_status()
        body = resp.json()
        token = body.get("accessToken")
        assert token, "accessToken должен быть в ответе"
        yield {
            **unique_user_data,
            "access_token": token,
        }


@pytest.fixture
def auth_headers(registered_user):
    token = registered_user["access_token"]
    return {"Authorization": token}
