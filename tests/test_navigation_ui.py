import allure
import pytest

from pages.inventory_page import InventoryPage


@allure.feature("Navigation UI")
class TestNavigation:
    @allure.story("Burger menu links are clickable and sidebar can be closed")
    @allure.title("Все ссылки в бургер-меню кликабельны, меню закрывается")
    def test_ui_002(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.click_burger_menu_button()
        inventory_page.verify_sidebar_links_are_clickable()
        inventory_page.click_close_sidebar_button()
        inventory_page.verify_sidebar_is_not_visible()

    @allure.story("Add to cart buttons are clickable")
    @allure.title("Кнопки Add to cart кликабельны "
                  "на десктопе и мобильном устройстве")
    @pytest.mark.parametrize("viewport", [
        pytest.param({"width": 375, "height": 812}, id="mobile"),
        pytest.param(None, id="desktop"),
    ])
    def test_ui_003_006(self, logged_in_page, viewport):
        if viewport:
            logged_in_page.set_viewport_size(viewport)
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.verify_add_to_cart_buttons_are_clickable()
