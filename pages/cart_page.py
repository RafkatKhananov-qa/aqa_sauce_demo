import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_item = page.locator(".cart_item")
        self.cart_quantity = page.locator(".cart_quantity")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.checkout_button = page.locator("#checkout")

    def verify_cart_items_count(self, num):
        expect(self.cart_item).to_have_count(num)

    def verify_cart_quantity(self, num):
        expect(self.cart_quantity).to_have_text(num)

    def verify_inventory_item_name(self, name):
        expect(self.inventory_item_name).to_contain_text(name)

    def get_cart_price(self):
        return self.inventory_item_price.text_content().strip()

    def verify_price(self, expected_price: str):
        actual_price = self.get_cart_price()
        assert actual_price == expected_price, \
            f"Ожидалось {expected_price}, получено {actual_price}"

    def click_checkout_button(self):
        self.checkout_button.click()

    def verify_checkout_step_one(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-one.html"))
