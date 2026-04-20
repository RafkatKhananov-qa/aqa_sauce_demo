import re
from pages.base_page import BasePage
from config.base import BASE_URL
from playwright.sync_api import expect


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def open(self):
        super().open(BASE_URL)

    def verify_page_loaded(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/")

    def enter_username(self, username):
        self.username_input.fill(username)

    def verify_username(self, username):
        expect(self.username_input).to_have_value(username)

    def enter_password(self, password):
        self.password_input.fill(password)

    def verify_password(self, password):
        expect(self.password_input).to_have_value(password)

    def click_login(self):
        self.login_button.click()

    def verify_login_success(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    def verify_error_message(self, expected_text):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(expected_text)
