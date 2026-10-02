import random

import requests
from faker import Faker

from constants import INGREDIENTS_URL

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


def get_ingredient_ids():
    """Запрашивает у API список всех ингредиентов и возвращает их ID."""
    response = requests.get(INGREDIENTS_URL)
    # response.raise_for_status()
    return [item["_id"] for item in response.json()["data"]]


def get_random_ingredient_ids(count=2):
    """Возвращает count случайных валидных ID ингредиентов."""
    return random.sample(get_ingredient_ids(), count)
