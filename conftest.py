import pytest
from selenium import webdriver

from utils.debug import save_page_source_on_failure


def pytest_addoption(parser):
    parser.addoption(
        '--browsers',
        action='store',
        default='chrome,firefox',
        help='Список браузеров через запятую, в которых нужно прогнать UI-тесты: chrome,firefox',
    )


def pytest_generate_tests(metafunc):
    # Параметризуем фикстуру driver списком браузеров из CLI-опции — так каждый
    # тест, который (прямо или через Page Object) использует driver, автоматически
    # прогоняется во всех указанных браузерах без дублирования кода в тестах.
    if 'driver' in metafunc.fixturenames:
        browsers = metafunc.config.getoption('--browsers').split(',')
        metafunc.parametrize('driver', browsers, indirect=True, ids=browsers)


@pytest.fixture
def driver(request):
    """Создаёт и завершает сессию браузера для одного теста."""
    browser_name = request.param

    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1440,900')
        # Без этого get_log('browser') в utils/debug.py всегда возвращает пусто —
        # а именно там обычно видна настоящая причина "пустой" страницы.
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        browser_driver = webdriver.Chrome(options=options)
    elif browser_name == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        options.add_argument('--width=1440')
        options.add_argument('--height=900')
        browser_driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f'Неизвестный браузер: "{browser_name}". Поддерживаются: chrome, firefox')

    browser_driver.implicitly_wait(5)

    yield browser_driver

    browser_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Модуль дебага: если тест упал, сохраняет HTML-код страницы браузера
    в файл и прикладывает его к Allure-отчёту.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        test_driver = item.funcargs.get('driver')
        if test_driver is not None:
            save_page_source_on_failure(test_driver, item.nodeid)
