import allure

from config.goods import (
    GOODS_EXPECTED_NAMES,
    GOODS_EXPECTED_PRICES,
    GOODS_SORT_ASC_EXPECTED_PRICES,
    GOODS_SORT_DESC_EXPECTED_PRICES,
    GOODS_SORT_ASC_EXPECTED_NAMES,
    ITEM_NAME,
)

from pages.inventory_page import InventoryPage, SortOption


@allure.feature("Inventory")
class TestInventory:
    @allure.story("Verifying inventory items count on the main page")
    @allure.title("На странице товаров отображается 6 товаров")
    def test_inv_001(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.verify_inventory_items_count(6)

    @allure.story("Verifying inventory items names on the main page")
    @allure.title("На странице товаров отображаются товары "
                  "с определенными названиями")
    def test_inv_002(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        goods_names = inventory_page.get_inventory_item_names()
        assert goods_names == GOODS_EXPECTED_NAMES

    @allure.story("Verifying inventory items prices on the main page")
    @allure.title("На странице товаров отображаются товары "
                  "с определенными ценами")
    def test_inv_003(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        goods_prices = inventory_page.get_inventory_item_prices()
        assert goods_prices == GOODS_EXPECTED_PRICES

    @allure.story("Verifying inventory items images on the main page")
    @allure.title("На странице товаров отображаются товары "
                  "с валидными изображениями")
    def test_inv_004(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.verify_inventory_item_images()

    @allure.story("Verifying inventory items sorting by price in ascending order")
    @allure.title("При сортировке товаров по возрастанию цены "
                  "товары располагаются от меньшей к большей цене")
    def test_inv_005(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.sort_by(SortOption.PRICE_ASC)
        goods_prices = inventory_page.get_inventory_item_prices()
        assert goods_prices == GOODS_SORT_ASC_EXPECTED_PRICES

    @allure.story("Verifying inventory items sorting by price in descending order")
    @allure.title("При сортировке товаров по убыванию цены "
                  "товары располагаются от большей к меньшей цене")
    def test_inv_006(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.sort_by(SortOption.PRICE_DESC)
        goods_prices = inventory_page.get_inventory_item_prices()
        assert goods_prices == GOODS_SORT_DESC_EXPECTED_PRICES

    @allure.story("Verifying inventory items sorting by name in ascending order")
    @allure.title("При сортировке товаров по имени "
                  "товары сортируются по алфавиту")
    def test_inv_007(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.sort_by(SortOption.NAME_ASC)
        goods_names = inventory_page.get_inventory_item_names()
        assert goods_names == GOODS_SORT_ASC_EXPECTED_NAMES

    @allure.story("Verifying inventory items sorting after adding item to cart")
    @allure.title("После добавления товара в корзину "
                  "сортировка по убыванию цены работает корректно")
    def test_inv_008(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.click_add_to_cart_button()
        inventory_page.sort_by(SortOption.PRICE_DESC)
        goods_names = inventory_page.get_inventory_item_names()
        assert ITEM_NAME in goods_names

    @allure.story("Verifying inventory item page opened after clicking inventory image")
    @allure.title("При клике по изображению товара "
                  "открывается подробная страница товара")
    def test_inv_009(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.click_inventory_item_image()
        inventory_page.verify_inventory_item_page_opened()

    @allure.story("Removing item from cart on item detail page")
    @allure.title("После удаления товара через кнопку "
                  "Remove на детальной странице корзина пуста")
    def test_inv_010(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.click_inventory_item_image()
        inventory_page.click_add_to_cart_button_details()
        inventory_page.verify_text_in_remove_button_details("Remove")
        inventory_page.click_remove_button_details()
        inventory_page.verify_bucket_is_empty()
