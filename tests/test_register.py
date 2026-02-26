import time
import requests
import pytest
import allure

from config import BASE_URL


@allure.feature("API: Создание пользователя")
@allure.story("POST /api/auth/register")
class TestCreateUser:

    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self, base_url, unique_user_data):
        with allure.step("POST /api/auth/register — создание уникального пользователя"):
            resp = requests.post(f"{base_url}/auth/register", json=unique_user_data)
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data.get("success") is True
        assert "user" in data
        assert data["user"].get("email") == unique_user_data["email"]
        assert data["user"].get("name") == unique_user_data["name"]
        assert "accessToken" in data
        assert "refreshToken" in data

    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_user_already_registered(self, base_url, unique_user_data):
        with allure.step("POST /api/auth/register — первая регистрация"):
            requests.post(f"{base_url}/auth/register", json=unique_user_data)
        with allure.step("POST /api/auth/register — повторная регистрация того же пользователя"):
            resp = requests.post(f"{base_url}/auth/register", json=unique_user_data)
        assert resp.status_code == 403, resp.text
        data = resp.json()
        assert data.get("success") is False
        assert "already exists" in data.get("message", "").lower()

    @allure.title("Создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("omit_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, base_url, omit_field):
        ts = int(time.time() * 1000)
        payload = {
            "email": f"user_{ts}@test.example.com",
            "password": "SecurePass123",
            "name": f"User_{ts}",
        }
        del payload[omit_field]
        with allure.step("POST /api/auth/register — без обязательного поля"):
            resp = requests.post(f"{base_url}/auth/register", json=payload)
        assert resp.status_code == 403, resp.text
        data = resp.json()
        assert data.get("success") is False
        assert "required" in data.get("message", "").lower() or "fields" in data.get("message", "").lower()
