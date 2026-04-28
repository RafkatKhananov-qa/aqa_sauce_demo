import allure
from config.base import INVENTORY_URL
from config.users import USER_PASSWORD, USER1_NAME
from pages.base_page import BasePage
from pages.login_page import LoginPage


@allure.feature("UI Performance")
class TestPerformance:
    @allure.story("Page Load")
    @allure.title("Загрузка страницы inventory не превышает 3 секунды")
    def test_perf_001(self, logged_in_page):
        base_page = BasePage(logged_in_page)
        base_page.open(INVENTORY_URL)
        assert base_page.get_load_time_ms() < 3000

    @allure.story("Login Performance")
    @allure.title("Время отклика при авторизации не превышает 1 секунды")
    def test_perf_002(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USER_PASSWORD)
        assert login_page.click_login_and_get_response_time_ms() < 1000

    @allure.story("Stability")
    @allure.title("Авторизация стабильна при 10 последовательных входах")
    def test_perf_003(self, page):
        for _ in range(10):
            login_page = LoginPage(page)
            login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

    @allure.story("Network Conditions")
    @allure.title("Авторизация проходит успешно при эмуляции 3G сети")
    def test_perf_004(self, page):
        login_page = LoginPage(page)
        login_page.emulate_3g()
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

    @allure.story("Memory Usage")
    @allure.title("Потребление памяти не увеличивается более чем на 20% при открытии 20 вкладок")
    def test_perf_005(self, logged_in_page):
        base_page = BasePage(logged_in_page)
        memory_before = base_page.get_memory_usage_bytes()

        context = logged_in_page.context.browser.new_context()
        pages = []
        for _ in range(20):
            p = context.new_page()
            p.goto(INVENTORY_URL)
            pages.append(p)

        context.close()

        memory_after = base_page.get_memory_usage_bytes()
        assert memory_after <= memory_before * 1.2
