from playwright.sync_api import expect
from config.base import BASE_URL


class BasePage:
    def __init__(self, page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")
        self.burger_menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_button = page.locator("[data-test='logout-sidebar-link']")

    def open(self, url=BASE_URL):
        self.page.goto(url)

    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    def verify_items_count_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    def verify_bucket_is_empty(self):
        expect(self.cart_badge).to_have_count(0)

    def click_burger_menu_button(self):
        self.burger_menu_btn.click()

    def click_logout_button(self):
        self.logout_button.click()
