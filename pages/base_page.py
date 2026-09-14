from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.base_locators import HeaderLocators
from locators.modal_locators import ModalLocators

DEFAULT_TIMEOUT = 10
APP_LOAD_TIMEOUT = 30


class BasePage:
    """Базовый класс для всех Page Object: навигация по шапке и обёртки над ожиданиями."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open_url(self, url: str) -> None:
        """
        Открывает URL и дожидается, что React-приложение реально
        отрисовалось (по наличию шапки — она есть на каждой странице),
        а не просто вернулся пустой <div id="root"> из-за медленной
        загрузки статических чанков. Если с первого раза не получилось —
        пробует ещё раз перед тем, как дать тесту упасть.
        """
        for attempt in range(2):
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, APP_LOAD_TIMEOUT).until(
                    EC.presence_of_element_located(HeaderLocators.CONSTRUCTOR_LINK)
                )
                return
            except TimeoutException:
                if attempt == 1:
                    raise

    def find(self, locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator) -> None:
        # Приложение может ненадолго показывать глобальный спиннер загрузки
        # поверх страницы (например, сразу после захода на страницу или после
        # отправки формы) — он физически перекрывает элементы и приводит к
        # ElementClickInterceptedException. Проверка общая для ЛЮБОГО клика.
        self.wait_for_invisibility(ModalLocators.LOADING_INDICATOR)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def is_present(self, locator) -> bool:
        """Проверяет наличие элемента на странице, не выбрасывая исключение, если его нет."""
        try:
            self.find(locator)
            return True
        except TimeoutException:
            return False

    def wait_for_invisibility(self, locator) -> None:
        """Ждёт, пока элемент перестанет быть видимым (используется после закрытия модалок)."""
        self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_url_contains(self, path: str) -> None:
        self.wait.until(EC.url_contains(path))

    def wait_for_url_to_be(self, url: str) -> None:
        self.wait.until(EC.url_to_be(url))

    def wait_until(self, condition, timeout: int, poll_frequency: float = 1) -> None:
        """
        Ждёт выполнения произвольного условия (функции от driver) с заданной
        частотой опроса. Общая точка входа для нестандартных ожиданий, для
        которых нет готового expected_conditions — чтобы Page Object не
        создавали WebDriverWait самостоятельно, а пользовались этим методом.
        """
        WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency).until(condition)

    def get_active_element(self) -> WebElement:
        """Возвращает текущий активный (сфокусированный) элемент страницы."""
        return self.driver.execute_script('return document.activeElement')

    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.driver.current_url    

    # Навигация по шапке — общая для всех страниц

    def go_to_constructor(self) -> None:
        self.click(HeaderLocators.CONSTRUCTOR_LINK)

    def go_to_feed(self) -> None:
        self.click(HeaderLocators.FEED_LINK)

    def go_to_personal_account(self) -> None:
        self.click(HeaderLocators.PERSONAL_ACCOUNT_LINK)
