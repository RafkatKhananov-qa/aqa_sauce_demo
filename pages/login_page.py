import time

import allure
from playwright.sync_api import expect

from config.base import BASE_URL, CRITICAL_CONTENT_TIMEOUT, INVENTORY_URL_PATTERN
from pages.base_page import BasePage
from utils.logger import get_logger

ERROR_BACKGROUND_CSS = ("background-color", "rgb(226, 35, 26)")

logger = get_logger("login_page")


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
        logger.info("Проверка, что страница имеет url https://www.saucedemo.com")
        expect(self.page).to_have_url(BASE_URL)

    @allure.step("Ввести имя пользователя")
    def fill_username(self, username, use_tap=False):
        if use_tap:
            logger.info(f"Ввод имени пользователя {username} через tap")
            self.username_input.tap()
        else:
            logger.info(f"Ввод имени пользователя {username}")

        self.username_input.fill(username)

    @allure.step("Проверить, что имя пользователя введено в поле")
    def verify_username(self, username):
        logger.info(f"Проверка, что имя пользователя введено в поле")
        expect(self.username_input).to_have_value(username)

    @allure.step("Проверить, что поле 'Имя пользователя' имеет type = text")
    def verify_username_input_type(self):
        logger.info("Проверка, что поле 'Имя пользователя' имеет type = text")
        expect(self.username_input).to_have_attribute("type", "text")

    @allure.step("Проверить, что поле 'Имя пользователя' имеет placeholder=Username")
    def verify_username_input_placeholder(self):
        logger.info("Проверка, что поле 'Имя пользователя' имеет placeholder=Username")
        expect(self.username_input).to_have_attribute("placeholder", "Username")

    @allure.step("Ввести пароль")
    def fill_password(self, password, use_tap=False):
        if use_tap:
            logger.info(f"Ввод пароля {password} через tap")
            self.password_input.tap()
        else:
            logger.info(f"Ввод пароля {password}")
        self.password_input.fill(password)

    @allure.step("Проверить, что пароль введён в поле")
    def verify_password(self, password):
        logger.info(f"Проверка, что пароль введён в поле")
        expect(self.password_input).to_have_value(password)

    @allure.step("Проверить, что поле 'Пароль' имеет type = password")
    def verify_password_input_type(self):
        logger.info("Проверка, что поле 'Пароль' имеет type = password")
        expect(self.password_input).to_have_attribute("type", "password")

    @allure.step("Проверить, что поле 'Пароль' имеет placeholder=Password")
    def verify_password_input_placeholder(self):
        logger.info("Проверка, что поле 'Пароль' имеет placeholder=Password")
        expect(self.password_input).to_have_attribute("placeholder", "Password")

    @allure.step("Кликнуть кнопку логина")
    def click_login(self):
        logger.info("Клик по кнопке логина")
        self.login_button.click()

    @allure.step("Нажать кнопку логина (tap)")
    def tap_login(self):
        logger.info("Клик по кнопке логина (tap)")
        self.login_button.tap()

    @allure.step("Проверить, что страница имеет путь /inventory.html")
    def verify_login_success(self):
        logger.info("Проверка, что страница имеет путь /inventory.html")
        expect(self.page).to_have_url(INVENTORY_URL_PATTERN)

    @allure.step("Авторизоваться")
    def authorize(self, username, password, use_tap=False):
        logger.info(f"Авторизация пользователя {username}")

        self.fill_username(username, use_tap=use_tap)
        self.verify_username(username)

        self.fill_password(password, use_tap=use_tap)
        self.verify_password(password)

        if use_tap:
            self.tap_login()
        else:
            self.click_login()

    @allure.step("Авторизоваться и проверить url главной страницы")
    def login_and_verify(self, username: str, password: str):
        logger.info(f"Авторизация пользователя {username} и проверка url главной страницы")
        self.open()
        self.verify_page_loaded()
        self.authorize(username, password)
        self.verify_login_success()

    @allure.step("Выполнить логин и измерить время загрузки после авторизации (мс)")
    def click_login_and_get_response_time_ms(self):
        start = time.perf_counter()
        logger.info("Начало измерения времени авторизации")
        self.click_login()
        self.verify_login_success()
        end = time.perf_counter()
        response_time_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(f"Авторизация выполнена успешно за {response_time_ms} мс")
        return round((end - start) * 1000, 2)

    @allure.step("Проверить, что сообщение об ошибке имеет текст и цвет")
    def verify_error_message(self, expected_text):
        logger.info("Проверка, что сообщение об ошибке имеет текст и цвет")
        expect(self.error_message).to_be_visible(timeout=3000)
        expect(self.error_message).to_have_text(expected_text)
        expect(self.error_message_container_error).to_have_css(
            *ERROR_BACKGROUND_CSS
        )

    @allure.step("Проверить, что поле ввода логина, пароля, и кнопка логина видны на странице")
    def verify_critical_content_visible(self):
        logger.info("Проверка, что поле ввода логина, пароля, и кнопка логина видны на странице")
        expect(self.username_input).to_be_visible(timeout=CRITICAL_CONTENT_TIMEOUT)
        expect(self.password_input).to_be_visible(timeout=CRITICAL_CONTENT_TIMEOUT)
        expect(self.login_button).to_be_visible(timeout=CRITICAL_CONTENT_TIMEOUT)

    @allure.step("Проверить, что элементы формы входа не скрыты анимацией")
    def verify_login_form_elements_not_hidden_by_animation(self):
        logger.info("Проверка, что элементы формы входа не скрыты анимацией")
        self.verify_element_not_hidden_by_animation(self.username_input)
        self.verify_element_not_hidden_by_animation(self.password_input)
        self.verify_element_not_hidden_by_animation(self.login_button)

    @allure.step("Проверить навигацию через Tab")
    def verify_keyboard_navigation(self):
        logger.info("Проверка навигации через Tab")

        expected_order = [
            self.username_input,
            self.password_input,
            self.login_button
        ]

        for element in expected_order:
            self.page.keyboard.press("Tab")
            expect(element).to_be_focused()

    @allure.step("Проверить контраст элементов страницы")
    def verify_all_wcag_contrast(self):
        logger.info("Проверка контраста элементов страницы")

        elements = [
            ("#login-button", "кнопка Login (текст на зелёном фоне)"),
            (".login_logo", "логотип Swag Labs (страница логина)"),
        ]

        for locator, description in elements:
            self.verify_wcag_contrast(
                locator,
                description
            )
