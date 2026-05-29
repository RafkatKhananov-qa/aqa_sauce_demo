import allure
import pytest

from config.goods import ITEM_NAME, ITEM_PRICE, ITEM_QUANTITY
from config.users import (USERNAME_REQUIRED_MESSAGE, USER1_NAME,
                          USER_PASSWORD, PASSWORD_REQUIRED_MESSAGE)
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Мобильный UX и доступность")
class TestMobileUX:
    @allure.story("Проверка accessibility-атрибутов")
    @allure.title("Поля ввода имеют понятные placeholder")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_001(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_username_input_placeholder()
        login_page.verify_password_input_placeholder()

    @allure.story("Пустой логин → ошибка → Epic sadface: Username is required")
    @allure.title("Ошибки валидации видны и озвучиваются скринридером")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_002(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.click_login()
        login_page.verify_error_message(USERNAME_REQUIRED_MESSAGE)
        login_page.fill_username(USER1_NAME, use_tap=True)
        login_page.click_login()
        login_page.verify_error_message(PASSWORD_REQUIRED_MESSAGE)

    @allure.story("Контраст")
    @allure.title("Контраст текста/фона соответствует WCAG 2.1 AA (≥ 4.5:1)")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_ux_003(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()

        login_page.verify_all_wcag_contrast()

        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)

        inventory_page.verify_all_wcag_contrast()

    @allure.story("Эмуляция keyboard.press(Tab)")
    @allure.title("Навигация с клавиатуры (Tab) работает на мобильных")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_004(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_keyboard_navigation()

    @allure.story("page.go_back() → возврат на предыдущую страницу")
    @allure.title("Возврат по кнопке Назад браузера работает корректно")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_005(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()

        inventory_page.go_to_previous_page()

        login_page.verify_page_loaded()

    @allure.story("Состояние корзины сохраняется при перезагрузке (sessionStorage)")
    @allure.title("Добавить товар → page.reload() → товар в корзине")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_006(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(mobile_page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

        mobile_page.reload()

        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

    @allure.story("Кликабельность элементов")
    @allure.title("Нет 'мёртвых' зон (элементы, на которые нельзя тапнуть)")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_ux_007(self, mobile_page):
        inventory_page = InventoryPage(mobile_page)

        inventory_page.open()
        inventory_page.verify_no_dead_zones()
