import re

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("checkout_step_one_page")


class CheckoutStepOnePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.cancel_button = page.locator("#cancel")
        self.error = page.locator("[data-test='error']")

    @allure.step("Заполнить имя, фамилию, почтовый код")
    def fill_form(self, first_name, last_name, postal_code):
        logger.info(f"Заполнение формы checkout: {first_name} {last_name}, {postal_code}")
        self.first_name.fill(first_name)
        self.verify_first_name(first_name)
        self.last_name.fill(last_name)
        self.verify_last_name(last_name)
        self.postal_code.fill(postal_code)
        self.verify_postal_code(postal_code)

    @allure.step("Заполнить имя")
    def enter_first_name(self, first_name: str):
        logger.debug(f"Ввод имени: {first_name}")
        self.first_name.fill(first_name)

    @allure.step("Проверить, что поле с именем заполнено")
    def verify_first_name(self, first_name: str):
        logger.debug(f"Проверка поля имени: {first_name}")
        expect(self.first_name).to_have_value(first_name)

    @allure.step("Заполнить фамилию")
    def enter_last_name(self, last_name: str):
        logger.debug(f"Ввод фамилии: {last_name}")
        self.last_name.fill(last_name)

    @allure.step("Проверить, что поле с фамилией заполнено")
    def verify_last_name(self, last_name: str):
        logger.debug(f"Проверка поля фамилии: {last_name}")
        expect(self.last_name).to_have_value(last_name)

    @allure.step("Заполнить почтовый код")
    def enter_postal_code(self, postal_code):
        logger.debug(f"Ввод почтового кода: {postal_code}")
        self.postal_code.fill(postal_code)

    @allure.step("Проверить, что поле с почтовым кодом заполнено")
    def verify_postal_code(self, postal_code):
        logger.debug(f"Проверка поля почтового кода: {postal_code}")
        expect(self.postal_code).to_have_value(postal_code)

    @allure.step("Кликнуть по кнопке Continue")
    def click_continue_button(self):
        logger.info("Клик по кнопке Continue")
        self.continue_button.click()

    @allure.step("Кликнуть по кнопке Cancel")
    def click_cancel_button(self):
        logger.info("Клик по кнопке Cancel")
        self.cancel_button.click()

    @allure.step("Проверить, что страница имеет путь /checkout-step-two.html")
    def verify_checkout_step_two(self):
        logger.debug("Проверка URL: /checkout-step-two.html")
        expect(self.page).to_have_url(re.compile(r".*/checkout-step-two.html"))

    @allure.step("Проверить, что страница имеет путь /cart.html")
    def verify_cart_page(self):
        logger.debug("Проверка URL: /cart.html")
        expect(self.page).to_have_url(re.compile(r".*/cart.html"))

    @allure.step("Проверить текст ошибки: {text}")
    def verify_text_in_field_is_required_error(self, text: str):
        logger.debug(f"Проверка текста ошибки валидации: '{text}'")
        expect(self.error).to_have_text(text)
