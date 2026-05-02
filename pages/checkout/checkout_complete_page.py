import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.header = page.locator("[data-test='complete-header']")
        self.message = page.locator("[data-test='complete-text']")
        self.back_home_button = page.locator("#back-to-products")

    @allure.step("Проверить, что title страницы содержит текст {text}")
    def verify_title(self, text):
        expect(self.title).to_have_text(text)

    @allure.step("Получить размер шрифта title")
    def get_title_font_size(self):
        return self.title.evaluate(
            "el => parseFloat(getComputedStyle(el).fontSize)"
        )

    @allure.step("Проверить заголовок страницы успешного оформления заказа")
    def verify_header(self):
        expect(self.header).to_have_text("Thank you for your order!")

    @allure.step("Проверить, что сообщение на странице содержит текст {text}")
    def verify_message(self, text):
        expect(self.message).to_contain_text(text)

    @allure.step("Проверить, что кнопка Back Home активна")
    def verify_back_home_button(self):
        expect(self.back_home_button).to_be_enabled()

    @allure.step("Кликнуть по кнопке Back Home")
    def click_back_home_button(self):
        self.back_home_button.click()

    @allure.step("Проверить, что url страницы содержит путь /inventory.html")
    def verify_inventory_page_opened(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    @allure.step("Проверить, что размер шрифта title не менее {min_size}px")
    def verify_title_font_size(self, min_size: int):
        actual = self.get_title_font_size()
        assert actual >= min_size, \
            f"Размер шрифта title {actual}px меньше {min_size}px"
