from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы страницы конструктора (/)."""

    # Зона для булки (перетаскивание в любой из слотов автоматически ставит булку и сверху, и снизу)
    BUN_DROP_ZONE = (By.CSS_SELECTOR, '[class*="constructor-element_pos_top"]')
    # Зона, куда перетаскиваются начинки и соусы (изначально пустой <span>, заполняется после добавления)
    CONSTRUCTOR_DROP_ZONE = (By.CSS_SELECTOR, '[class*="BurgerConstructor_basket__listContainer"]')

    ORDER_BUTTON = (By.XPATH, '//button[text()="Оформить заказ"]')
    TOTAL_PRICE = (By.CSS_SELECTOR, '[class*="BurgerConstructor_basket__totalContainer"] p')

    @staticmethod
    def ingredient_card(ingredient_name: str):
        """Карточка ингредиента в списке слева — источник для drag-and-drop и клика."""
        return By.XPATH, f'//a[.//img[@alt="{ingredient_name}"]]'

    @staticmethod
    def ingredient_counter(ingredient_name: str):
        """Каунтер количества конкретного ингредиента, уже добавленного в заказ."""
        return (
            By.XPATH,
            f'//a[.//img[@alt="{ingredient_name}"]]//p[contains(@class, "counter_counter__num")]',
        )
