import re
from playwright.sync_api import expect

from config.goods import ITEM_NAME
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_item = page.get_by_text(ITEM_NAME)
        self.add_to_cart_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.add_to_cart_button_details = page.locator("#add-to-cart")
        self.remove_button_details = page.locator("#remove")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")
        self.inventory_item_image = page.locator("//div[@class='inventory_item'][1]//img[@class='inventory_item_img']")

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

    def verify_price_format(self, price: str):
        assert price.startswith("$"), f"Цена не в формате $, получено: {price}"

    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    def click_add_to_cart_button_details(self):
        self.add_to_cart_button_details.click()

    def verify_text_in_remove_button_details(self, text: str):
        expect(self.remove_button_details).to_have_text(text)

    def click_remove_button_details(self):
        self.remove_button_details.click()

    def verify_items_count_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    def verify_bucket_is_empty(self):
        expect(self.page.locator(".shopping_cart_badge")).to_have_count(0)

    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    def click_inventory_item_image(self):
        self.inventory_item_image.click()

    def sort_by_ascending_price(self):
        self.page.locator(".product_sort_container").select_option(value='lohi')

    def sort_by_descending_price(self):
        self.page.locator(".product_sort_container").select_option(value='hilo')

    def sort_by_ascending_name(self):
        self.page.locator(".product_sort_container").select_option(value='az')

    def verify_cart_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))

    def verify_inventory_item_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory-item.html"))
