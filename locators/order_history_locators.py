from selenium.webdriver.common.by import By


class OrderHistoryLocators:
    """Локаторы раздела /account/order-history."""

    CONTAINER = (By.CSS_SELECTOR, '[class*="OrderHistory_orderHistory"]')
    ORDER_NUMBERS = (
        By.CSS_SELECTOR,
        '[class*="OrderHistory_orderHistory"] p[class*="text_type_digits-default"]',
    )
