import uuid


def generate_user_data() -> dict:
    """Генерирует уникальные данные пользователя для регистрации через API."""
    unique_id = uuid.uuid4().hex[:12]

    return {
        'email': f'stellar-ui-test-{unique_id}@yandex.ru',
        'password': f'Pass-{unique_id}',
        'name': f'UiTestUser{unique_id}',
    }
