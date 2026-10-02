import allure
import pytest

from constants import WRONG_CREDENTIALS_ERROR
from helpers import generate_user_data, remove_field


@allure.feature("Логин пользователя")
@allure.story("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, client, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        with allure.step("Отправляем запрос на авторизацию под созданным пользователем"):
            response = client.login(payload)

        with allure.step("Проверяем статус 200 и наличие токенов"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body
            assert "refreshToken" in body

    @allure.title("Вход с несуществующими (случайными) данными")
    def test_login_wrong_credentials(self, client):
        # Генерируем данные, которых точно нет в базе
        payload = generate_user_data()

        with allure.step("Отправляем запрос с заведомо несуществующими данными"):
            response = client.login(payload)

        with allure.step("Ожидаем 401 и сообщение о неверных email/пароле"):
            assert response.status_code == 401
            body = response.json()
            assert body["success"] is False
            assert WRONG_CREDENTIALS_ERROR in body["message"]

    @allure.title("Вход без обязательного поля: {missing_field}")
    @pytest.mark.parametrize(
    "missing_field, expected_error_msg",
    [
        ("email", WRONG_CREDENTIALS_ERROR),
        ("password", WRONG_CREDENTIALS_ERROR),
    ],
    ids=["no_email", "no_password"],
)
    def test_login_without_required_field(self, client, missing_field, expected_error_msg):
        payload = remove_field(generate_user_data(), missing_field)

        with allure.step(f"Отправляем запрос на логин без поля '{missing_field}'"):
            response = client.login(payload)

        with allure.step("Ожидаем ошибку 401 — отсутствие поля считается неавторизованным запросом"):
            # Для логина API отдаёт 401 даже при отсутствии полей
            assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code}"
            
            body = response.json()
            assert body["success"] is False
            # В ответе для 401 будет сообщение про неверный email/пароль, а не про отсутствие полей
            assert expected_error_msg in body["message"]