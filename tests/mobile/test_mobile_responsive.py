import allure
import pytest

from config.mobile import (IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT,
                           PIXEL_7_WIDTH, PIXEL_7_HEIGHT,
                           IPHONE_8_LANDSCAPE_WIDTH, IPHONE_8_LANDSCAPE_HEIGHT,
                           MIN_INVENTORY_TITLE_FONT_SIZE, MIN_INVENTORY_ITEM_NAME_FONT_SIZE,
                           MIN_INVENTORY_ITEM_DESCR_FONT_SIZE, MIN_ADD_TO_CART_BUTTON_FONT_SIZE)
from config.users import (USER1_NAME, USER_PASSWORD, CHECKOUT_FIRST_NAME,
                          CHECKOUT_LAST_NAME, CHECKOUT_ZIP)
from pages.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Responsive")
class TestMobileResponsive:

    @allure.story("Correct viewport on iPhone 14 Pro")
    @allure.title("Проверка, что сайт не требует зума/горизонтального скролла")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_resp_01(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_page_does_not_have_horizontal_scroll()
        login_page.verify_viewport_size(IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT)
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

    @allure.story("Correct viewport on Pixel 7")
    @allure.title("Проверка, что сайт не требует зума/горизонтального скролла")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_02(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_viewport_size(PIXEL_7_WIDTH, PIXEL_7_HEIGHT)
        inventory_page.verify_element_font_size_at_least(inventory_page.title, MIN_INVENTORY_TITLE_FONT_SIZE)
        inventory_page.verify_element_font_size_at_least(inventory_page.add_to_cart_button, MIN_ADD_TO_CART_BUTTON_FONT_SIZE)

    @allure.story("Minimum size of tap targets")
    @allure.title("Все интерактивные элементы ≥20×20 px")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_03(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_viewport_size(PIXEL_7_WIDTH, PIXEL_7_HEIGHT)
        inventory_page.verify_element_width_and_height_at_least(inventory_page.add_to_cart_button, 328, 33)
        inventory_page.verify_element_width_and_height_at_least(inventory_page.burger_menu_btn, 20, 20)
        inventory_page.verify_element_width_and_height_at_least(inventory_page.shopping_cart_icon, 40, 40)
        inventory_page.verify_element_width_and_height_at_least(inventory_page.sort_container, 40, 30)

    @allure.story("The fonts are readable without zooming")
    @allure.title("Основной текст ≥14px, заголовки ≥18px")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_04(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_viewport_size(PIXEL_7_WIDTH, PIXEL_7_HEIGHT)
        inventory_page.verify_element_font_size_at_least(inventory_page.title, MIN_INVENTORY_TITLE_FONT_SIZE)
        inventory_page.verify_element_font_size_at_least(inventory_page.inventory_item_name, MIN_INVENTORY_ITEM_NAME_FONT_SIZE)
        inventory_page.verify_element_font_size_at_least(inventory_page.inventory_item_descr, MIN_INVENTORY_ITEM_DESCR_FONT_SIZE)

    @allure.story("Images are scaled correctly")
    @allure.title("Изображения не выходят за пределы контейнера")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_05(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_viewport_size(PIXEL_7_WIDTH, PIXEL_7_HEIGHT)
        inventory_page.verify_all_images_scale_correctly()

    @allure.story("No horizontal scrolling on all pages")
    @allure.title("Страницы с путями /, /inventory, /cart, /checkout-*, "
                  "/complete не имеют горизонтальной прокрутки")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_06(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_page_does_not_have_horizontal_scroll()
        inventory_page.click_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()

        cart_page = CartPage(logged_in_mobile_page)
        cart_page.verify_page_does_not_have_horizontal_scroll()
        cart_page.click_checkout_button()
        cart_page.verify_checkout_step_one()

        checkout_step_one_page = CheckoutStepOnePage(logged_in_mobile_page)
        checkout_step_one_page.verify_page_does_not_have_horizontal_scroll()
        checkout_step_one_page.fill_form(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_ZIP)
        checkout_step_one_page.click_continue_button()
        checkout_step_one_page.verify_checkout_step_two()

        checkout_step_two_page = CheckoutStepTwoPage(logged_in_mobile_page)
        checkout_step_two_page.verify_page_does_not_have_horizontal_scroll()
        checkout_step_two_page.click_finish_button()
        checkout_step_two_page.verify_checkout_complete()

        checkout_complete_page = CheckoutCompletePage(logged_in_mobile_page)
        checkout_complete_page.verify_page_does_not_have_horizontal_scroll()

    @allure.story("Correct display when screen is rotated (landscape)")
    @allure.title("Эмуляция viewport: {width: 667, height: 375}")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "iPhone 8", "browser": "webkit", "landscape": True}
                             ],
                             indirect=True)
    def test_resp_07(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_viewport_size(IPHONE_8_LANDSCAPE_WIDTH, IPHONE_8_LANDSCAPE_HEIGHT)
        inventory_page.verify_all_images_scale_correctly()
        inventory_page.verify_add_to_cart_buttons_are_clickable()

    @allure.story("Responsive menu (hamburger) on mobile devices")
    @allure.title("Меню сворачивается в иконку, раскрывается по тапу")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"}
                             ],
                             indirect=True)
    def test_resp_08(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.verify_sidebar_is_not_visible()
        inventory_page.click_burger_menu_button()
        inventory_page.verify_sidebar_is_visible()
