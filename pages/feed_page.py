import time
from typing import List, Tuple

from config import FEED_URL
from locators.feed_locators import FeedLocators
from pages.base_page import BasePage
from pages.order_details_modal import OrderDetailsModal

# Заказ переходит в статус "готов" на сервере не мгновенно, а с реальной
# задержкой обработки — столько (в секундах) ждём, пока счётчики "Выполнено" обновятся.
COUNTERS_UPDATE_TIMEOUT = 60
COUNTERS_POLL_INTERVAL = 1

# Лента показывает только последние 5 заказов в каждом разделе и обновляется
# не мгновенно — на активном стенде заказ может не успеть попасть в список
# с первой попытки, если параллельно создаются другие заказы.
FEED_LIST_UPDATE_TIMEOUT = 30
FEED_LIST_POLL_INTERVAL = 1


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
        poll_interval: int = COUNTERS_POLL_INTERVAL,
    ) -> Tuple[int, int]:
        """
        Заказ, только что созданный через API, не сразу учитывается в счётчиках
        "Выполнено" — сервер обрабатывает его (created -> done) с задержкой.
        Поэтому вместо проверки сразу после создания раз в секунду обновляем
        ленту и проверяем счётчики, пока оба не увеличатся либо не закончатся попытки.
        """
        total_after, today_after = total_before, today_before

        for _ in range(timeout // poll_interval):
            self.open()
            total_after = self.get_total_done_count()
            today_after = self.get_today_done_count()

            if total_after > total_before and today_after > today_before:
                break

            time.sleep(poll_interval)
        else:
            raise TimeoutError(
                f'Счётчики не увеличились за {timeout} секунд ожидания: '
                f'было total={total_before}, today={today_before}; '
                f'осталось total={total_after}, today={today_after}'
            )

        return total_after, today_after

    def wait_for_order_in_progress(
        self,
        formatted_order_number: str,
        timeout: int = FEED_LIST_UPDATE_TIMEOUT,
        poll_interval: int = FEED_LIST_POLL_INTERVAL,
    ) -> List[str]:
        """
        Лента показывает только последние 5 заказов "В работе" и обновляется
        не мгновенно — между созданием заказа через API и открытием ленты
        на активном стенде успевают появиться другие заказы, из-за чего наш
        может не попасть в список с первой попытки. Поэтому вместо одной
        проверки раз в секунду обновляем ленту, пока заказ не появится
        в списке либо не закончатся попытки.
        """
        in_progress_orders: List[str] = []

        for _ in range(timeout // poll_interval):
            self.open()
            in_progress_orders = self.get_in_progress_order_numbers()

            if formatted_order_number in in_progress_orders:
                break

            time.sleep(poll_interval)
        else:
            raise TimeoutError(
                f'Заказ {formatted_order_number} не появился в разделе "В работе" '
                f'за {timeout} секунд ожидания: последний раз список был {in_progress_orders}'
            )

        return in_progress_orders
