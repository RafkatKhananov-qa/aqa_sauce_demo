import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")

    def enter_first_name(self, first_name):
        self.first_name.fill(first_name)

    def verify_first_name(self, first_name):
        expect(self.first_name).to_have_value(first_name)

    def enter_last_name(self, last_name):
        self.last_name.fill(last_name)

    def verify_last_name(self, last_name):
        expect(self.last_name).to_have_value(last_name)

    def enter_postal_code(self, postal_code):
        self.postal_code.fill(postal_code)

    def verify_postal_code(self, postal_code):
        expect(self.postal_code).to_have_value(postal_code)

    def click_continue_button(self):
        self.continue_button.click()

    def verify_checkout_step_two(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-two.html"))
