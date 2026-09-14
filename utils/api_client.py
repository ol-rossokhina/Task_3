from typing import List, Optional

import allure
import requests

from config import LOGIN_API_URL, REGISTER_API_URL, USER_API_URL, API_BASE_URL

INGREDIENTS_API_URL = f'{API_BASE_URL}/ingredients'
ORDERS_API_URL = f'{API_BASE_URL}/orders'


def _auth_headers(access_token: Optional[str]) -> dict:
    return {'Authorization': access_token} if access_token else {}


def register_user(user_data: dict) -> requests.Response:
    email = user_data.get('email', '<без email>')
    with allure.step(f'API: зарегистрировать пользователя {email}'):
        return requests.post(REGISTER_API_URL, json=user_data)


def login_user(credentials: dict) -> requests.Response:
    email = credentials.get('email', '<без email>')
    with allure.step(f'API: авторизоваться под пользователем {email}'):
        return requests.post(LOGIN_API_URL, json=credentials)


@allure.step('API: удалить пользователя')
def delete_user(access_token: Optional[str]) -> requests.Response:
    return requests.delete(USER_API_URL, headers=_auth_headers(access_token))


@allure.step('API: получить список доступных ингредиентов')
def get_ingredients() -> requests.Response:
    return requests.get(INGREDIENTS_API_URL)


@allure.step('API: создать заказ с ингредиентами {ingredient_ids}')
def create_order(ingredient_ids: List[str], access_token: str) -> requests.Response:
    return requests.post(
        ORDERS_API_URL,
        json={'ingredients': ingredient_ids},
        headers=_auth_headers(access_token),
    )
