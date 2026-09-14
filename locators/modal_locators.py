from selenium.webdriver.common.by import By


class ModalLocators:
    """
    Общие локаторы для любого модального окна.
    ВАЖНО: приложение держит в DOM одновременно несколько шаблонов модалок
    (ингредиент, успешный заказ, загрузка) — реально открыта обычно только
    одна из них, но общий класс "Modal_modal__..." совпадает у всех сразу.
    Поэтому CLOSE_BUTTON и другие элементы конкретной модалки нужно искать
    не по этим общим локаторам, а от уникального текста внутри именно
    открытой модалки (см. локаторы ниже, привязанные к тексту).
    """

    OVERLAY = (By.CSS_SELECTOR, '[class*="Modal_modal_overlay"]')
    # Глобальный спиннер загрузки приложения. В отличие от остальных модалок-заглушек,
    # этот оверлей действительно ненадолго становится видимым во время переходов
    # между страницами и может физически перекрывать клики по реальным элементам
    # (ElementClickInterceptedException) — поэтому его стоит дожидаться перед кликом.
    LOADING_INDICATOR = (By.CSS_SELECTOR, '[class*="Modal_modal__loading"]')


class IngredientDetailsModalLocators:
    """Локаторы модалки с деталями ингредиента (открывается по клику на ингредиент)."""

    TITLE = (By.XPATH, '//h2[text()="Детали ингредиента"]')
    INGREDIENT_NAME = (
        By.XPATH,
        '//h2[text()="Детали ингредиента"]/following-sibling::p[contains(@class, "text_type_main-medium")]',
    )
    STATS_ITEMS = (
        By.XPATH,
        '//h2[text()="Детали ингредиента"]/parent::div//li[contains(@class, "Modal_modal__statsListItem")]',
    )
    # Кнопка закрытия ищется внутри той же секции, что и заголовок "Детали ингредиента" —
    # это гарантирует клик именно по нужной кнопке, а не по одной из других
    # одновременно присутствующих в DOM модалок.
    CLOSE_BUTTON = (
        By.XPATH,
        '//h2[text()="Детали ингредиента"]/ancestor::section//button[contains(@class, "Modal_modal__close")]',
    )


class OrderCreatedModalLocators:
    """Локаторы модалки успешного оформления заказа (номер заказа)."""

    ORDER_ID_LABEL = (By.XPATH, '//p[text()="идентификатор заказа"]')
    ORDER_NUMBER = (
        By.XPATH,
        '//p[text()="идентификатор заказа"]/preceding-sibling::h2[contains(@class, "Modal_modal__title_shadow")]',
    )
    CLOSE_BUTTON = (
        By.XPATH,
        '//p[text()="идентификатор заказа"]/ancestor::section//button[contains(@class, "Modal_modal__close")]',
    )


class OrderDetailsModalLocators:
    """
    Локаторы модалки с деталями конкретного заказа (открывается по клику
    на карточку заказа в Ленте заказов или в Истории заказов).
    Номер заказа в модалке отображается в формате "#019238", как и в списке заказов.
    """

    ORDER_NUMBER = (By.XPATH, '//*[starts-with(normalize-space(text()), "#")]')
    CLOSE_BUTTON = (
        By.XPATH,
        '//*[starts-with(normalize-space(text()), "#")]/ancestor::section'
        '//button[contains(@class, "Modal_modal__close")]',
    )
