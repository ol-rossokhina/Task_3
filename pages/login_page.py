from config import LOGIN_URL
from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object страницы /login."""

    def open(self) -> 'LoginPage':
        self.open_url(LOGIN_URL)
        return self

    def login(self, email: str, password: str) -> None:
        self.find(LoginLocators.EMAIL_INPUT).send_keys(email)
        self.find(LoginLocators.PASSWORD_INPUT).send_keys(password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def click_forgot_password_link(self) -> None:
        self.click(LoginLocators.FORGOT_PASSWORD_LINK)
