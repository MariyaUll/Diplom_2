import allure
import pytest

from constants import USER_EXISTS_ERROR, MISSING_FIELDS_ERROR, REQUIRED_FIELDS
from helpers import generate_user_data, remove_field


@allure.feature("Создание пользователя")
@allure.story("Регистрация пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, client):
        with allure.step("Генерируем уникальные тестовые данные"):
            payload = generate_user_data()

        with allure.step("Отправляем запрос на регистрацию"):
            response = client.register(payload)

        with allure.step("Проверяем статус ответа и наличие токенов"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user(self, client, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        }

        with allure.step("Отправляем запрос с данными уже существующего пользователя"):
            response = client.register(payload)

        with allure.step("Ожидаем ошибку 403 и сообщение о существующем пользователе"):
            assert response.status_code == 403
            body = response.json()
            assert body["success"] is False
            assert USER_EXISTS_ERROR in body["message"]

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", REQUIRED_FIELDS)
    def test_create_user_without_required_field(self, client, missing_field):
        payload = remove_field(generate_user_data(), missing_field)

        with allure.step(f"Отправляем запрос без поля '{missing_field}'"):
            response = client.register(payload)

        with allure.step("Ожидаем ошибку 403 и сообщение об обязательных полях"):
            assert response.status_code == 403
            body = response.json()
            assert body["success"] is False
            assert MISSING_FIELDS_ERROR in body["message"]
