import allure

from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage
from utils.api_client import create_order


def _format_order_number(order_number: int) -> str:
    """Лента и история показывают номер заказа в формате '#019238' — с ведущими нулями до 6 знаков."""
    return f'#{order_number:06d}'


@allure.feature('Лента заказов')
class TestOrderFeed:
    """Тесты страницы /feed."""

    @allure.title('Клик по заказу в ленте открывает модалку с деталями этого заказа')
    def test_click_order_opens_details_modal(self, driver, api_created_order):
        _, order_number = api_created_order
        feed_page = FeedPage(driver).open()

        with allure.step('Открыть первый заказ в ленте'):
            order_modal = feed_page.open_first_order()

        with allure.step('Проверить, что модалка с деталями заказа открылась'):
            assert order_modal.is_open()

    @allure.title('Заказ из истории заказов пользователя отображается в ленте заказов')
    def test_user_order_appears_in_feed(self, logged_in_driver, registered_user, ingredients_by_type):
        _, register_response = registered_user
        access_token = register_response['accessToken']
        bun_id = ingredients_by_type['bun'][0]['_id']
        filling_id = ingredients_by_type['main'][0]['_id']

        with allure.step('Создать заказ для пользователя через API'):
            response = create_order([bun_id, filling_id], access_token)
            order_number = _format_order_number(response.json()['order']['number'])

        with allure.step('Проверить, что заказ отображается в истории заказов пользователя'):
            order_history_page = ProfilePage(logged_in_driver).open().go_to_order_history()
            assert order_number in order_history_page.get_order_numbers()

        with allure.step('Проверить, что тот же заказ отображается в общей ленте заказов'):
            feed_page = FeedPage(logged_in_driver).open()
            assert order_number in feed_page.get_order_numbers()

    @allure.title('После оформления нового заказа счётчики "Выполнено" увеличиваются')
    def test_feed_counters_increase_after_new_order(self, driver, registered_user, ingredients_by_type):
        feed_page = FeedPage(driver).open()

        with allure.step('Запомнить текущие значения счётчиков'):
            total_before = feed_page.get_total_done_count()
            today_before = feed_page.get_today_done_count()

        _, register_response = registered_user
        access_token = register_response['accessToken']
        bun_id = ingredients_by_type['bun'][0]['_id']
        filling_id = ingredients_by_type['main'][0]['_id']

        with allure.step('Создать новый заказ через API'):
            create_order([bun_id, filling_id], access_token)

        with allure.step('Дождаться, пока сервер обработает заказ, и проверить, что счётчики увеличились'):
            total_after, today_after = feed_page.wait_for_counters_increase(total_before, today_before)
            assert total_after > total_before
            assert today_after > today_before

    @allure.title('Номер нового заказа появляется в разделе "В работе"')
    def test_new_order_appears_in_progress_section(self, driver, api_created_order):
        _, order_number = api_created_order
        # В разделах "Готовы"/"В работе" номер показывается без "#", но с ведущими нулями
        formatted_number = f'{order_number:06d}'

        with allure.step('Открыть ленту заказов'):
            feed_page = FeedPage(driver).open()

        with allure.step('Дождаться, пока заказ появится в разделе "В работе"'):
            in_progress_orders = feed_page.wait_for_order_in_progress(formatted_number)
            assert formatted_number in in_progress_orders
