from selenium.webdriver.remote.webelement import WebElement

from locators.reset_password_locators import ResetPasswordLocators
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    """Page Object страницы /reset-password."""

    def get_password_input(self) -> WebElement:
        return self.find(ResetPasswordLocators.PASSWORD_INPUT)

    def toggle_password_visibility(self) -> None:
        self.click(ResetPasswordLocators.PASSWORD_SHOW_HIDE_ICON)

    def is_password_field_active(self) -> bool:
        """Проверяет, что поле пароля стало активным элементом страницы (в фокусе)."""
        password_input = self.get_password_input()
        return password_input == self.get_active_element()
