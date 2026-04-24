from config.base import INVENTORY_ITEM_NAME
from config.users import USER1_NAME, USER_PASSWORD
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from utils.artifacts import save_screenshot, save_report
from utils.helpers import verify_price_format
from utils.logger import get_logger


class TestCheckout:

    def test_check_001(self, page):
        results = {
            "test_name": "TC_SAUCE_001",
            "status": "passed",
            "steps": []
        }

        logger = get_logger("TC_SAUCE_001")
        login_page = LoginPage(page)

        login_page.open()
        logger.info("Открыли страницу логина")
        results["steps"].append("Открыли страницу логина")

        login_page.verify_page_loaded()
        logger.info("Страница логина успешно загружена")
        results["steps"].append("Страница логина успешно загружена")

        login_page.fill_username(USER1_NAME)
        login_page.verify_username(USER1_NAME)
        logger.info(f"Ввели логин: {USER1_NAME}")
        results["steps"].append(f"Ввели логин: {USER1_NAME}")

        login_page.fill_password(USER_PASSWORD)
        login_page.verify_password(USER_PASSWORD)
        logger.info("Ввели пароль")
        results["steps"].append("Ввели пароль")

        login_page.click_login()
        login_page.verify_login_success()
        logger.info("Успешно авторизовались")
        results["steps"].append("Успешно авторизовались")

        inventory_page = InventoryPage(page)
        inventory_page.verify_backpack_visible()
        logger.info(f"Товар {INVENTORY_ITEM_NAME} отображается")
        results["steps"].append(f"Товар {INVENTORY_ITEM_NAME} отображается")

        price = inventory_page.get_item_price(INVENTORY_ITEM_NAME)
        verify_price_format(price)
        logger.info(f"Цена товара сохранена: {price}")
        results["steps"].append(f"Цена товара сохранена: {price}")

        inventory_page.click_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket("1")
        logger.info("Товар добавлен в корзину")
        results["steps"].append("Товар добавлен в корзину")

        inventory_page.click_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()
        logger.info("Открыли корзину")
        results["steps"].append("Открыли корзину")

        cart_page = CartPage(page)
        cart_page.verify_cart_items_count(1)
        cart_page.verify_cart_quantity("1")
        cart_page.verify_inventory_item_name(INVENTORY_ITEM_NAME)
        cart_page.verify_price(price)
        logger.info("Проверили товар в корзине")
        results["steps"].append("Проверили товар в корзине")

        cart_page.click_checkout_button()
        cart_page.verify_checkout_step_one()
        logger.info("Открыли Checkout Step One")
        results["steps"].append("Открыли Checkout Step One")

        checkout_step_one_page = CheckoutStepOnePage(page)
        checkout_step_one_page.enter_first_name("Joe")
        checkout_step_one_page.verify_first_name("Joe")

        checkout_step_one_page.enter_last_name("Lowson")
        checkout_step_one_page.verify_last_name("Lowson")

        checkout_step_one_page.enter_postal_code("1234")
        checkout_step_one_page.verify_postal_code("1234")
        logger.info("Заполнили данные покупателя")
        results["steps"].append("Заполнили данные покупателя")

        checkout_step_one_page.click_continue_button()
        checkout_step_one_page.verify_checkout_step_two()
        logger.info("Открыли Checkout Step Two")
        results["steps"].append("Открыли Checkout Step Two")

        checkout_step_two_page = CheckoutStepTwoPage(page)
        checkout_step_two_page.verify_cart_items_count(1)
        checkout_step_two_page.verify_inventory_item_name("Backpack")
        checkout_step_two_page.verify_price(price)
        checkout_step_two_page.verify_payment_information("SauceCard #31337")
        checkout_step_two_page.verify_shipping_information("Pony Express")
        checkout_step_two_page.verify_item_total_price(price)
        checkout_step_two_page.verify_item_tax_price("Tax: $2.40")
        checkout_step_two_page.verify_total_price()
        logger.info("Проверили итоговую информацию заказа")
        results["steps"].append("Проверили итоговую информацию заказа")

        checkout_step_two_page.click_finish_button()
        checkout_step_two_page.verify_checkout_complete()
        logger.info("Нажали Finish")
        results["steps"].append("Нажали Finish")

        checkout_complete_page = CheckoutCompletePage(page)
        checkout_complete_page.verify_title("Checkout: Complete!")
        checkout_complete_page.verify_header()
        checkout_complete_page.verify_message("dispatched")
        checkout_complete_page.verify_back_home_button()
        logger.info("Проверили страницу успешного завершения")
        results["steps"].append("Проверили страницу успешного завершения")

        save_screenshot(page, "TC_SAUCE_001_final.png")
        logger.info("Сохранили финальный скриншот")
        results["steps"].append("Сохранили финальный скриншот")

        checkout_complete_page.click_back_home_button()
        checkout_complete_page.verify_inventory_page_opened()
        logger.info("Вернулись на страницу товаров")
        results["steps"].append("Вернулись на страницу товаров")

        save_report("TC_SAUCE_001", results)
