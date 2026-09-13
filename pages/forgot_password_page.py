from config import FORGOT_PASSWORD_URL
from locators.forgot_password_locators import ForgotPasswordLocators
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    """Page Object страницы /forgot-password."""

    def open(self) -> 'ForgotPasswordPage':
        self.open_url(FORGOT_PASSWORD_URL)
        return self

    def is_open(self) -> bool:
        return self.is_present(ForgotPasswordLocators.TITLE)

    def enter_email(self, email: str) -> None:
        self.find(ForgotPasswordLocators.EMAIL_INPUT).send_keys(email)

    def click_recover(self) -> None:
        self.click(ForgotPasswordLocators.RECOVER_BUTTON)
