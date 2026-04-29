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
        self.inventory_item = page.locator("//div[@class='inventory_item']")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.sauce_labs_backpack_item_name = page.get_by_text(ITEM_NAME)
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

    @allure.step("Проверить, что название товара Sauce Labs Backpack видимо")
    def verify_backpack_visible(self):
        expect(self.sauce_labs_backpack_item_name).to_be_visible()

    @allure.step("Получить цену товара по названию товара")
    def get_item_price(self, item_name: str):
        item = self.page.locator(f".inventory_item:has-text('{item_name}')")
        price = item.locator(".inventory_item_price").text_content().strip()
        return price

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack")
    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

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
