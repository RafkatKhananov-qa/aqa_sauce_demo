import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_item = page.get_by_text("Sauce Labs Backpack")
        self.add_to_cart_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")

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

    def verify_items_count_in_bucket(self, num):
        expect(self.cart_badge).to_have_text(num)

    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    def verify_cart_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))
