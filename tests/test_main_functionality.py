import allure

from config import FEED_URL, MAIN_URL
from pages.base_page import BasePage
from pages.main_page import MainPage


@allure.feature('Основной функционал')
class TestMainFunctionality:
    """Тесты страницы конструктора (/) и переходов между основными разделами."""

    @allure.title('Переход в конструктор по клику на "Конструктор" в шапке')
    def test_navigate_to_constructor(self, driver):
        base_page = BasePage(driver)
        base_page.driver.get(FEED_URL)

        with allure.step('Кликнуть "Конструктор" в шапке'):
            base_page.go_to_constructor()

        with allure.step('Проверить, что открылась страница конструктора'):
            base_page.wait_for_url_to_be(MAIN_URL)

    @allure.title('Переход в ленту заказов по клику на "Лента заказов" в шапке')
    def test_navigate_to_feed(self, driver):
        base_page = BasePage(driver)
        base_page.driver.get(MAIN_URL)

        with allure.step('Кликнуть "Лента заказов" в шапке'):
            base_page.go_to_feed()

        with allure.step('Проверить, что открылась лента заказов'):
            base_page.wait_for_url_to_be(FEED_URL)

    @allure.title('Клик по ингредиенту открывает модалку с его деталями')
    def test_ingredient_click_opens_details_modal(self, driver, ingredients_by_type):
        main_page = MainPage(driver).open()
        ingredient_name = ingredients_by_type['sauce'][0]['name']

        with allure.step(f'Кликнуть на ингредиент "{ingredient_name}"'):
            ingredient_modal = main_page.open_ingredient_details(ingredient_name)

        with allure.step('Проверить, что открылась модалка с деталями именно этого ингредиента'):
            assert ingredient_modal.is_open()
            assert ingredient_modal.get_ingredient_name() == ingredient_name

    @allure.title('Модалка с деталями ингредиента закрывается по крестику')
    def test_close_ingredient_modal_by_cross(self, driver, ingredients_by_type):
        main_page = MainPage(driver).open()
        ingredient_name = ingredients_by_type['sauce'][0]['name']
        ingredient_modal = main_page.open_ingredient_details(ingredient_name)

        with allure.step('Закрыть модалку по крестику'):
            ingredient_modal.close()

        with allure.step('Проверить, что модалка закрылась'):
            assert not ingredient_modal.is_open()

    @allure.title('Добавление ингредиента в заказ увеличивает его каунтер')
    def test_add_ingredient_increases_counter(self, driver, ingredients_by_type):
        main_page = MainPage(driver).open()
        ingredient_name = ingredients_by_type['main'][0]['name']

        with allure.step('Проверить, что каунтер ингредиента изначально равен 0'):
            assert main_page.get_ingredient_counter(ingredient_name) == 0

        with allure.step(f'Перетащить ингредиент "{ingredient_name}" в конструктор'):
            main_page.add_ingredient_to_constructor(ingredient_name)

        with allure.step('Проверить, что каунтер ингредиента увеличился до 1'):
            assert main_page.get_ingredient_counter(ingredient_name) == 1

    @allure.title('Авторизованный пользователь может оформить заказ')
    def test_logged_in_user_can_create_order(self, logged_in_driver, ingredients_by_type):
        main_page = MainPage(logged_in_driver).open()
        bun_name = ingredients_by_type['bun'][0]['name']
        filling_name = ingredients_by_type['main'][0]['name']

        with allure.step('Собрать бургер: булка + начинка'):
            main_page.add_bun_to_constructor(bun_name)
            main_page.add_ingredient_to_constructor(filling_name)

        with allure.step('Нажать "Оформить заказ"'):
            order_modal = main_page.click_order_button()

        with allure.step('Проверить, что заказ оформлен и показан его номер'):
            assert order_modal.is_open()
            assert order_modal.get_order_number().isdigit()
