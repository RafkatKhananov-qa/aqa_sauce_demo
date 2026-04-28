import re
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.helpers import price_to_float, extract_price
import allure


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

    @allure.step("Проверить количество карточек товаров: {num}")
    def verify_cart_items_count(self, num):
        expect(self.cart_item).to_have_count(num)

    @allure.step("Проверить имя товара")
    def verify_inventory_item_name(self, name):
        expect(self.inventory_item_name).to_contain_text(name)

    @allure.step("Получить цену товара")
    def get_cart_price(self):
        return self.inventory_item_price.text_content().strip()

    @allure.step("Проверить цену первого товара")
    def verify_first_item_price(self, expected_price: str):
        expect(self.inventory_item_price.first).to_have_text(expected_price)

    @allure.step("Проверить текст в Payment Information: {payment_information_text}")
    def verify_payment_information(self, payment_information_text):
        expect(self.payment_information).to_contain_text(payment_information_text)

    @allure.step("Проверить текст в Shipping Information: {shipping_information_text}")
    def verify_shipping_information(self, shipping_information_text):
        expect(self.shipping_information).to_contain_text(shipping_information_text)

    @allure.step("Получить суммарную стоимость товаров")
    def get_item_total_price(self):
        return extract_price(self.inventory_item_total_price.text_content())

    @allure.step("Проверить суммарную стоимость товаров: {expected_price}")
    def verify_item_total_price(self, expected_price: str):
        expect(self.inventory_item_total_price).to_contain_text(expected_price)

    @allure.step("Получить цену налога на товар")
    def get_item_tax_price(self):
        return self.tax_price.text_content().strip()

    @allure.step("Проверить цену налога на товар: {expected_price}")
    def verify_item_tax_price(self, expected_price: str):
        expect(self.tax_price).to_have_text(expected_price)

    @allure.step("Получить итоговую стоимость заказа")
    def get_total_price(self):
        return extract_price(self.total_price.text_content())

    @allure.step("Проверить итоговую стоимость заказа")
    def verify_total_price(self):
        item_price = price_to_float(self.get_item_total_price())
        tax_price = price_to_float(self.get_item_tax_price())
        total_price = price_to_float(self.get_total_price())

        expected_total = round(item_price + tax_price, 2)

        assert total_price == expected_total, \
            f"Ожидалось {expected_total}, получено {total_price}"

    @allure.step("Кликнуть по кнопке Finish")
    def click_finish_button(self):
        self.finish_button.click()

    @allure.step("Проверить, что url страницы содержит путь /checkout-complete.html")
    def verify_checkout_complete(self):
        expect(self.page).to_have_url(re.compile(r".*/checkout-complete.html"))
