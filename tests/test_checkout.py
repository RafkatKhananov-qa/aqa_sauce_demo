from config.base import CHECKOUT_STEP_ONE_URL, INVENTORY_ITEM_NAME
from pages.cart_page import CartPage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage


def test_check_002(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.enter_last_name("Ivanov")
    checkout_step_one_page.enter_postal_code("45679")
    checkout_step_one_page.click_continue_button()
    checkout_step_one_page.verify_text_in_field_is_required_error("Error: First Name is required")


def test_check_003(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.enter_first_name("Ivan")
    checkout_step_one_page.enter_postal_code("45679")
    checkout_step_one_page.click_continue_button()
    checkout_step_one_page.verify_text_in_field_is_required_error("Error: Last Name is required")


def test_check_004(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.enter_first_name("Ivan")
    checkout_step_one_page.enter_last_name("Ivanov")
    checkout_step_one_page.click_continue_button()
    checkout_step_one_page.verify_text_in_field_is_required_error("Error: Postal Code is required")


def test_check_005(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.fill_form("Ivanov", "Ivanov", "sddgfdg")
    checkout_step_one_page.click_continue_button()
    checkout_step_one_page.verify_checkout_step_two()


def test_check_006(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.fill_form("Ivanov", "Ivanov", "435468")
    checkout_step_one_page.click_cancel_button()
    checkout_step_one_page.verify_cart_page()


def test_check_007(logged_in_page):
    logged_in_page.goto(CHECKOUT_STEP_ONE_URL)
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.fill_form("Ivanov", "Ivanov", "435468")
    checkout_step_one_page.click_cancel_button()
    checkout_step_one_page.verify_cart_page()
    cart_page = CartPage(logged_in_page)
    cart_page.click_continue_shopping_button()
    cart_page.verify_inventory()


def test_check_008(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.click_add_to_cart_button()
    inventory_page.click_shopping_cart_icon()
    cart_page = CartPage(logged_in_page)
    cart_page.verify_cart_quantity("1")
    cart_page.verify_inventory_item_name(INVENTORY_ITEM_NAME)
    cart_page.click_checkout_button()
    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.fill_form("Ivanov", "Ivanov", "435468")
    checkout_step_one_page.click_continue_button()

    checkout_step_two_page = CheckoutStepTwoPage(logged_in_page)
    checkout_step_two_page.verify_cart_items_count(1)
    checkout_step_two_page.verify_total_price()


def test_check_010(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.click_add_to_cart_buttons_by_indexes([0, 1])
    inventory_page.click_shopping_cart_icon()

    cart_page = CartPage(logged_in_page)
    cart_page.verify_cart_items_count(2)
    cart_page.click_checkout_button()
    cart_page.verify_checkout_step_one()

    checkout_step_one_page = CheckoutStepOnePage(logged_in_page)
    checkout_step_one_page.fill_form("Ivanov", "Ivanov", "435468")
    checkout_step_one_page.click_continue_button()
    checkout_step_one_page.verify_checkout_step_two()

    checkout_step_two_page = CheckoutStepTwoPage(logged_in_page)
    checkout_step_two_page.verify_cart_items_count(2)
    checkout_step_two_page.verify_total_price()
