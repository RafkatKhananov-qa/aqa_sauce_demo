from pathlib import Path

import allure
from playwright.sync_api import expect

from config.base import BASE_URL
from pages.mixins.accessibility_mixin import AccessibilityMixin
from pages.mixins.mobile_mixin import MobileMixin
from pages.mixins.performance_mixin import PerformanceMixin
from pages.mixins.storage_mixin import StorageMixin
from utils.logger import get_logger

logger = get_logger("base_page")


class BasePage(PerformanceMixin, MobileMixin, AccessibilityMixin, StorageMixin):
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
        logger.info(f"Переход на {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Переход на предыдущую страницу")
    def go_to_previous_page(self):
        logger.info("Переход на предыдущую страницу (go_back)")
        self.page.go_back(wait_until="load")

    @allure.step("Дождаться полной загрузки страницы")
    def wait_until_page_fully_loaded(self):
        logger.info("Ожидание полной загрузки страницы")
        self.page.wait_for_load_state("load")

    # --- Корзина ---

    @allure.step("Кликнуть по иконке корзины в header сайта")
    def click_shopping_cart_icon(self):
        logger.debug("Клик по иконке корзины")
        self.shopping_cart_icon.click()

    @allure.step("Кликнуть по иконке корзины в header сайта (tap)")
    def tap_shopping_cart_icon(self):
        logger.debug("Тап по иконке корзины в header сайта")
        self.shopping_cart_icon.tap()

    @allure.step("Проверить количество товаров в корзине")
    def verify_items_count_in_bucket(self, num: str):
        logger.debug(f"Проверка количества товаров в корзине: ожидается '{num}'")
        expect(self.cart_badge).to_have_text(num)

    @allure.step("Проверить, что корзина пуста")
    def verify_bucket_is_empty(self):
        logger.debug("Проверка, что корзина пуста")
        expect(self.cart_badge).to_have_count(0)

    # --- Боковое меню ---

    @allure.step("Кликнуть по бургер-меню")
    def click_burger_menu_button(self):
        logger.debug("Клик по бургер-меню")
        self.burger_menu_btn.click()

    @allure.step("Кликнуть по кнопке Logout")
    def click_logout_button(self):
        logger.debug("Клик по кнопке Logout")
        self.logout_button.click()

    @allure.step("Закрыть боковое меню")
    def click_close_sidebar_button(self):
        logger.debug("Клик по кнопке закрытия бокового меню")
        self.close_sidebar_button.click()

    @allure.step("Проверить, что боковое меню не отображается")
    def verify_sidebar_is_not_visible(self):
        logger.debug("Проверка, что боковое меню скрыто")
        expect(self.sidebar).to_be_hidden()

    @allure.step("Проверить, что боковое меню отображается")
    def verify_sidebar_is_visible(self):
        logger.debug("Проверка, что боковое меню видимо")
        expect(self.sidebar).to_be_visible()

    # --- Кликабельность ---

    @allure.step("Проверить, что элемент кликабелен")
    def click_visible_button(self, locator):
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        locator.click(trial=True)

    @allure.step("Проверить, что все элементы кликабельны")
    def verify_all_clickable(self, locator):
        count = locator.count()
        logger.debug(f"Проверка кликабельности {count} элементов")
        for i in range(count):
            self.click_visible_button(locator.nth(i))

    @allure.step("Проверить, что все ссылки в боковом меню кликабельны")
    def verify_sidebar_links_are_clickable(self):
        logger.debug("Проверка кликабельности ссылок в боковом меню")
        self.verify_all_clickable(self.sidebar_links)

    # --- Скриншоты ---

    @allure.step("Сохранить скриншот: {name}_{device_label}.png")
    def take_screenshot(self, name: str, device_label: str) -> str:
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        filename = f"{name}_{device_label}.png"
        path = screenshots_dir / filename

        self.page.screenshot(path=str(path), full_page=False)
        logger.info(f"Скриншот сохранён: {path}")

        allure.attach.file(
            str(path),
            name=filename,
            attachment_type=allure.attachment_type.PNG
        )

        return str(path)

    @allure.step("Проверить, что файл скриншота сохранён и не пуст")
    def verify_screenshot_saved(self, path: str):
        logger.debug(f"Проверка наличия и размера скриншота: {path}")
        p = Path(path)
        assert p.exists(), f"Файл скриншота не создан: {path}"
        assert p.stat().st_size > 0, f"Файл скриншота пуст (0 байт): {path}"
