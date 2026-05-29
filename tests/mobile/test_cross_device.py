import allure
import pytest

from config.goods import ITEM_NAME, ITEM_QUANTITY
from config.mobile import (IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT,
                           MIN_USERNAME_INPUT_HEIGHT_PX, MIN_PASSWORD_INPUT_HEIGHT_PX,
                           MIN_TITLE_FONT_SIZE, MIN_BUTTON_HEIGHT_PX, PIXEL_7_WIDTH,
                           PIXEL_7_HEIGHT, IPAD_MINI_WIDTH, IPAD_MINI_HEIGHT)
from config.users import (USER1_NAME, USER_PASSWORD, CHECKOUT_FIRST_NAME,
                          CHECKOUT_LAST_NAME, CHECKOUT_ZIP, CHECKOUT_COMPLETE_MESSAGE)
from pages.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Cross-Device")
class TestCrossDevice:
    @allure.story("Базовый сценарий покупки")
    @allure.title("Запуск на эмуляции iPhone 14 Pro, Pixel 7, iPad Mini")
    @pytest.mark.parametrize("mobile_page, expected_size",
                             [
                                 ({"device": "iPhone 14 Pro", "browser": "webkit"},
                                  (IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT)),
                                 ({"device": "Pixel 7", "browser": "chromium"},
                                  (PIXEL_7_WIDTH, PIXEL_7_HEIGHT)),
                                 ({"device": "iPad Mini", "browser": "webkit"},
                                  (IPAD_MINI_WIDTH, IPAD_MINI_HEIGHT))
                             ],
                             indirect=["mobile_page"])
    def test_xdev_001(self, mobile_page, expected_size):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_viewport_size(*expected_size)
        login_page.verify_element_height_at_least(
            login_page.username_input,
            MIN_USERNAME_INPUT_HEIGHT_PX
        )
        login_page.verify_element_height_at_least(
            login_page.password_input,
            MIN_PASSWORD_INPUT_HEIGHT_PX
        )
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()
        inventory_page.verify_inventory_items_count(6)
        inventory_page.verify_page_does_not_have_horizontal_scroll()
        inventory_page.verify_backpack_visible()
        inventory_page.verify_image_does_not_overflow()

        inventory_item_price = inventory_page.get_item_price(ITEM_NAME)
        inventory_page.verify_item_price_starts_with_dollar(inventory_item_price)
        inventory_page.tap_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket(ITEM_QUANTITY)
        inventory_page.verify_badge_does_not_overlap_menu_button()
        inventory_page.tap_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()

        cart_page = CartPage(mobile_page)
        cart_page.verify_cart_items_count(1)
        cart_page.verify_price(inventory_item_price)
        cart_page.tap_checkout_button()
        cart_page.verify_checkout_step_one()

        checkout_step_one_page = CheckoutStepOnePage(mobile_page)
        checkout_step_one_page.fill_form(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_ZIP)
        checkout_step_one_page.click_continue_button()
        checkout_step_one_page.verify_checkout_step_two()

        checkout_step_two_page = CheckoutStepTwoPage(mobile_page)
        checkout_step_two_page.verify_cart_items_count(1)
        checkout_step_two_page.verify_inventory_item_name(ITEM_NAME)
        checkout_step_two_page.verify_total_price()
        checkout_step_two_page.click_finish_button()
        checkout_step_two_page.verify_checkout_complete()

        checkout_complete_page = CheckoutCompletePage(mobile_page)
        checkout_complete_page.verify_title(CHECKOUT_COMPLETE_MESSAGE)
        checkout_complete_page.verify_title_font_size(MIN_TITLE_FONT_SIZE)
        checkout_complete_page.verify_back_home_button()
        checkout_complete_page.verify_element_height_at_least(
            checkout_complete_page.back_home_button,
            MIN_BUTTON_HEIGHT_PX
        )

        checkout_complete_page.click_back_home_button()
        checkout_complete_page.verify_inventory_page_opened()
        checkout_complete_page.verify_page_does_not_have_horizontal_scroll()

    @allure.story("Проверка ретина-экранов")
    @allure.title("Проверка отображения при device_scale_factor (2x, 3x)")
    @pytest.mark.parametrize("mobile_page, expected_dpr",
                             [
                                 ({"device": "iPad Mini", "browser": "webkit", "device_scale_factor": 2}, 2),
                                 ({"device": "iPad Mini", "browser": "webkit", "device_scale_factor": 3}, 3),
                             ],
                             indirect=["mobile_page"])
    def test_xdev_002(self, mobile_page, expected_dpr):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_viewport_size(IPAD_MINI_WIDTH, IPAD_MINI_HEIGHT)
        login_page.verify_device_pixel_ratio(expected_dpr)
        login_page.verify_element_height_at_least(
            login_page.username_input,
            MIN_USERNAME_INPUT_HEIGHT_PX
        )
        login_page.verify_element_height_at_least(
            login_page.password_input,
            MIN_PASSWORD_INPUT_HEIGHT_PX
        )
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()
        inventory_page.verify_inventory_items_count(6)
        inventory_page.verify_page_does_not_have_horizontal_scroll()
        inventory_page.verify_backpack_visible()
        inventory_page.verify_image_does_not_overflow()

        inventory_item_price = inventory_page.get_item_price(ITEM_NAME)
        inventory_page.verify_item_price_starts_with_dollar(inventory_item_price)
        inventory_page.tap_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket(ITEM_QUANTITY)
        inventory_page.verify_badge_does_not_overlap_menu_button()
        inventory_page.tap_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()

        cart_page = CartPage(mobile_page)
        cart_page.verify_cart_items_count(1)
        cart_page.verify_price(inventory_item_price)
        cart_page.tap_checkout_button()
        cart_page.verify_checkout_step_one()

        checkout_step_one_page = CheckoutStepOnePage(mobile_page)
        checkout_step_one_page.fill_form(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_ZIP)
        checkout_step_one_page.click_continue_button()
        checkout_step_one_page.verify_checkout_step_two()

        checkout_step_two_page = CheckoutStepTwoPage(mobile_page)
        checkout_step_two_page.verify_cart_items_count(1)
        checkout_step_two_page.verify_inventory_item_name(ITEM_NAME)
        checkout_step_two_page.verify_total_price()
        checkout_step_two_page.click_finish_button()
        checkout_step_two_page.verify_checkout_complete()

        checkout_complete_page = CheckoutCompletePage(mobile_page)
        checkout_complete_page.verify_title(CHECKOUT_COMPLETE_MESSAGE)
        checkout_complete_page.verify_title_font_size(MIN_TITLE_FONT_SIZE)
        checkout_complete_page.verify_back_home_button()
        checkout_complete_page.verify_element_height_at_least(
            checkout_complete_page.back_home_button,
            MIN_BUTTON_HEIGHT_PX
        )

        checkout_complete_page.click_back_home_button()
        checkout_complete_page.verify_inventory_page_opened()
        checkout_complete_page.verify_page_does_not_have_horizontal_scroll()

    @allure.story("Локализация и часовой пояс")
    @allure.title("Проверка отображения при locale=ru-RU, timezone=Europe/Moscow")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium",
                                  "locale": "ru-RU", "timezone_id": "Europe/Moscow"}
                             ],
                             indirect=True)
    def test_xdev_003(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_navigator_language("ru-RU")
        login_page.verify_timezone_offset_hours(3)
        login_page.verify_page_charset_utf8()
        login_page.verify_no_encoding_errors()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_all_prices_have_dollar_sign()
        inventory_page.verify_no_encoding_errors()

    @allure.story("Доступность")
    @allure.title("Эмуляция prefers-reduced-motion: анимации отключены/упрощены, контент доступен")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit",
                                  "reduced_motion": True},
                                 {"device": "Pixel 7", "browser": "chromium",
                                  "reduced_motion": True},
                             ],
                             indirect=True)
    def test_xdev_004(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()

        login_page.verify_prefers_reduced_motion_active()

        login_page.verify_critical_content_visible()
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.verify_login_form_elements_not_hidden_by_animation()

        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()
        inventory_page.verify_inventory_items_count(6)
        inventory_page.verify_page_does_not_have_horizontal_scroll()
        inventory_page.verify_backpack_visible()
        inventory_page.verify_all_prices_have_dollar_sign()
        inventory_page.verify_add_to_cart_buttons_are_clickable()

        inventory_page.verify_burger_menu_accessible_with_reduced_motion()

    @allure.story("User-Agent мобильного браузера")
    @allure.title("Бэкенд получает мобильный UA: ответ содержит мобильные классы и структуру")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_xdev_005(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open_and_verify_request_user_agent_is_mobile()
        login_page.verify_page_loaded()
        login_page.verify_user_agent_is_mobile()
        login_page.verify_response_contains_mobile_viewport()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()
        inventory_page.verify_page_does_not_have_horizontal_scroll()
        inventory_page.verify_response_contains_mobile_nav_classes()
        inventory_page.verify_mobile_navigation_present()
        inventory_page.verify_mobile_inventory_layout()

    @allure.story("Изоляция контекстов")
    @allure.title("Параллельный запуск на 3 устройствах: сессии изолированы, тесты не влияют друг на друга")
    @pytest.mark.parallel
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                                 {"device": "Pixel 7", "browser": "chromium"},
                                 {"device": "iPad Mini", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_xdev_006(self, mobile_page, worker_id):
        allure.dynamic.parameter("worker", worker_id)

        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_no_session_cookie()
        login_page.verify_cart_storage_is_empty()

        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        login_page.verify_session_cookie_exists()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()

        inventory_page.verify_bucket_is_empty()
        inventory_page.verify_cart_storage_is_empty()

        inventory_page.tap_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket(ITEM_QUANTITY)

        inventory_page.verify_cart_storage_count(1)

        inventory_page.click_burger_menu_button()
        inventory_page.verify_sidebar_is_visible()
        inventory_page.click_logout_button()
        login_page.verify_page_loaded()

        login_page.verify_no_session_cookie()
        login_page.verify_cart_storage_count(1)

    @allure.story("Артефакты для отладки")
    @allure.title("Скриншоты с префиксом устройства: TC_010_<step>_<device>.png")
    @pytest.mark.parametrize("mobile_page, device_label",
                             [
                                 ({"device": "iPhone 14 Pro", "browser": "webkit"}, "iPhone14Pro"),
                                 ({"device": "Pixel 7", "browser": "chromium"}, "Pixel7"),
                                 ({"device": "iPad Mini", "browser": "webkit"}, "iPadMini"),
                             ],
                             indirect=["mobile_page"])
    def test_xdev_007(self, mobile_page, device_label):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()

        ss_login = login_page.take_screenshot("TC_010_login", device_label)

        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        inventory_page = InventoryPage(mobile_page)
        inventory_page.verify_title_is_visible()
        inventory_page.verify_inventory_items_count(6)

        ss_inventory = inventory_page.take_screenshot("TC_010_inventory", device_label)

        inventory_page.tap_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket(ITEM_QUANTITY)

        ss_cart = inventory_page.take_screenshot("TC_010_cart", device_label)

        login_page.verify_screenshot_saved(ss_login)
        login_page.verify_screenshot_saved(ss_inventory)
        login_page.verify_screenshot_saved(ss_cart)
