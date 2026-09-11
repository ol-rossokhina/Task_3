from selenium.webdriver.common.by import By


class LoginLocators:
    """Локаторы страницы /login."""

    EMAIL_INPUT = (By.XPATH, '//label[text()="Email"]/following-sibling::input')
    PASSWORD_INPUT = (By.XPATH, '//label[text()="Пароль"]/following-sibling::input')
    LOGIN_BUTTON = (By.XPATH, '//button[text()="Войти"]')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, 'Восстановить пароль')
