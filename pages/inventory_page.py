import re
from enum import Enum

import allure
from playwright.sync_api import expect

from config.goods import ITEM_NAME
from pages.base_page import BasePage


class SortOption(Enum):
    PRICE_ASC = 'lohi'
    PRICE_DESC = 'hilo'
    NAME_ASC = 'az'
    NAME_DESC = 'za'


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.inventory_item = page.locator("//div[@class='inventory_item']")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.sauce_labs_backpack_item_name = page.get_by_text(ITEM_NAME)
        self.inventory_item_descr = page.locator("[data-test='inventory-item-desc']")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.add_to_cart_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.add_to_cart_buttons = page.locator("//button[text()='Add to cart']")
        self.add_to_cart_button_details = page.locator("#add-to-cart")
        self.remove_button_details = page.locator("#remove")
        self.inventory_item_image = page.locator("//div[@class='inventory_item'][1]"
                                                 "//img[@class='inventory_item_img']")
        self.inventory_item_images = page.locator("//img[@class='inventory_item_img']")
        self.sort_container = page.locator(".product_sort_container")
        self.remove_button = page.locator("//button[text()='Remove']")
        self.context_menu = page.locator(".context-menu")

    def verify_title_is_visible(self):
        expect(self.title).to_be_visible()

    @allure.step("Получить количество карточек товаров")
    def get_inventory_item_count(self):
        return self.inventory_item.count()

    @allure.step("Проверить количество карточек товаров")
    def verify_inventory_items_count(self, expected_count):
        actual_count = self.get_inventory_item_count()
        assert actual_count == expected_count, (
            f"Ожидалось {expected_count} товаров, найдено: {actual_count}"
        )

    @allure.step("Получить названия товаров")
    def get_inventory_item_names(self):
        return self.inventory_item_name.all_text_contents()

    @allure.step("Получить цены товаров")
    def get_inventory_item_prices(self):
        return self.inventory_item_price.all_text_contents()

    @allure.step("Проверить изображения товаров")
    def verify_inventory_item_images(self):
        images = self.inventory_item_images

        self.page.wait_for_load_state("networkidle")

        results = images.evaluate_all("""
                (imgs) => imgs.map(img => ({
                    src: img.getAttribute("src"),
                    complete: img.complete,
                    width: img.naturalWidth
                }))
            """)

        for img in results:
            print(f"src={img['src']}, complete={img['complete']}, width={img['width']}")
            assert img["src"], "У изображения отсутствует src"
            assert img["width"] > 0, f"Битое изображение: {img['src']}"

    @allure.step("Проверить корректное масштабирование всех изображений")
    def verify_all_images_scale_correctly(self):
        self.page.wait_for_load_state("networkidle")
        results = self.inventory_item_images.evaluate_all("""
            images => images.map(img => ({
                isLoaded: img.complete,
                fitsContainer: img.scrollWidth <= img.clientWidth
            }))
        """)

        for result in results:
            assert result["isLoaded"], "Одно из изображений не загрузилось"
            assert result["fitsContainer"], \
                "Одно из изображений выходит за пределы контейнера"

    @allure.step("Проверить, что название товара Sauce Labs Backpack видимо")
    def verify_backpack_visible(self):
        expect(self.sauce_labs_backpack_item_name).to_be_visible()

    @allure.step("Получить цену товара по названию товара")
    def get_item_price(self, item_name: str):
        item = self.page.locator(f".inventory_item:has-text('{item_name}')")
        price = item.locator(".inventory_item_price").text_content().strip()
        return price

    def verify_item_price_starts_with_dollar(self, item_name: str):
        price = self.get_item_price(item_name)
        assert price.startswith("$"), f"Цена не начинается с $: {price}"

    def verify_inventory_item_price_starts_from_dollar(self):
        assert self.inventory_item_price.startswith("$")

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack")
    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack с задержкой")
    def click_add_to_cart_button_with_delay(self):
        self.add_to_cart_button.click(button="left", delay=1500)

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack (tap)")
    def tap_add_to_cart_button(self):
        self.add_to_cart_button.tap()

    @allure.step("Кликнуть кнопку 'Add to cart' в подробной странице товара")
    def click_add_to_cart_button_details(self):
        self.add_to_cart_button_details.click()

    @allure.step("Проверить текст кнопки Remove в подробной странице товара")
    def verify_text_in_remove_button_details(self, text: str):
        expect(self.remove_button_details).to_have_text(text)

    @allure.step("Кликнуть кнопку Remove в подробной странице товара")
    def click_remove_button_details(self):
        self.remove_button_details.click()

    @allure.step("Кликнуть первое изображение товара на странице товаров")
    def click_inventory_item_image(self):
        self.inventory_item_image.click()

    def verify_image_does_not_overflow(self):
        result = self.inventory_item_image.evaluate("""
                el => el.scrollWidth <= el.clientWidth
            """)

        assert result, "Изображение вызывает overflow"

    @allure.step("Отсортировать товары")
    def sort_by(self, option: SortOption):
        self.sort_container.select_option(value=option.value)

    @allure.step("Проверить, что страница имеет путь /cart.html")
    def verify_cart_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))

    @allure.step("Проверить, что страница имеет путь /inventory-item.html")
    def verify_inventory_item_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory-item.html"))

    @allure.step("Кликнуть {count} раз по кнопке Add to cart")
    def click_add_to_cart_button_count_times(self, count):
        for _ in range(count):
            self.add_to_cart_button.click()
            self.remove_button.click()
        self.add_to_cart_button.click()

    @allure.step("Кликнуть по кнопке Add to cart по индексам: {indexes}")
    def click_add_to_cart_buttons_by_indexes(self, indexes: list[int]):
        for i in indexes:
            self.add_to_cart_buttons.nth(i).click()

    @allure.step("Проверить, что кнопки Add to cart кликабельны")
    def verify_add_to_cart_buttons_are_clickable(self):
        self.verify_all_clickable(self.add_to_cart_buttons)

    @allure.step("Проверить, что контекстное меню не появилось")
    def verify_context_menu_is_not_visible(self):
        expect(self.context_menu).not_to_be_visible()

    @allure.step("Проверить прокрутку товаров без залипаний")
    def swipe_goods(self):
        swipe_x = 300
        swipe_start_y = 1600
        swipe_end_y = 100
        swipe_distance = swipe_start_y - swipe_end_y  # 1500px
        min_expected_scroll = swipe_distance * 0.3
        steps = 20

        before_scroll = self.page.evaluate("window.scrollY")

        cdp = self.page.context.new_cdp_session(self.page)

        cdp.send("Input.dispatchTouchEvent", {
            "type": "touchStart",
            "touchPoints": [{"x": swipe_x, "y": swipe_start_y, "id": 0,
                             "radiusX": 1, "radiusY": 1, "force": 1}]
        })
        for i in range(1, steps + 1):
            y = swipe_start_y - swipe_distance * i / steps
            cdp.send("Input.dispatchTouchEvent", {
                "type": "touchMove",
                "touchPoints": [{"x": swipe_x, "y": y, "id": 0,
                                 "radiusX": 1, "radiusY": 1, "force": 1}]
            })
        cdp.send("Input.dispatchTouchEvent", {
            "type": "touchEnd",
            "touchPoints": []
        })
        cdp.detach()

        self.page.wait_for_timeout(500)

        after_scroll = self.page.evaluate("window.scrollY")
        scroll_delta = after_scroll - before_scroll

        assert scroll_delta >= min_expected_scroll, (
            f"Обнаружено залипание: страница прокрутилась на {scroll_delta:.0f}px "
            f"при свайпе {swipe_distance}px (ожидалось минимум {min_expected_scroll:.0f}px)"
        )

    @allure.step("Проверить, что двойной тап не вызывает зум страницы")
    def verify_double_tap_does_not_zoom(self):
        scale_before = self.page.evaluate(
            "() => window.visualViewport.scale"
        )

        self.page.locator("body").tap()
        self.page.locator("body").tap()

        scale_after = self.page.evaluate(
            "() => window.visualViewport.scale"
        )

        assert scale_before == scale_after
