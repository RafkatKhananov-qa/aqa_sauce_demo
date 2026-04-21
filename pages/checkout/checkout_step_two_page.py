import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.helpers import price_to_float, extract_price


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_item = page.locator(".cart_item")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.payment_information = page.locator("[data-test='payment-info-value']")
        self.shipping_information = page.locator("[data-test='shipping-info-value']")
        self.inventory_item_total_price = page.locator("[data-test='subtotal-label']")
        self.tax_price = page.locator("[data-test='tax-label']")
        self.total_price = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")

    def verify_cart_items_count(self, num):
        expect(self.cart_item).to_have_count(num)

    def verify_inventory_item_name(self, name):
        expect(self.inventory_item_name).to_contain_text(name)

    def get_cart_price(self):
        return self.inventory_item_price.text_content().strip()

    def verify_price(self, expected_price: str):
        actual_price = self.get_cart_price()
        assert actual_price == expected_price, \
            f"Ожидалось {expected_price}, получено {actual_price}"

    def verify_payment_information(self, payment_information_text):
        expect(self.payment_information).to_contain_text(payment_information_text)

    def verify_shipping_information(self, shipping_information_text):
        expect(self.shipping_information).to_contain_text(shipping_information_text)

    def get_item_total_price(self):
        return extract_price(self.inventory_item_total_price.text_content())

    def verify_item_total_price(self, expected_price: str):
        actual_price = self.get_item_total_price()
        assert actual_price == expected_price, \
            f"Ожидалось {expected_price}, получено {actual_price}"

    def get_item_tax_price(self):
        return self.tax_price.text_content().strip()

    def verify_item_tax_price(self, expected_price: str):
        actual_price = self.get_item_tax_price()
        assert actual_price == expected_price, \
            f"Ожидалось {expected_price}, получено {actual_price}"

    def get_total_price(self):
        return extract_price(self.total_price.text_content())

    def verify_total_price(self):
        item_price = price_to_float(self.get_item_total_price())
        tax_price = price_to_float(self.get_item_tax_price())
        total_price = price_to_float(self.get_total_price())

        expected_total = round(item_price + tax_price, 2)

        assert total_price == expected_total, \
            f"Ожидалось {expected_total}, получено {total_price}"

    def click_finish_button(self):
        self.finish_button.click()

    def verify_checkout_complete(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-complete.html"))
