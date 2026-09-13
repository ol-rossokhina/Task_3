import allure

from config import LOGIN_URL, ORDER_HISTORY_URL, PROFILE_URL
from pages.main_page import MainPage
from pages.profile_page import ProfilePage


@allure.feature('Личный кабинет')
class TestPersonalAccount:
    """Тесты раздела /account (доступен только авторизованному пользователю)."""

    @allure.title('Переход в личный кабинет по клику на "Личный Кабинет" в шапке')
    def test_navigate_to_personal_account(self, logged_in_driver):
        main_page = MainPage(logged_in_driver)

        with allure.step('Кликнуть "Личный Кабинет" в шапке'):
            main_page.go_to_personal_account()

        with allure.step('Проверить, что открылся личный кабинет'):
            main_page.wait_for_url_to_be(PROFILE_URL)
            assert ProfilePage(logged_in_driver).is_open()

    @allure.title('Переход в историю заказов по клику на вкладку "История заказов"')
    def test_navigate_to_order_history(self, logged_in_driver):
        profile_page = ProfilePage(logged_in_driver).open()

        with allure.step('Кликнуть вкладку "История заказов"'):
            profile_page.go_to_order_history()

        with allure.step('Проверить, что открылась история заказов'):
            profile_page.wait_for_url_to_be(ORDER_HISTORY_URL)

    @allure.title('Выход из личного кабинета по клику на "Выход"')
    def test_logout(self, logged_in_driver):
        profile_page = ProfilePage(logged_in_driver).open()

        with allure.step('Кликнуть "Выход"'):
            profile_page.logout()

        with allure.step('Проверить, что пользователь вышел и перенаправлен на страницу входа'):
            profile_page.wait_for_url_to_be(LOGIN_URL)
