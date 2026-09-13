import allure

from config import FORGOT_PASSWORD_URL, RESET_PASSWORD_URL
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage
from utils.data_generator import generate_user_data


@allure.feature('Восстановление пароля')
class TestPasswordRecovery:
    """Тесты страниц /forgot-password и /reset-password."""

    @allure.title('Переход на страницу восстановления пароля по кнопке "Восстановить пароль"')
    def test_navigate_to_forgot_password_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open()

        with allure.step('Кликнуть "Восстановить пароль" на странице логина'):
            login_page.click_forgot_password_link()

        forgot_password_page = ForgotPasswordPage(driver)

        with allure.step('Проверить, что открылась страница восстановления пароля'):
            forgot_password_page.wait_for_url_to_be(FORGOT_PASSWORD_URL)
            assert forgot_password_page.is_open()

    @allure.title('После ввода почты и клика "Восстановить" происходит переход на /reset-password')
    def test_submit_email_redirects_to_reset_password(self, driver):
        forgot_password_page = ForgotPasswordPage(driver).open()
        email = generate_user_data()['email']

        with allure.step('Ввести email и отправить форму восстановления пароля'):
            forgot_password_page.enter_email(email)
            forgot_password_page.click_recover()

        with allure.step('Проверить, что произошёл переход на страницу ввода нового пароля'):
            forgot_password_page.wait_for_url_to_be(RESET_PASSWORD_URL)
            assert forgot_password_page.driver.current_url == RESET_PASSWORD_URL

    @allure.title('Клик по иконке "показать пароль" делает поле пароля активным')
    def test_toggle_password_visibility_makes_field_active(self, driver):
        forgot_password_page = ForgotPasswordPage(driver).open()
        email = generate_user_data()['email']

        with allure.step('Дойти до страницы ввода нового пароля'):
            forgot_password_page.enter_email(email)
            forgot_password_page.click_recover()
            forgot_password_page.wait_for_url_to_be(RESET_PASSWORD_URL)

        reset_password_page = ResetPasswordPage(driver)

        with allure.step('Кликнуть по иконке показать/скрыть пароль'):
            reset_password_page.toggle_password_visibility()

        with allure.step('Проверить, что поле пароля стало активным элементом страницы'):
            assert reset_password_page.is_password_field_active()
