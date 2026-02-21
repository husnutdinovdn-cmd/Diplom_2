"""Фикстуры pytest для API тестов Stellar Burgers."""
import time
import requests
import pytest

from config import BASE_URL


@pytest.fixture
def base_url():
    """Базовый URL API."""
    return BASE_URL


@pytest.fixture
def valid_ingredient_ids(base_url):
    """Список валидных ID ингредиентов с сервера."""
    resp = requests.get(f"{base_url}/ingredients")
    resp.raise_for_status()
    data = resp.json()
    items = data if isinstance(data, list) else data.get("data", [])
    ids = [item["_id"] for item in items[:2]]
    assert len(ids) >= 2, "Нужно минимум 2 ингредиента для тестов"
    return ids


@pytest.fixture
def unique_user_data():
    """Уникальные данные пользователя (email с временной меткой)."""
    ts = int(time.time() * 1000)
    return {
        "email": f"user_{ts}@test.example.com",
        "password": "SecurePass123",
        "name": f"User_{ts}",
    }


@pytest.fixture
def registered_user(base_url, unique_user_data):
    """
    Создаёт пользователя, возвращает его данные и access_token.
    После теста пользователь остаётся в системе (для повторного входа).
    """
    resp = requests.post(f"{base_url}/auth/register", json=unique_user_data)
    resp.raise_for_status()
    body = resp.json()
    token = body.get("accessToken")
    assert token, "accessToken должен быть в ответе"
    yield {
        **unique_user_data,
        "access_token": token,
    }
    # Очистка не требуется по ТЗ; при необходимости можно вызвать logout


@pytest.fixture
def auth_headers(registered_user):
    """Заголовок Authorization для запросов с авторизацией."""
    token = registered_user["access_token"]
    return {"Authorization": token}
