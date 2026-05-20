import allure
import pytest

from config.users import USER1_NAME, USER_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Touch")
class TestMobileTouch:
    @allure.story("Long press does not bring up the system context menu")
    @allure.title("Проверка, что contextmenu не появляется при long_press")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_touch_02(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
        inventory_page = InventoryPage(mobile_page)
        inventory_page.click_add_to_cart_button_with_delay()
        inventory_page.verify_context_menu_is_not_visible()

    @allure.story("Swipe in the inventory page")
    @allure.title("Проверка, что товары прокручиваются без залипаний")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_touch_04(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
        inventory_page = InventoryPage(mobile_page)
        inventory_page.swipe_goods()

    @allure.story("Double tap and zoom")
    @allure.title("Двойной тап не вызывает зум страницы")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_touch_06(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_double_tap_does_not_zoom()

    @allure.story("Elements do not overlap each other")
    @allure.title("Элементы не перекрывают друг друга при тапе")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_touch_08(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
        inventory_page = InventoryPage(mobile_page)
        inventory_page.click_add_to_cart_button()
        inventory_page.verify_badge_does_not_overlap_menu_button()

    @allure.story("Multiple clicks do not increase the amount of goods in bucket")
    @allure.title("Быстрые последовательные тапы не дублируют действия")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_touch_09(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
        inventory_page = InventoryPage(mobile_page)
        inventory_page.click_add_to_cart_button_count_times(3)
        inventory_page.verify_items_count_in_bucket("1")
