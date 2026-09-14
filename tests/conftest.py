import pytest

from config import MAIN_URL
from pages.login_page import LoginPage
from utils.api_client import create_order, delete_user, get_ingredients, register_user
from utils.data_generator import generate_user_data


@pytest.fixture
def registered_user():
    """
    Регистрирует нового пользователя через API перед тестом и гарантированно
    удаляет его после теста (в т.ч. если тест упал), независимо от исхода.
    Возвращает кортеж (исходные данные пользователя, тело ответа регистрации).
    """
    user_data = generate_user_data()
    response = register_user(user_data)
    response_data = response.json()

    yield user_data, response_data

    access_token = response_data.get('accessToken')
    if access_token:
        delete_user(access_token)


@pytest.fixture
def logged_in_driver(driver, registered_user):
    """
    Логинит пользователя через настоящую форму входа в браузере.
    Сам пользователь создаётся через API (быстро, не зависит от UI),
    а вход выполняется через UI, чтобы заодно проверялось реальное
    поведение формы логина.
    """
    user_data, _ = registered_user

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(user_data['email'], user_data['password'])
    login_page.wait_for_url_to_be(MAIN_URL)

    return driver


@pytest.fixture(scope='session')
def ingredients_by_type():
    """
    Группирует названия ингредиентов, полученные через API, по типу
    (bun/sauce/main) — используется, чтобы находить нужный ингредиент
    в UI по alt-тексту картинки, не хардкодя конкретные названия.
    """
    response = get_ingredients()
    ingredients = response.json()['data']

    grouped = {}
    for ingredient in ingredients:
        grouped.setdefault(ingredient['type'], []).append(ingredient)

    return grouped


@pytest.fixture
def api_created_order(registered_user, ingredients_by_type):
    """
    Создаёт для зарегистрированного пользователя один заказ через API —
    используется в тестах Ленты заказов, которым не нужна авторизация в
    браузере (лента и её счётчики доступны неавторизованным пользователям),
    а нужен только сам факт существования заказа.
    Возвращает кортеж (данные ответа регистрации, номер созданного заказа).
    """
    _, register_response = registered_user
    access_token = register_response['accessToken']

    bun_id = ingredients_by_type['bun'][0]['_id']
    filling_id = ingredients_by_type['main'][0]['_id']

    response = create_order([bun_id, filling_id], access_token)
    order_number = response.json()['order']['number']

    return register_response, order_number
