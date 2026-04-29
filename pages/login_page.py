import re
import time

import allure
from playwright.sync_api import expect

from config.base import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
        self.error_message_container_error = page.locator(".error-message-container.error")

    @allure.step("Проверить, что страница имеет url https://www.saucedemo.com")
    def verify_page_loaded(self):
        expect(self.page).to_have_url(BASE_URL)

    @allure.step("Ввести имя пользователя")
    def fill_username(self, username):
        self.username_input.fill(username)

    @allure.step("Проверить, что имя пользователя введено в поле")
    def verify_username(self, username):
        expect(self.username_input).to_have_value(username)

    @allure.step("Ввести пароль")
    def fill_password(self, password):
        self.password_input.fill(password)

    @allure.step("Проверить, что пароль введён в поле")
    def verify_password(self, password):
        expect(self.password_input).to_have_value(password)

    @allure.step("Кликнуть кнопку логина")
    def click_login(self):
        self.login_button.click()

    @allure.step("Проверить, что страница имеет путь /inventory.html")
    def verify_login_success(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory.html"))

    @allure.step("Авторизоваться")
    def authorize(self, username, password):
        self.fill_username(username)
        self.verify_username(username)
        self.fill_password(password)
        self.verify_password(password)
        self.click_login()

    @allure.step("Авторизоваться и проверить url главной страницы")
    def login_and_verify(self, username: str, password: str):
        self.open()
        self.verify_page_loaded()
        self.authorize(username, password)
        self.verify_login_success()

    @allure.step("Выполнить логин и измерить время загрузки после авторизации (мс)")
    def click_login_and_get_response_time_ms(self):
        start = time.perf_counter()
        self.click_login()
        self.verify_login_success()
        end = time.perf_counter()
        return round((end - start) * 1000, 2)

    @allure.step("Проверить, что сообщение об ошибке имеет текст и цвет")
    def verify_error_message(self, expected_text):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(expected_text)
        expect(self.error_message_container_error).to_have_css(
            "background-color", "rgb(226, 35, 26)"
        )
