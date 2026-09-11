from selenium.webdriver.common.by import By


class ResetPasswordLocators:
    """Локаторы страницы /reset-password."""

    PASSWORD_INPUT = (By.XPATH, '//label[text()="Пароль"]/following-sibling::input')
    # Иконка-«глаз» показать/скрыть пароль лежит внутри того же контейнера, что и сам input
    PASSWORD_SHOW_HIDE_ICON = (
        By.XPATH,
        '//label[text()="Пароль"]/following-sibling::div[contains(@class, "input__icon-action")]',
    )
    CODE_INPUT = (By.XPATH, '//label[text()="Введите код из письма"]/following-sibling::input')
    SAVE_BUTTON = (By.XPATH, '//button[text()="Сохранить"]')
