import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
import allure


class CartPage(BasePage):

    @classmethod
    @allure.step("Добавить товар в корзину и открыть корзину")
    def add_item_and_open_cart(cls, page):
        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.click_shopping_cart_icon()
        return cls(page)

    @classmethod
    @allure.step("Добавить товар через детальную страницу и открыть корзину")
    def add_item_via_detail_and_open_cart(cls, page):
        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
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

    @allure.step("Проверить количество карточек товаров на странице: {num}")
    def verify_cart_items_count(self, num):
        expect(self.cart_item).to_have_count(num)

    @allure.step("Проверить количество товаров в карточке товара")
    def verify_cart_quantity(self, num: str):
        expect(self.cart_quantity).to_have_text(num)

    @allure.step("Проверить название товара")
    def verify_inventory_item_name(self, name):
        expect(self.inventory_item_name).to_contain_text(name)

    @allure.step("Получить цену товара")
    def get_cart_price(self):
        return self.inventory_item_price.text_content().strip()

    @allure.step("Проверить цену первого товара")
    def verify_price(self, expected_price: str):
        expect(self.inventory_item_price.first).to_have_text(expected_price)

    @allure.step("Кликнуть по кнопке Checkout")
    def click_checkout_button(self):
        self.checkout_button.click()

    @allure.step("Кликнуть по кнопке Continue Shopping")
    def click_continue_shopping_button(self):
        self.continue_shopping_button.click()

    @allure.step("Проверить, что url страницы содержит /checkout-step-one.html")
    def verify_checkout_step_one(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-one.html"))

    @allure.step("Проверить, что url страницы содержит /inventory.html")
    def verify_inventory(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    @allure.step("Кликнуть по кнопке Remove у товара")
    def click_remove_button(self):
        self.remove_button.click()

    @allure.step("Проверить название товара, количество товара, цену товара")
    def verify_cart_item(self, item_name: str, quantity: str, price: str):
        self.verify_cart_quantity(quantity)
        self.verify_price(price)
        self.verify_cart_items_count(1)
        self.verify_inventory_item_name(item_name)
