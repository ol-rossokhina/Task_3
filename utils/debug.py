import os

import allure
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

DEBUG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'debug_reports')


def save_page_source_on_failure(driver: WebDriver, test_name: str) -> None:
    """
    При падении теста сохраняет в файл (папка debug_reports) и прикладывает
    к Allure-отчёту:
    - HTML-код страницы;
    - текущий URL (страница может быть пустой из-за редиректа в неожиданное
      место, а не только из-за медленной загрузки);
    - консоль браузера (только для Chrome — geckodriver/Firefox не отдаёт
      логи консоли через стандартный Selenium API), где обычно видна
      настоящая причина "пустого" экрана — необработанная JS-ошибка
      или ChunkLoadError.

    Это диагностический код: он не должен ронять прогон тестов, даже если
    к моменту вызова сессия браузера уже недоступна (например, браузер упал
    или был закрыт) — поэтому обращения к driver обёрнуты в try/except.
    """
    os.makedirs(DEBUG_DIR, exist_ok=True)
    safe_name = test_name.replace('/', '_').replace('::', '__').replace(' ', '_')

    try:
        page_source = driver.page_source
        current_url = driver.current_url
    except WebDriverException as error:
        allure.attach(
            f'Не удалось получить состояние страницы: сессия браузера уже недоступна.\n{error}',
            name=f'debug_unavailable_{safe_name}',
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    html_path = os.path.join(DEBUG_DIR, f'{safe_name}.html')
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(page_source)

    allure.attach(
        page_source,
        name=f'page_source_{safe_name}',
        attachment_type=allure.attachment_type.HTML,
    )
    allure.attach(
        current_url,
        name=f'current_url_{safe_name}',
        attachment_type=allure.attachment_type.TEXT,
    )

    try:
        browser_logs = driver.get_log('browser')
    except Exception:
        browser_logs = None

    if browser_logs:
        logs_text = '\n'.join(f'{entry["level"]}: {entry["message"]}' for entry in browser_logs)
        logs_path = os.path.join(DEBUG_DIR, f'{safe_name}_console.log')
        with open(logs_path, 'w', encoding='utf-8') as file:
            file.write(logs_text)

        allure.attach(
            logs_text,
            name=f'browser_console_{safe_name}',
            attachment_type=allure.attachment_type.TEXT,
        )
