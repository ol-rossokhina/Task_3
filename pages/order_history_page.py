from typing import List

from locators.order_history_locators import OrderHistoryLocators
from pages.base_page import BasePage


class OrderHistoryPage(BasePage):
    """Page Object раздела /account/order-history."""

    def get_order_numbers(self) -> List[str]:
        """Возвращает номера заказов (в формате '#019238') из истории заказов пользователя."""
        self.find(OrderHistoryLocators.CONTAINER)
        return [element.text for element in self.find_all(OrderHistoryLocators.ORDER_NUMBERS)]
