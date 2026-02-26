import requests
import pytest
import allure

from config import BASE_URL


@allure.feature("API: Создание заказа")
@allure.story("POST /api/orders")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, base_url, auth_headers, valid_ingredient_ids):
        with allure.step("POST /api/orders — заказ с авторизацией"):
            resp = requests.post(
                f"{base_url}/orders",
                headers=auth_headers,
                json={"ingredients": valid_ingredient_ids},
            )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data.get("success") is True
        assert "order" in data
        assert "number" in data["order"]

    @allure.title("Создание заказа с ингредиентами (проверка тела ответа)")
    def test_create_order_with_ingredients(self, base_url, auth_headers, valid_ingredient_ids):
        with allure.step("POST /api/orders — заказ с ингредиентами"):
            resp = requests.post(
                f"{base_url}/orders",
                headers=auth_headers,
                json={"ingredients": valid_ingredient_ids},
            )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data.get("success") is True
        assert "name" in data
        assert "order" in data and "number" in data["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, base_url, valid_ingredient_ids):
        with allure.step("POST /api/orders — без токена авторизации"):
            resp = requests.post(
                f"{base_url}/orders",
                json={"ingredients": valid_ingredient_ids},
            )
        assert resp.status_code in (200, 401, 403), resp.text
        if resp.status_code == 401:
            data = resp.json()
            assert data.get("success") is False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, base_url, auth_headers):
        with allure.step("POST /api/orders — пустой список ингредиентов"):
            resp = requests.post(
                f"{base_url}/orders",
                headers=auth_headers,
                json={"ingredients": []},
            )
        assert resp.status_code == 400, resp.text
        data = resp.json()
        assert data.get("success") is False
        assert "ingredient" in data.get("message", "").lower() or "provided" in data.get("message", "").lower()

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self, base_url, auth_headers):
        with allure.step("POST /api/orders — неверный хеш ингредиентов"):
            resp = requests.post(
                f"{base_url}/orders",
                headers=auth_headers,
                json={"ingredients": ["invalid_hash_12345"]},
            )
        assert resp.status_code == 500, resp.text
