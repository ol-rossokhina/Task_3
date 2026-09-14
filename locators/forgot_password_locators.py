from selenium.webdriver.common.by import By


class ForgotPasswordLocators:
    """Локаторы страницы /forgot-password."""

    TITLE = (By.XPATH, '//h2[text()="Восстановление пароля"]')
    EMAIL_INPUT = (By.XPATH, '//label[text()="Email"]/following-sibling::input')
    RECOVER_BUTTON = (By.XPATH, '//button[text()="Восстановить"]')
