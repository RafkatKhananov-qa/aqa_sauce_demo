import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.header = page.locator("//h2[text()='Thank you for your order!']")
        self.message = page.locator("[data-test='complete-text']")
        self.back_home_button = page.locator("#back-to-products")

    def verify_title(self, text):
        expect(self.title).to_have_text(text)

    def verify_header(self):
        expect(self.header).to_be_visible()

    def verify_message(self, text):
        expect(self.message).to_contain_text(text)

    def verify_back_home_button(self):
        expect(self.back_home_button).to_be_enabled()

    def click_back_home_button(self):
        self.back_home_button.click()

    def verify_inventory_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))
