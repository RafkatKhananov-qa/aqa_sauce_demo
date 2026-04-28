from playwright.sync_api import expect
from config.base import BASE_URL
import allure


class BasePage:
    def __init__(self, page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")
        self.burger_menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_button = page.locator("[data-test='logout-sidebar-link']")
        self.sidebar_links = page.locator("//nav[@class='bm-item-list']/a")
        self.close_sidebar_button = page.locator("#react-burger-cross-btn")
        self.sidebar = page.locator(".bm-menu")

    @allure.step("Открыть страницу входа на сайт Swag Labs")
    def open(self, url=BASE_URL):
        self.page.goto(url)

    @allure.step("Эмулировать сеть 3G")
    def emulate_3g(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": 375 * 1024 / 8,
            "uploadThroughput": 750 * 1024 / 8,
            "latency": 100
        })

    @allure.step("Получить размер используемой JS-памяти")
    def get_memory_usage_bytes(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Performance.enable")
        metrics = cdp.send("Performance.getMetrics")
        return next(m["value"] for m in metrics["metrics"] if m["name"] == "JSHeapUsedSize")

    @allure.step("Получить время загрузи страницы в миллисекундах")
    def get_load_time_ms(self):
        return self.page.evaluate(
            "() => performance.timing.loadEventEnd - performance.timing.navigationStart"
        )

    @allure.step("Кликнуть по иконке корзины в header сайта")
    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    @allure.step("Проверить количество товаров в корзине")
    def verify_items_count_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    @allure.step("Проверить, что корзина пуста")
    def verify_bucket_is_empty(self):
        expect(self.cart_badge).to_have_count(0)

    @allure.step("Кликнуть по бургер-меню")
    def click_burger_menu_button(self):
        self.burger_menu_btn.click()

    @allure.step("Кликнуть по кнопке Logout")
    def click_logout_button(self):
        self.logout_button.click()

    @allure.step("Проверить, что элемент кликабелен")
    def click_visible_button(self, locator):
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        locator.click(trial=True)

    @allure.step("Проверить, что все элементы кликабельны")
    def verify_all_clickable(self, locator):
        for i in range(locator.count()):
            self.click_visible_button(locator.nth(i))

    @allure.step("Проверить, что все ссылки в боковом меню кликабельны")
    def verify_sidebar_links_are_clickable(self):
        self.verify_all_clickable(self.sidebar_links)

    @allure.step("Закрыть боковое меню")
    def click_close_sidebar_button(self):
        self.close_sidebar_button.click()

    @allure.step("Проверить, что боковое меню не отображается")
    def verify_sidebar_is_not_visible(self):
        expect(self.sidebar).not_to_be_visible()
