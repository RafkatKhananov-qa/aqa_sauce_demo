import re
from enum import Enum
from playwright.sync_api import expect

from config.goods import ITEM_NAME
from pages.base_page import BasePage
from utils.helpers import verify_price_format


class SortOption(Enum):
    PRICE_ASC = 'lohi'
    PRICE_DESC = 'hilo'
    NAME_ASC = 'az'
    NAME_DESC = 'za'


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_item = page.get_by_text(ITEM_NAME)
        self.add_to_cart_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.add_to_cart_buttons = page.locator("//button[text()='Add to cart']")
        self.add_to_cart_button_details = page.locator("#add-to-cart")
        self.remove_button_details = page.locator("#remove")
        self.inventory_item_image = page.locator("//div[@class='inventory_item'][1]//img[@class='inventory_item_img']")
        self.sort_container = page.locator(".product_sort_container")
        self.remove_button = page.locator("//button[text()='Remove']")

    def get_inventory_item_count(self):
        return self.page.locator(".inventory_item").count()

    def verify_inventory_items_count(self, expected_count):
        actual_count = self.get_inventory_item_count()
        assert actual_count == expected_count, f"Ожидалось {expected_count} товаров, найдено: {actual_count}"

    def get_inventory_item_names(self):
        return self.page.locator(".inventory_item_name").all_text_contents()

    def get_inventory_item_prices(self):
        return self.page.locator(".inventory_item_price").all_text_contents()

    def verify_inventory_item_images(self):
        images = self.page.locator("//img[@class='inventory_item_img']")

        results = images.evaluate_all("""
                (imgs) => imgs.map(img => ({
                    src: img.getAttribute("src"),
                    complete: img.complete,
                    width: img.naturalWidth
                }))
            """)

        for img in results:
            assert img["src"], "У изображения отсутствует src"
            assert img["width"] > 0, f"Битое изображение: {img['src']}"

    def verify_backpack_visible(self):
        expect(self.inventory_item).to_be_visible()

    def get_item_price(self, item_name: str):
        item = self.page.locator(f".inventory_item:has-text('{item_name}')")
        price = item.locator(".inventory_item_price").text_content().strip()
        return price

    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    def click_add_to_cart_button_details(self):
        self.add_to_cart_button_details.click()

    def verify_text_in_remove_button_details(self, text: str):
        expect(self.remove_button_details).to_have_text(text)

    def click_remove_button_details(self):
        self.remove_button_details.click()

    def click_inventory_item_image(self):
        self.inventory_item_image.click()

    def sort_by(self, option: SortOption):
        self.sort_container.select_option(value=option.value)

    def verify_cart_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))

    def verify_inventory_item_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory-item.html"))

    def click_add_to_cart_button_count_times(self, count):
        for _ in range(count):
            self.add_to_cart_button.click()
            self.remove_button.click()
        self.add_to_cart_button.click()

    def click_add_to_cart_buttons_by_indexes(self, indexes: list[int]):
        for i in indexes:
            self.add_to_cart_buttons.nth(i).click()

    def click_inventory_item(self):
        self.inventory_item.click()
