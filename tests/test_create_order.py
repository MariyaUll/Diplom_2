import allure

from constants import EMPTY_INGREDIENTS_ERROR, INVALID_HASH


@allure.feature("Создание заказа")
@allure.story("Оформление заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, authorized_client, order_ingredients):
        payload = {"ingredients": order_ingredients}

        with allure.step("Отправляем запрос на создание заказа с токеном"):
            response = authorized_client.create_order(payload)

        with allure.step("Проверяем, что заказ успешно создан"):
            assert response.status_code == 200
            body = response.json()
            assert body.get("success") is True
            assert "order" in body
            assert "number" in body["order"]
            assert isinstance(body["order"]["number"], int)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, client, order_ingredients):
        payload = {"ingredients": order_ingredients}

        with allure.step("Отправляем запрос без токена"):
            response = client.create_order(payload)

        with allure.step("Проверяем, что заказ создан даже без авторизации"):
            assert response.status_code == 200
            body = response.json()
            assert body.get("success") is True
            assert "name" in body
            assert "order" in body
            assert "number" in body["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, client, order_ingredients):
        payload = {"ingredients": order_ingredients}

        with allure.step("Отправляем запрос с набором валидных ингредиентов"):
            response = client.create_order(payload)

        with allure.step("Проверяем успешный ответ и наличие номера заказа"):
            assert response.status_code == 200
            body = response.json()
            assert body.get("success") is True
            assert "name" in body
            assert "order" in body and "number" in body["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authorized_client):
        payload = {"ingredients": []}

        with allure.step("Отправляем запрос с пустым списком ингредиентов"):
            response = authorized_client.create_order(payload)

        with allure.step("Ожидаем ошибку 400 — ингредиенты обязательны"):
            assert response.status_code == 400
            body = response.json()
            assert body.get("success") is False
            assert EMPTY_INGREDIENTS_ERROR in body["message"]

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self, authorized_client):
        payload = {"ingredients": [INVALID_HASH]}

        with allure.step("Отправляем запрос с некорректным ID ингредиента"):
            response = authorized_client.create_order(payload)

        with allure.step("Ожидаем ошибку сервера 500"):
            assert response.status_code == 500
