import requests
import allure

from constants import REGISTER_URL, LOGIN_URL, USER_URL, ORDERS_URL, INGREDIENTS_URL


class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("POST /api/auth/register")
    def register(self, payload):
        return self.session.post(REGISTER_URL, json=payload)

    @allure.step("POST /api/auth/login")
    def login(self, payload):
        return self.session.post(LOGIN_URL, json=payload)

    @allure.step("DELETE /api/auth/user")
    def delete_user(self, token):
        return self.session.delete(USER_URL, headers={"Authorization": token})

    @allure.step("GET /api/ingredients")
    def get_ingredients(self):
        return self.session.get(INGREDIENTS_URL)

    @allure.step("POST /api/orders")
    def create_order(self, payload):
        return self.session.post(ORDERS_URL, json=payload)

    def set_token(self, token):
        # accessToken из ответа API уже содержит "Bearer ..."
        # поэтому добавлять префикс повторно не нужно
        self.session.headers.update({"Authorization": token})
