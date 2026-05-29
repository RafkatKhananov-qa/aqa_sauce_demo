import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from utils.logger import get_logger

logger = get_logger("cart_page")


class CartPage(BasePage):

    @classmethod
    @allure.step("Добавить товар в корзину и открыть корзину")
    def add_item_and_open_cart(cls, page):
        logger.info("Добавление товара в корзину и открытие корзины")
        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.click_shopping_cart_icon()
        return cls(page)

    @classmethod
    @allure.step("Добавить товар через детальную страницу и открыть корзину")
    def add_item_via_detail_and_open_cart(cls, page):
        logger.info("Добавление товара через детальную страницу и открытие корзины")
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
        logger.debug(f"Проверка количества товаров в корзине: {num}")
        expect(self.cart_item).to_have_count(num)

    @allure.step("Проверить количество товаров в карточке товара")
    def verify_cart_quantity(self, num: str):
        logger.debug(f"Проверка количества в карточке товара: {num}")
        expect(self.cart_quantity).to_have_text(num)

    @allure.step("Проверить название товара")
    def verify_inventory_item_name(self, name):
        logger.debug(f"Проверка названия товара: {name}")
        expect(self.inventory_item_name).to_contain_text(name)

    @allure.step("Получить цену товара")
    def get_cart_price(self):
        price = self.inventory_item_price.text_content().strip()
        logger.debug(f"Цена товара в корзине: {price}")
        return price

    @allure.step("Проверить цену первого товара")
    def verify_price(self, expected_price: str):
        logger.debug(f"Проверка цены первого товара: {expected_price}")
        expect(self.inventory_item_price.first).to_have_text(expected_price)

    @allure.step("Кликнуть по кнопке Checkout")
    def click_checkout_button(self):
        logger.info("Клик по кнопке Checkout")
        self.checkout_button.click()

    @allure.step("Нажать на кнопку Checkout (tap)")
    def tap_checkout_button(self):
        logger.info("Tap по кнопке Checkout")
        self.checkout_button.tap()

    @allure.step("Кликнуть по кнопке Continue Shopping")
    def click_continue_shopping_button(self):
        logger.info("Клик по кнопке Continue Shopping")
        self.continue_shopping_button.click()

    @allure.step("Проверить, что url страницы содержит /checkout-step-one.html")
    def verify_checkout_step_one(self):
        logger.debug("Проверка URL: /checkout-step-one.html")
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-one.html"))

    @allure.step("Проверить, что url страницы содержит /inventory.html")
    def verify_inventory(self):
        logger.debug("Проверка URL: /inventory.html")
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    @allure.step("Кликнуть по кнопке Remove у товара")
    def click_remove_button(self):
        logger.info("Клик по кнопке Remove у товара")
        self.remove_button.click()

    @allure.step("Проверить название товара, количество товара, цену товара")
    def verify_cart_item(self, item_name: str, quantity: str, price: str):
        logger.info(
            f"Проверка товара в корзине: {item_name}, "
            f"количество: {quantity}, цена: {price}"
        )
        self.verify_cart_quantity(quantity)
        self.verify_price(price)
        self.verify_cart_items_count(1)
        self.verify_inventory_item_name(item_name)
