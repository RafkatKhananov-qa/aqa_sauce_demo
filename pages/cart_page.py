import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class CartPage(BasePage):

    @classmethod
    def add_item_and_open_cart(cls, page):
        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.click_shopping_cart_icon()
        return cls(page)

    @classmethod
    def add_item_via_detail_and_open_cart(cls, page):
        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.click_inventory_item()
        inventory_page.click_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()
        return cls(page)

    def __init__(self, page):
        super().__init__(page)
        self.cart_item = page.locator(".cart_item")
        self.cart_quantity = page.locator(".cart_quantity")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.checkout_button = page.locator("#checkout")
        self.remove_button = page.locator("//button[text()='Remove']")
        self.continue_shopping_button = page.locator("#continue-shopping")

    def verify_cart_items_count(self, num):
        expect(self.cart_item).to_have_count(num)

    def verify_cart_quantity(self, num: str):
        expect(self.cart_quantity).to_have_text(num)

    def verify_inventory_item_name(self, name):
        expect(self.inventory_item_name).to_contain_text(name)

    def get_cart_price(self):
        return self.inventory_item_price.text_content().strip()

    def verify_price(self, expected_price: str):
        expect(self.inventory_item_price.first).to_have_text(expected_price)

    def click_checkout_button(self):
        self.checkout_button.click()

    def click_continue_shopping_button(self):
        self.continue_shopping_button.click()

    def verify_checkout_step_one(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-one.html"))

    def verify_inventory(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    def click_remove_button(self):
        self.remove_button.click()

    def verify_cart_item(self, item_name: str, quantity: str, price: str):
        self.verify_cart_quantity(quantity)
        self.verify_price(price)
        self.verify_cart_items_count(1)
        self.verify_inventory_item_name(item_name)
