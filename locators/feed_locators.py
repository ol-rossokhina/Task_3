from selenium.webdriver.common.by import By


class FeedLocators:
    """Локаторы страницы /feed."""

    # Карточки заказов в ленте (переиспользуют компонент карточки из истории заказов)
    ORDER_CARDS = (By.CSS_SELECTOR, '[class*="OrderFeed_list"] a[class*="OrderHistory_link"]')
    ORDER_CARD_NUMBERS = (
        By.CSS_SELECTOR,
        '[class*="OrderFeed_list"] p[class*="text_type_digits-default"]',
    )

    TOTAL_DONE_COUNT = (By.XPATH, '//p[text()="Выполнено за все время:"]/following-sibling::p')
    TODAY_DONE_COUNT = (By.XPATH, '//p[text()="Выполнено за сегодня:"]/following-sibling::p')

    IN_PROGRESS_ORDERS_LIST = (By.XPATH, '//ul[@class="OrderFeed_orderList__cBvyi"]/li')
    READY_ORDERS_LIST = (By.CSS_SELECTOR, '[class*="OrderFeed_orderListReady"] li')
