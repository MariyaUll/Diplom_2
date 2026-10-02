"""URL-адреса сервиса Stellar Burgers и его эндпоинтов."""

BASE_URL = "https://stellarburgers.education-services.ru"

REGISTER_URL = f"{BASE_URL}/api/auth/register"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
ORDERS_URL = f"{BASE_URL}/api/orders"
USER_URL = f"{BASE_URL}/api/auth/user"
INGREDIENTS_URL = f"{BASE_URL}/api/ingredients"


"""Предопределённые тестовые данные и сообщения API."""

# Сообщения об ошибках API (для проверок в тестах)
USER_EXISTS_ERROR = "User already exists"
MISSING_FIELDS_ERROR = "Email, password and name are required fields"
WRONG_CREDENTIALS_ERROR = "email or password are incorrect"
EMPTY_INGREDIENTS_ERROR = "Ingredient ids must be provided"

# Поля, без которых регистрация невозможна
REQUIRED_FIELDS = ["email", "password", "name"]

# Неверный хеш ингредиента
INVALID_HASH = "invalidhash123456"
