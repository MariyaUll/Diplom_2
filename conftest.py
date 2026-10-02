import pytest
from api_client import ApiClient
from helpers import generate_user_data, get_random_ingredient_ids


@pytest.fixture
def client():
    """Базовый клиент без авторизации."""
    return ApiClient()


@pytest.fixture
def registered_user(client):
    """Создаёт уникального пользователя, а после теста удаляет его."""
    user_data = generate_user_data()
    response = client.register(user_data)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    body = response.json()
    user_data["access_token"] = body["accessToken"]

    yield user_data

    # Очистка: удаляем пользователя после теста
    client.delete_user(user_data["access_token"])


@pytest.fixture
def authorized_client(client, registered_user):
    """Клиент с токеном созданного пользователя — для тестов, где нужна авторизация."""
    client.set_token(registered_user["access_token"])
    return client


@pytest.fixture
def order_ingredients():
    """Случайный набор валидных ID ингредиентов."""
    return get_random_ingredient_ids(count=3)
