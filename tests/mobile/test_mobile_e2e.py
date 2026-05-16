import allure
import pytest

from config.goods import ITEM_NAME, ITEM_QUANTITY
from config.mobile import (IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT, MIN_TITLE_FONT_SIZE,
                           MIN_USERNAME_INPUT_HEIGHT_PX, MIN_PASSWORD_INPUT_HEIGHT_PX,
                           MIN_BUTTON_HEIGHT_PX)
from config.users import (USER1_NAME, USER_PASSWORD, CHECKOUT_FIRST_NAME,
                          CHECKOUT_LAST_NAME, CHECKOUT_ZIP, CHECKOUT_COMPLETE_MESSAGE)
from pages.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

from utils.artifacts import save_screenshot, save_report
from utils.helpers import log_step
from utils.logger import get_logger


@allure.feature("E2E checkout flow")
class TestMobile:
    @allure.story("Полный цикл заказа на мобильном устройстве")
    @allure.title("Mobile E2E: login → add to cart → checkout")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 14 Pro", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_mobile_e2e(self, mobile_page):
        results = {
            "test_name": "TC_MOBILE_001",
            "status": "passed",
            "steps": []
        }
        logger = get_logger("TC_MOBILE_001")

        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_viewport_size(IPHONE_14_PRO_WIDTH, IPHONE_14_PRO_HEIGHT)
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
        log_step(logger, results, "Успешно авторизовались")

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
        log_step(logger, results, f"Товар добавлен в корзину, цена: {inventory_item_price}")

        cart_page = CartPage(mobile_page)
        cart_page.verify_cart_items_count(1)
        cart_page.verify_price(inventory_item_price)
        cart_page.tap_checkout_button()
        cart_page.verify_checkout_step_one()
        log_step(logger, results, "Проверили товар в корзине, открыли Checkout Step One")

        checkout_step_one_page = CheckoutStepOnePage(mobile_page)
        checkout_step_one_page.fill_form(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_ZIP)
        checkout_step_one_page.click_continue_button()
        checkout_step_one_page.verify_checkout_step_two()
        log_step(logger, results, "Заполнили данные покупателя")

        checkout_step_two_page = CheckoutStepTwoPage(mobile_page)
        checkout_step_two_page.verify_cart_items_count(1)
        checkout_step_two_page.verify_inventory_item_name(ITEM_NAME)
        checkout_step_two_page.verify_total_price()
        checkout_step_two_page.click_finish_button()
        checkout_step_two_page.verify_checkout_complete()
        log_step(logger, results, "Проверили итоговую информацию заказа и нажали Finish")

        checkout_complete_page = CheckoutCompletePage(mobile_page)
        checkout_complete_page.verify_title(CHECKOUT_COMPLETE_MESSAGE)
        checkout_complete_page.verify_title_font_size(MIN_TITLE_FONT_SIZE)
        checkout_complete_page.verify_back_home_button()
        checkout_complete_page.verify_element_height_at_least(
            checkout_complete_page.back_home_button,
            MIN_BUTTON_HEIGHT_PX
        )
        log_step(logger, results, "Проверили страницу успешного завершения")

        save_screenshot(mobile_page, "TC_MOBILE_001_final.png")
        log_step(logger, results, "Сохранили финальный скриншот")

        checkout_complete_page.click_back_home_button()
        checkout_complete_page.verify_inventory_page_opened()
        checkout_complete_page.verify_page_does_not_have_horizontal_scroll()
        log_step(logger, results, "Вернулись на страницу товаров")

        save_report("TC_MOBILE_001", results)
