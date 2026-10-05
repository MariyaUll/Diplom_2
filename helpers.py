import random
import allure
from faker import Faker

fake = Faker("ru_RU")


def generate_user_data():
    """Генерирует уникальные данные пользователя."""
    return {
        "email": fake.email(),
        "password": fake.password(length=8),
        "name": fake.name(),
    }


def remove_field(payload, field):
    """Возвращает копию payload без указанного поля."""
    data = dict(payload)
    data.pop(field, None)
    return data


@allure.step("Получаем {count} случайных валидных ID ингредиентов через API-клиент")
def get_random_ingredient_ids(client, count=2):
    response = client.get_ingredients()
    ids = [item["_id"] for item in response.json()["data"]]
    if count > len(ids):
        raise ValueError(f"Запрошено {count} ингредиентов, но доступно только {len(ids)}")
    return random.sample(ids, count)
