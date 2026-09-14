from locators.modal_locators import OrderDetailsModalLocators
from pages.base_page import BasePage


class OrderDetailsModal(BasePage):
    """
    Page Object модалки с деталями заказа.
    Открывается поверх Ленты заказов или Истории заказов по клику на карточку
    заказа и имеет собственный маршрут (/feed/<id> или .../order-history/<id>).
    """

    def is_open(self) -> bool:
        return self.is_present(OrderDetailsModalLocators.ORDER_NUMBER)

    def get_order_number(self) -> str:
        return self.find(OrderDetailsModalLocators.ORDER_NUMBER).text

    def close(self) -> None:
        self.click(OrderDetailsModalLocators.CLOSE_BUTTON)
        self.wait_for_invisibility(OrderDetailsModalLocators.ORDER_NUMBER)
