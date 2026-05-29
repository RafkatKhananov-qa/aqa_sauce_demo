from enum import Enum

import allure
from playwright.sync_api import expect

from config.base import CART_URL_PATTERN, INVENTORY_ITEM_URL_PATTERN
from config.goods import ITEM_NAME
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("inventory_page")


class SortOption(Enum):
    PRICE_ASC = 'lohi'
    PRICE_DESC = 'hilo'
    NAME_ASC = 'az'
    NAME_DESC = 'za'


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator("[data-test='title']")
        self.inventory_item = page.locator("//div[@class='inventory_item']")
        self.inventory_item_name = page.locator(".inventory_item_name")
        self.sauce_labs_backpack_item_name = page.get_by_text(ITEM_NAME)
        self.inventory_item_descr = page.locator("[data-test='inventory-item-desc']")
        self.inventory_item_price = page.locator(".inventory_item_price")
        self.add_to_cart_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.add_to_cart_buttons = page.locator("//button[text()='Add to cart']")
        self.add_to_cart_button_details = page.locator("#add-to-cart")
        self.remove_button_details = page.locator("#remove")
        self.inventory_item_image = page.locator("//div[@class='inventory_item'][1]"
                                                 "//img[@class='inventory_item_img']")
        self.inventory_item_images = page.locator("//img[@class='inventory_item_img']")
        self.sort_container = page.locator(".product_sort_container")
        self.remove_button = page.locator("//button[text()='Remove']")
        self.context_menu = page.locator(".context-menu")
        self.img = page.locator("img")

    @allure.step("Проверить, что заголовок виден на странице")
    def verify_title_is_visible(self):
        logger.info("Проверка, что заголовок виден на странице")
        expect(self.title).to_be_visible()

    @allure.step("Получить количество карточек товаров")
    def get_inventory_item_count(self):
        logger.info("Получение количества карточек товаров")
        return self.inventory_item.count()

    @allure.step("Проверить количество карточек товаров")
    def verify_inventory_items_count(self, expected_count):
        actual_count = self.get_inventory_item_count()
        logger.info(f"Проверка количества товаров. Ожидается: {expected_count}, найдено: {actual_count}")
        assert actual_count == expected_count, (
            f"Ожидалось {expected_count} товаров, найдено: {actual_count}"
        )

    @allure.step("Получить названия товаров")
    def get_inventory_item_names(self):
        logger.info("Получение названий товаров")
        return self.inventory_item_name.all_text_contents()

    @allure.step("Получить цены товаров")
    def get_inventory_item_prices(self):
        logger.info("Получение цен товаров")
        return self.inventory_item_price.all_text_contents()

    @allure.step("Проверить изображения товаров")
    def verify_inventory_item_images(self):
        logger.info("Получение изображений товаров")
        images = self.inventory_item_images

        self.page.wait_for_load_state("networkidle")

        results = images.evaluate_all("""
                (imgs) => imgs.map(img => ({
                    src: img.getAttribute("src"),
                    complete: img.complete,
                    width: img.naturalWidth
                }))
            """)

        for img in results:
            logger.debug(f"Изображение: src={img['src']}, complete={img['complete']}, width={img['width']}")
            assert img["src"], "У изображения отсутствует src"
            assert img["width"] > 0, f"Битое изображение: {img['src']}"

    @allure.step("Проверить корректное масштабирование всех изображений")
    def verify_all_images_scale_correctly(self):
        logger.info("Проверка корректного масштабирования всех изображений")
        self.page.wait_for_load_state("networkidle")
        results = self.inventory_item_images.evaluate_all("""
            images => images.map(img => ({
                isLoaded: img.complete,
                fitsContainer: img.scrollWidth <= img.clientWidth
            }))
        """)

        for result in results:
            assert result["isLoaded"], "Одно из изображений не загрузилось"
            assert result["fitsContainer"], \
                "Одно из изображений выходит за пределы контейнера"

    @allure.step("Проверить, что название товара Sauce Labs Backpack видимо")
    def verify_backpack_visible(self):
        logger.info("Проверка, что название товара Sauce Labs Backpack видимо")
        expect(self.sauce_labs_backpack_item_name).to_be_visible()

    @allure.step("Получить цену товара по названию товара")
    def get_item_price(self, item_name: str):
        logger.info("Получение цены товара по названию товара")
        item = self.page.locator(f".inventory_item:has-text('{item_name}')")
        price = item.locator(".inventory_item_price").text_content().strip()
        return price

    @allure.step("Проверить, что цена товара начинается со знака $")
    def verify_item_price_starts_with_dollar(self, item_name: str):
        logger.info("Проверка, что цена товара начинается со знака $")
        price = self.get_item_price(item_name)
        assert price.startswith("$"), f"Цена не начинается с $: {price}"

    @allure.step("Проверить, что все цены отображаются со знаком $")
    def verify_all_prices_have_dollar_sign(self):
        prices = self.get_inventory_item_prices()
        logger.debug(f"Проверка знака $ у {len(prices)} цен")
        for price in prices:
            assert price.startswith("$"), \
                f"Цена '{price}' не начинается со знака $"

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack")
    def click_add_to_cart_button(self):
        logger.debug(f"Клик по кнопке Add to cart")
        self.add_to_cart_button.click()

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack с задержкой")
    def click_add_to_cart_button_with_delay(self):
        logger.debug(f"Клик по кнопке Add to cart для товара Sauce Labs Backpack с задержкой")
        self.add_to_cart_button.click(button="left", delay=1500)

    @allure.step("Кликнуть кнопку 'Add to cart' для товара Sauce Labs Backpack (tap)")
    def tap_add_to_cart_button(self):
        logger.debug("Клик по кнопке 'Add to cart' для товара Sauce Labs Backpack (tap)")
        self.add_to_cart_button.tap()

    @allure.step("Кликнуть кнопку 'Add to cart' в подробной странице товара")
    def click_add_to_cart_button_details(self):
        logger.debug("Клик по кнопке 'Add to cart' в подробной странице товара")
        self.add_to_cart_button_details.click()

    @allure.step("Проверить текст кнопки Remove в подробной странице товара")
    def verify_text_in_remove_button_details(self, text: str):
        logger.info("Проверка текста кнопки Remove в подробной странице товара")
        expect(self.remove_button_details).to_have_text(text)

    @allure.step("Кликнуть кнопку Remove в подробной странице товара")
    def click_remove_button_details(self):
        logger.debug("Клик по кнопке Remove в подробной странице товара")
        self.remove_button_details.click()

    @allure.step("Кликнуть первое изображение товара на странице товаров")
    def click_inventory_item_image(self):
        logger.debug("Клик по первому изображению товара на странице товаров")
        self.inventory_item_image.click()

    def verify_image_does_not_overflow(self):
        logger.info("Проверка, что изображение не вызывает overflow")
        result = self.inventory_item_image.evaluate("""
                el => el.scrollWidth <= el.clientWidth
            """)

        assert result, "Изображение вызывает overflow"

    @allure.step("Отсортировать товары")
    def sort_by(self, option: SortOption):
        logger.info("Сортировка товаров")
        self.sort_container.select_option(value=option.value)

    @allure.step("Проверить, что страница имеет путь /cart.html")
    def verify_cart_page_opened(self):
        logger.info("Проверить, что страница имеет путь /cart.html")
        expect(self.page).to_have_url(CART_URL_PATTERN)

    @allure.step("Проверить, что страница имеет путь /inventory-item.html")
    def verify_inventory_item_page_opened(self):
        logger.info("Проверить, что страница имеет путь /inventory-item.html")
        expect(self.page).to_have_url(INVENTORY_ITEM_URL_PATTERN)

    @allure.step("Кликнуть {count} раз по кнопке Add to cart")
    def click_add_to_cart_button_count_times(self, count):
        logger.debug(f"Клик по кнопке Add to cart {count} раз")
        for _ in range(count):
            self.add_to_cart_button.click()
            self.remove_button.click()
        self.add_to_cart_button.click()

    @allure.step("Кликнуть по кнопке Add to cart по индексам: {indexes}")
    def click_add_to_cart_buttons_by_indexes(self, indexes: list[int]):
        logger.info(f"Кликнуть по кнопке Add to cart по индексам: {indexes}")
        for i in indexes:
            self.add_to_cart_buttons.nth(i).click()

    @allure.step("Проверить, что кнопки Add to cart кликабельны")
    def verify_add_to_cart_buttons_are_clickable(self):
        logger.info("Проверить, что кнопки Add to cart кликабельны")
        self.verify_all_clickable(self.add_to_cart_buttons)

    @allure.step("Проверить, что контекстное меню не появилось")
    def verify_context_menu_is_not_visible(self):
        logger.info("Проверить, что контекстное меню не появилось")
        expect(self.context_menu).not_to_be_visible()

    @allure.step("Проверить прокрутку товаров без залипаний")
    def swipe_goods(self):
        logger.info("Проверить прокрутку товаров без залипаний")
        swipe_x = 300
        swipe_start_y = 1600
        swipe_end_y = 100
        swipe_distance = swipe_start_y - swipe_end_y  # 1500px
        min_expected_scroll = swipe_distance * 0.3
        steps = 20

        before_scroll = self.page.evaluate("window.scrollY")

        cdp = self.page.context.new_cdp_session(self.page)

        cdp.send("Input.dispatchTouchEvent", {
            "type": "touchStart",
            "touchPoints": [{"x": swipe_x, "y": swipe_start_y, "id": 0,
                             "radiusX": 1, "radiusY": 1, "force": 1}]
        })
        for i in range(1, steps + 1):
            y = swipe_start_y - swipe_distance * i / steps
            cdp.send("Input.dispatchTouchEvent", {
                "type": "touchMove",
                "touchPoints": [{"x": swipe_x, "y": y, "id": 0,
                                 "radiusX": 1, "radiusY": 1, "force": 1}]
            })
        cdp.send("Input.dispatchTouchEvent", {
            "type": "touchEnd",
            "touchPoints": []
        })
        cdp.detach()

        self.page.wait_for_timeout(500)

        after_scroll = self.page.evaluate("window.scrollY")
        scroll_delta = after_scroll - before_scroll
        logger.debug(
            f"Свайп: прокрутка {scroll_delta:.0f}px, "
            f"ожидалось минимум {min_expected_scroll:.0f}px"
        )
        assert scroll_delta >= min_expected_scroll, (
            f"Обнаружено залипание: страница прокрутилась на {scroll_delta:.0f}px "
            f"при свайпе {swipe_distance}px (ожидалось минимум {min_expected_scroll:.0f}px)"
        )

    @allure.step("Получить srcset первого изображения на странице")
    def get_first_image_srcset(self):
        logger.info("Получить srcset первого изображения на странице")
        return self.img.first.get_attribute("srcset")

    @allure.step("Проверить мобильный layout инвентаря: карточки вписываются в контейнер и viewport")
    def verify_mobile_inventory_layout(self):
        logger.info("Проверить мобильный layout инвентаря: карточки вписываются в контейнер и viewport")
        viewport_width = self.page.evaluate("() => window.innerWidth")
        results = self.inventory_item.evaluate_all("""
            items => items.map(item => ({
                name: item.querySelector('.inventory_item_name')?.textContent ?? '',
                fitsContainer: item.scrollWidth <= item.clientWidth,
                width: item.getBoundingClientRect().width
            }))
        """)
        for item in results:
            assert item["fitsContainer"], \
                f"Карточка '{item['name']}' вызывает overflow в контейнере"
            assert item["width"] >= viewport_width * 0.7, \
                (f"Карточка '{item['name']}' слишком узкая ({item['width']:.0f}px) "
                 f"для мобильного viewport ({viewport_width}px) — layout не мобильный")

    @allure.step("Проверить, что двойной тап не вызывает зум страницы")
    def verify_double_tap_does_not_zoom(self):
        logger.info("Проверка, что двойной тап не вызывает зум страницы")

        scale_before = self.page.evaluate(
            "() => window.visualViewport.scale"
        )

        self.page.locator("body").tap()
        self.page.locator("body").tap()

        scale_after = self.page.evaluate(
            "() => window.visualViewport.scale"
        )
        logger.debug(f"Масштаб до двойного тапа: {scale_before}, после: {scale_after}")
        assert scale_before == scale_after

    @allure.step("Проверить контраст элементов страницы")
    def verify_all_wcag_contrast(self):
        logger.info("Проверка контраста элементов страницы")

        elements = [
            (".app_logo", "логотип Swag Labs (хедер)"),
            ("[data-test='title']", "заголовок Products"),
            (".inventory_item_name", "название товара"),
            (".inventory_item_price", "цена товара"),
            (".btn_inventory", "кнопка Add to cart")
        ]

        for locator, description in elements:
            self.verify_wcag_contrast(
                locator,
                description
            )
