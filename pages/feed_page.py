from typing import List, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from config import FEED_URL
from locators.feed_locators import FeedLocators
from pages.base_page import BasePage
from pages.order_details_modal import OrderDetailsModal

# Заказ переходит в статус "готов" на сервере не мгновенно, а с реальной
# задержкой обработки — столько (в секундах) ждём, пока счётчики "Выполнено" обновятся.
COUNTERS_UPDATE_TIMEOUT = 60
COUNTERS_POLL_FREQUENCY = 1

# Лента показывает только последние 5 заказов в каждом разделе и обновляется
# не мгновенно — на активном стенде заказ может не успеть попасть в список
# с первой попытки, если параллельно создаются другие заказы.
FEED_LIST_UPDATE_TIMEOUT = 30
FEED_LIST_POLL_FREQUENCY = 1


class FeedPage(BasePage):
    """Page Object страницы /feed."""

    def open(self) -> 'FeedPage':
        self.open_url(FEED_URL)
        return self

    def get_order_numbers(self) -> List[str]:
        """Возвращает номера заказов (в формате '#019238') из карточек в ленте."""
        return [element.text for element in self.find_all(FeedLocators.ORDER_CARD_NUMBERS)]

    def open_first_order(self) -> OrderDetailsModal:
        self.click(FeedLocators.ORDER_CARDS)
        return OrderDetailsModal(self.driver)

    def get_total_done_count(self) -> int:
        return int(self.find(FeedLocators.TOTAL_DONE_COUNT).text)

    def get_today_done_count(self) -> int:
        return int(self.find(FeedLocators.TODAY_DONE_COUNT).text)

    def get_ready_order_numbers(self) -> List[str]:
        return [element.text for element in self.find_all(FeedLocators.READY_ORDERS_LIST)]

    def get_in_progress_order_numbers(self) -> List[str]:
        return [element.text for element in self.find_all(FeedLocators.IN_PROGRESS_ORDERS_LIST)]

    def wait_for_counters_increase(
        self,
        total_before: int,
        today_before: int,
        timeout: int = COUNTERS_UPDATE_TIMEOUT,
        poll_frequency: int = COUNTERS_POLL_FREQUENCY,
    ) -> Tuple[int, int]:
        """
        Заказ, только что созданный через API, не сразу учитывается в счётчиках
        "Выполнено" — сервер обрабатывает его (created -> done) с задержкой.
        Вместо проверки сразу после создания дожидаемся увеличения обоих
        счётчиков через WebDriverWait с кастомным условием (готового
        expected_conditions для сравнения двух чисел между перезагрузками
        страницы в Selenium нет, поэтому условие описано отдельной функцией
        и передано в until — без ручных time.sleep).
        """
        result: dict = {}

        def _counters_increased(_driver) -> bool:
            self.open()
            total_after = self.get_total_done_count()
            today_after = self.get_today_done_count()
            result['last_total'] = total_after
            result['last_today'] = today_after

            if total_after > total_before and today_after > today_before:
                result['total'] = total_after
                result['today'] = today_after
                return True

            return False

        try:
            WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency).until(_counters_increased)
        except TimeoutException:
            raise TimeoutError(
                f'Счётчики не увеличились за {timeout} секунд ожидания: '
                f'было total={total_before}, today={today_before}; '
                f'осталось total={result.get("last_total")}, today={result.get("last_today")}'
            )

        return result['total'], result['today']

    def wait_for_order_in_progress(
        self,
        formatted_order_number: str,
        timeout: int = FEED_LIST_UPDATE_TIMEOUT,
        poll_frequency: int = FEED_LIST_POLL_FREQUENCY,
    ) -> List[str]:
        """
        Лента показывает только последние 5 заказов "В работе" и обновляется
        не мгновенно — между созданием заказа через API и открытием ленты
        на активном стенде успевают появиться другие заказы, из-за чего наш
        может не попасть в список с первой попытки. Дожидаемся появления
        заказа через WebDriverWait с кастомным условием, а не ручным опросом.
        """
        result: dict = {}

        def _order_appeared(_driver) -> bool:
            self.open()
            orders = self.get_in_progress_order_numbers()
            result['last_seen'] = orders

            if formatted_order_number in orders:
                result['orders'] = orders
                return True

            return False

        try:
            WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency).until(_order_appeared)
        except TimeoutException:
            raise TimeoutError(
                f'Заказ {formatted_order_number} не появился в разделе "В работе" '
                f'за {timeout} секунд ожидания: последний раз список был {result.get("last_seen")}'
            )

        return result['orders']
