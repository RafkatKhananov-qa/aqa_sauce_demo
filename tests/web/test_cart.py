import allure

from config.goods import ITEM_NAME, ITEM_PRICE, ITEM_QUANTITY
from config.users import USER1_NAME, USER_PASSWORD, USER2_NAME

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Cart")
class TestCart:

    @allure.story("Adding items to cart")
    @allure.title("Пользователь может добавить один товар в корзину")
    def test_cart_001(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button()
        inventory_page.verify_items_count_in_bucket("1")

    @allure.story("Adding items to cart")
    @allure.title("Пользователь может добавить несколько товаров в корзину")
    def test_cart_002(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_buttons_by_indexes([0, 1, 2])
        inventory_page.verify_items_count_in_bucket("3")

    @allure.story("Adding items to cart")
    @allure.title("Счётчик корзины не дублируется при повторном добавлении одного товара")
    def test_cart_003(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_add_to_cart_button_count_times(5)
        inventory_page.verify_items_count_in_bucket("1")

    @allure.story("Removing items from cart")
    @allure.title("Пользователь может удалить товар из корзины")
    def test_cart_004(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(page)
        cart_page.click_remove_button()
        cart_page.verify_cart_items_count(0)
        cart_page.verify_bucket_is_empty()

    @allure.story("Cart item details")
    @allure.title("Товар, добавленный через детальную страницу, отображается в корзине корректно")
    def test_cart_006(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_via_detail_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

    @allure.story("Navigation from cart")
    @allure.title("Кнопка Continue Shopping возвращает пользователя на страницу товаров")
    def test_cart_007(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_via_detail_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)
        cart_page.click_continue_shopping_button()
        cart_page.verify_inventory()

    @allure.story("Cart state")
    @allure.title("Корзина пуста при открытии без добавления товаров")
    def test_cart_008(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(page)
        inventory_page.click_shopping_cart_icon()
        inventory_page.verify_cart_page_opened()

        cart_page = CartPage(page)
        cart_page.verify_cart_items_count(0)

    @allure.story("Cart persistence")
    @allure.title("Содержимое корзины сохраняется после перезагрузки страницы")
    def test_cart_009(self, page):
        login_page = LoginPage(page)
        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        cart_page = CartPage.add_item_and_open_cart(page)
        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

        page.reload()

        cart_page.verify_cart_item(ITEM_NAME, ITEM_QUANTITY, ITEM_PRICE)

    @allure.story("Cart persistence")
    @allure.title("Корзина не изолирована между пользователями на одном устройстве")
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
