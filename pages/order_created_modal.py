from locators.modal_locators import OrderCreatedModalLocators
from pages.base_page import BasePage


class OrderCreatedModal(BasePage):
    """Page Object модалки, которая появляется сразу после успешного оформления заказа."""

    def is_open(self) -> bool:
        return self.is_present(OrderCreatedModalLocators.ORDER_ID_LABEL)

    def get_order_number(self) -> str:
        return self.find(OrderCreatedModalLocators.ORDER_NUMBER).text

    def close(self) -> None:
        self.click(OrderCreatedModalLocators.CLOSE_BUTTON)
        self.wait_for_invisibility(OrderCreatedModalLocators.ORDER_ID_LABEL)
