import allure
from playwright.sync_api import expect

from config.base import BASE_URL


class BasePage:
    def __init__(self, page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_icon = page.locator(".shopping_cart_link")
        self.burger_menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_button = page.locator("[data-test='logout-sidebar-link']")
        self.sidebar_links = page.locator("//nav[@class='bm-item-list']/a")
        self.close_sidebar_button = page.locator("#react-burger-cross-btn")
        self.sidebar = page.locator(".bm-menu")

    @allure.step("Открыть страницу входа на сайт Swag Labs")
    def open(self, url=BASE_URL):
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Эмулировать сеть 3G")
    def emulate_3g(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": 375 * 1024 / 8,
            "uploadThroughput": 750 * 1024 / 8,
            "latency": 100
        })

    @allure.step("Эмулировать потерю сети")
    def emulate_offline(self):
        self.page.route(
            "**/*",
            lambda route: route.abort()
        )

    @allure.step("Принудительная сборка мусора")
    def force_gc(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("HeapProfiler.enable")
        cdp.send("HeapProfiler.collectGarbage")
        cdp.detach()

    @allure.step("Получить размер используемой JS-памяти")
    def get_memory_usage_bytes(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Performance.enable")
        metrics = cdp.send("Performance.getMetrics")
        return next(
            m["value"] for m in metrics["metrics"]
            if m["name"] == "JSHeapUsedSize"
        )

    @allure.step("Получить First Contentful Paint в миллисекундах")
    def get_fcp_ms(self):
        return self.page.evaluate("""
            () => new Promise((resolve) => {
                const existing = performance.getEntriesByName(
                    'first-contentful-paint'
                );
                if (existing.length > 0) {
                    resolve(existing[0].startTime);
                    return;
                }
                const observer = new PerformanceObserver((list) => {
                    const entry = list.getEntriesByName(
                        'first-contentful-paint'
                    )[0];
                    if (entry) {
                        observer.disconnect();
                        resolve(entry.startTime);
                    }
                });
                observer.observe({ type: 'paint', buffered: true });
                setTimeout(() => { observer.disconnect(); resolve(null); }, 5000);
            })
        """)

    @allure.step("Включить отслеживание CLS")
    def setup_cls_tracking(self):
        self.page.add_init_script("""
            window.clsValue = 0;
            new PerformanceObserver((entryList) => {
                for (const entry of entryList.getEntries()) {
                    if (!entry.hadRecentInput) {
                        window.clsValue += entry.value;
                    }
                }
            }).observe({ type: 'layout-shift', buffered: true });
        """)

    @allure.step("Получить Cumulative Layout Shift")
    def get_cls(self):
        return self.page.evaluate("() => window.clsValue")

    @allure.step("Получить Device Pixel Ratio")
    def get_device_pixel_ratio(self):
        return self.page.evaluate("() => window.devicePixelRatio")

    @allure.step("Получить время загрузи страницы в миллисекундах")
    def get_load_time_ms(self):
        return self.page.evaluate(
            "() => performance.timing.loadEventEnd"
            " - performance.timing.navigationStart"
        )

    @allure.step("Кликнуть по иконке корзины в header сайта")
    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    @allure.step("Кликнуть по иконке корзины в header сайта (tap)")
    def tap_shopping_cart_icon(self):
        self.shopping_cart_icon.tap()

    @allure.step("Проверить количество товаров в корзине")
    def verify_items_count_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    @allure.step("Проверить, что корзина пуста")
    def verify_bucket_is_empty(self):
        expect(self.cart_badge).to_have_count(0)

    @allure.step("Кликнуть по бургер-меню")
    def click_burger_menu_button(self):
        self.burger_menu_btn.click()

    @allure.step("Кликнуть по кнопке Logout")
    def click_logout_button(self):
        self.logout_button.click()

    @allure.step("Проверить, что элемент кликабелен")
    def click_visible_button(self, locator):
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        locator.click(trial=True)

    @allure.step("Проверить, что все элементы кликабельны")
    def verify_all_clickable(self, locator):
        for i in range(locator.count()):
            self.click_visible_button(locator.nth(i))

    @allure.step("Проверить, что все ссылки в боковом меню кликабельны")
    def verify_sidebar_links_are_clickable(self):
        self.verify_all_clickable(self.sidebar_links)

    @allure.step("Закрыть боковое меню")
    def click_close_sidebar_button(self):
        self.close_sidebar_button.click()

    @allure.step("Проверить, что боковое меню не отображается")
    def verify_sidebar_is_not_visible(self):
        expect(self.sidebar).to_be_hidden()

    @allure.step("Проверить, что боковое меню отображается")
    def verify_sidebar_is_visible(self):
        expect(self.sidebar).to_be_visible()

    @allure.step("Проверить, что страница не имеет горизонтального скролла")
    def verify_page_does_not_have_horizontal_scroll(self):
        has_horizontal_scroll = self.page.evaluate("""
            () => document.documentElement.scrollWidth > document.documentElement.clientWidth
        """)

        assert not has_horizontal_scroll, "Есть горизонтальный скролл"

    def is_elements_overlapping(self, locator1, locator2):
        box1 = locator1.bounding_box()
        box2 = locator2.bounding_box()

        assert box1 is not None
        assert box2 is not None

        return not (
                box1["x"] + box1["width"] <= box2["x"] or
                box2["x"] + box2["width"] <= box1["x"] or
                box1["y"] + box1["height"] <= box2["y"] or
                box2["y"] + box2["height"] <= box1["y"]
        )

    @allure.step("Проверить, что кнопка меню доступна и не перекрыта бейджем корзины")
    def is_badge_overlapping_menu_button(self):
        return self.is_elements_overlapping(
            self.cart_badge,
            self.burger_menu_btn
        )

    @allure.step("Проверить, что бейдж корзины не перекрывает кнопку меню")
    def verify_badge_does_not_overlap_menu_button(self):
        assert not self.is_badge_overlapping_menu_button(), \
            "Бейдж корзины перекрывает кнопку бургер-меню"

    @allure.step("Проверить размер viewport")
    def verify_viewport_size(self, expected_width: int, expected_height: int):
        viewport = self.page.viewport_size
        assert viewport["width"] == expected_width
        assert viewport["height"] == expected_height

        real_width = self.page.evaluate("() => window.innerWidth")
        assert real_width == expected_width

    @allure.step("Проверить, что высота элемента не меньше {min_height}px")
    def verify_element_height_at_least(self, locator, min_height: int):
        box = locator.bounding_box()
        assert box is not None, "Элемент не найден или не виден"

        actual_height = box["height"]
        assert actual_height >= min_height, \
            f"Высота элемента {actual_height}px меньше {min_height}px"

    @allure.step("Проверить, что ширина элемента не меньше {min_width}px и "
                 "высота элемента не меньше {min_height}px ")
    def verify_element_width_and_height_at_least(self, locator, min_width: int, min_height: int):
        box = locator.bounding_box()
        assert box is not None, "Элемент не найден или не виден"

        actual_width = box["width"]
        actual_height = box["height"]

        assert actual_width >= min_width, \
            f"Ширина элемента {actual_width}px меньше {min_width}px"
        assert actual_height >= min_height, \
            f"Высота элемента {actual_height}px меньше {min_height}px"

    @allure.step("Проверить, что размер шрифта элемента не меньше {min_size}px")
    def verify_element_font_size_at_least(self, locator, min_size: int):
        font_size = locator.first.evaluate(
            "el => parseFloat(getComputedStyle(el).fontSize)"
        )

        assert font_size >= min_size, \
            f"Font size {font_size}px меньше {min_size}px"

    @allure.step("Дождаться полной загрузки страницы")
    def wait_until_page_fully_loaded(self):
        self.page.wait_for_load_state("load")
