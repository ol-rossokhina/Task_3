from selenium.common.exceptions import TimeoutException

from config import MAIN_URL
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from pages.ingredient_details_modal import IngredientDetailsModal
from pages.order_created_modal import OrderCreatedModal
from utils.drag_and_drop import drag_and_drop


class MainPage(BasePage):
    """Page Object страницы конструктора (/)."""

    def open(self) -> 'MainPage':
        self.driver.get(MAIN_URL)
        return self

    def open_ingredient_details(self, ingredient_name: str) -> IngredientDetailsModal:
        self.click(MainPageLocators.ingredient_card(ingredient_name))
        return IngredientDetailsModal(self.driver)

    def add_bun_to_constructor(self, bun_name: str) -> None:
        source = self.find(MainPageLocators.ingredient_card(bun_name))
        target = self.find(MainPageLocators.BUN_DROP_ZONE)
        drag_and_drop(self.driver, source, target)

    def add_ingredient_to_constructor(self, ingredient_name: str) -> None:
        source = self.find(MainPageLocators.ingredient_card(ingredient_name))
        target = self.find_present(MainPageLocators.CONSTRUCTOR_DROP_ZONE)
        drag_and_drop(self.driver, source, target)

    def get_ingredient_counter(self, ingredient_name: str) -> int:
        try:
            counter_text = self.find(MainPageLocators.ingredient_counter(ingredient_name)).text
        except TimeoutException:
            return 0
        return int(counter_text)

    def get_total_price(self) -> int:
        return int(self.find(MainPageLocators.TOTAL_PRICE).text)

    def click_order_button(self) -> OrderCreatedModal:
        self.click(MainPageLocators.ORDER_BUTTON)
        return OrderCreatedModal(self.driver)
