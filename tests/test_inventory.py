from pages.inventory_page import InventoryPage
from config.goods import (goods_expected_names, goods_expected_prices,
                          goods_sort_asc_expected_prices, goods_sort_desc_expected_prices,
                          goods_sort_asc_expected_names)
from config.goods import ITEM_NAME


def test_inv_001(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.get_inventory_item_count()
    inventory_page.verify_inventory_items_count(6)


def test_inv_002(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    goods_names = inventory_page.get_inventory_item_names()

    assert goods_names == goods_expected_names


def test_inv_003(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    goods_prices = inventory_page.get_inventory_item_prices()

    assert goods_prices == goods_expected_prices


def test_inv_004(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.verify_inventory_item_images()


def test_inv_005(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.sort_by_ascending_price()

    goods_prices = inventory_page.get_inventory_item_prices()

    assert goods_prices == goods_sort_asc_expected_prices


def test_inv_006(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.sort_by_descending_price()

    goods_prices = inventory_page.get_inventory_item_prices()

    assert goods_prices == goods_sort_desc_expected_prices


def test_inv_007(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.sort_by_ascending_name()

    goods_names = inventory_page.get_inventory_item_names()

    assert goods_names == goods_sort_asc_expected_names


def test_inv_008(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.click_add_to_cart_button()

    inventory_page.sort_by_descending_price()

    goods_names = inventory_page.get_inventory_item_names()

    assert ITEM_NAME in goods_names


def test_inv_009(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.click_inventory_item_image()

    inventory_page.verify_inventory_item_page_opened()


def test_inv_010(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.click_inventory_item_image()

    inventory_page.click_add_to_cart_button_details()

    inventory_page.verify_text_in_remove_button_details("Remove")

    inventory_page.click_remove_button_details()

    inventory_page.verify_bucket_is_empty()
