import requests
import pytest
import allure

from config import BASE_URL


@allure.feature("API: Логин пользователя")
@allure.story("POST /api/auth/login")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, base_url, registered_user):
        email = registered_user["email"]
        password = registered_user["password"]
        with allure.step("POST /api/auth/login — вход под существующим пользователем"):
            resp = requests.post(
                f"{base_url}/auth/login",
                json={"email": email, "password": password},
            )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data.get("success") is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data.get("user", {}).get("email") == email

    @allure.title("Вход с неверным логином и паролем")
    def test_login_wrong_credentials(self, base_url):
        with allure.step("POST /api/auth/login — неверные учётные данные"):
            resp = requests.post(
                f"{base_url}/auth/login",
                json={"email": "wrong@test.com", "password": "wrongpassword"},
            )
        assert resp.status_code == 401, resp.text
        data = resp.json()
        assert data.get("success") is False
        assert "incorrect" in data.get("message", "").lower() or "email" in data.get("message", "").lower()
