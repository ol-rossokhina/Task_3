from selenium.webdriver.common.by import By


class HeaderLocators:
    """Локаторы навигации в шапке — присутствует на всех страницах."""

    CONSTRUCTOR_LINK = (By.XPATH, '//a[.//p[text()="Конструктор"]]')
    FEED_LINK = (By.XPATH, '//a[.//p[text()="Лента Заказов"]]')
    PERSONAL_ACCOUNT_LINK = (By.XPATH, '//a[.//p[text()="Личный Кабинет"]]')