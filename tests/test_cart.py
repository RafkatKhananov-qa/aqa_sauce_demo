from config.goods import ITEM_NAME, ITEM_PRICE, ITEM_QUANTITY
from config.users import USER1_NAME, USER_PASSWORD, USER2_NAME
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCart:

    def test_cart_001(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket("1")

    def test_cart_002(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_buttons_by_indexes([0, 1, 2])
        inventory_page.verify_items_count_in_bucket("3")

    def test_cart_003(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button_count_times(5)
        inventory_page.verify_items_count_in_bucket("1")

    def test_cart_004(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(page)
        cart_page.click_remove_button()
        cart_page.verify_cart_items_count(0)
        cart_page.verify_bucket_is_empty()

    def test_cart_006(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_via_detail_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

    def test_cart_007(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_via_detail_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)
        cart_page.click_continue_shopping_button()
        cart_page.verify_inventory()

    def test_cart_008(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()

        cart_page = CartPage(page)
        cart_page.verify_cart_items_count(0)

    def test_cart_009(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

        page.reload()

        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

    def test_cart_010(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

        inventory_page = InventoryPage(page)
        inventory_page.click_burger_menu_button()
        inventory_page.click_logout_button()

        login_page = LoginPage(page)
        login_page.login_and_verify(USER2_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_shopping_cart_icon()

        cart_page = CartPage(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)
