from config import MAIN_URL, PROFILE_URL
from locators.profile_locators import ProfileLocators
from pages.base_page import BasePage
from pages.order_history_page import OrderHistoryPage


class ProfilePage(BasePage):
    """Page Object раздела /account/profile."""

    def open(self) -> 'ProfilePage':
        self.open_url(MAIN_URL)
        self.go_to_personal_account()
        self.wait_for_url_to_be(PROFILE_URL)
        return self

    def is_open(self) -> bool:
        return self.is_present(ProfileLocators.NAME_INPUT)

    def go_to_order_history(self) -> OrderHistoryPage:
        self.click(ProfileLocators.ORDER_HISTORY_TAB)
        return OrderHistoryPage(self.driver)

    def logout(self) -> None:
        self.click(ProfileLocators.LOGOUT_BUTTON)
