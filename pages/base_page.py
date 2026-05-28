import re
from pathlib import Path

import allure
from playwright.sync_api import expect

from config.base import BASE_URL

# ---------------------------------------------------------------------------
# WCAG 2.1 contrast helpers (module-level, не зависят от страницы)
# ---------------------------------------------------------------------------

_GET_ELEMENT_COLORS_JS = """
(selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const color = getComputedStyle(el).color;

    // Поднимаемся по DOM, пока не найдём непрозрачный фон
    let node = el;
    let bgColor = 'rgb(255, 255, 255)';
    while (node) {
        const bg = getComputedStyle(node).backgroundColor;
        if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
            bgColor = bg;
            break;
        }
        node = node.parentElement;
    }
    return { color, bgColor };
}
"""


def _parse_rgb(css: str) -> tuple:
    """'rgb(19, 35, 34)' или 'rgba(...)' → (r, g, b)."""
    nums = re.findall(r'[\d.]+', css)
    return tuple(int(float(x)) for x in nums[:3])


def _relative_luminance(r: int, g: int, b: int) -> float:
    """Относительная яркость по WCAG 2.1 (IEC 61966-2-1)."""
    def linearize(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_ratio(fg: tuple, bg: tuple) -> float:
    """Коэффициент контраста по WCAG 2.1: (L_светлый + 0.05) / (L_тёмный + 0.05)."""
    L1 = _relative_luminance(*fg)
    L2 = _relative_luminance(*bg)
    lighter, darker = max(L1, L2), min(L1, L2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


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

    @allure.step("Проверить Device Pixel Ratio равен {expected_dpr}")
    def verify_device_pixel_ratio(self, expected_dpr: float):
        actual = self.get_device_pixel_ratio()
        assert actual == expected_dpr, \
            f"devicePixelRatio = {actual}, ожидался {expected_dpr}"

    @allure.step("Получить язык браузера (navigator.language)")
    def get_navigator_language(self):
        return self.page.evaluate("() => navigator.language")

    @allure.step("Проверить язык браузера равен {expected_locale}")
    def verify_navigator_language(self, expected_locale: str):
        actual = self.get_navigator_language()
        assert actual == expected_locale, \
            f"navigator.language = '{actual}', ожидался '{expected_locale}'"

    @allure.step("Получить смещение часового пояса в часах")
    def get_timezone_offset_hours(self):
        return self.page.evaluate("() => -new Date().getTimezoneOffset() / 60")

    @allure.step("Проверить смещение часового пояса равно UTC+{expected_offset_hours}")
    def verify_timezone_offset_hours(self, expected_offset_hours: int):
        actual = self.get_timezone_offset_hours()
        assert actual == expected_offset_hours, \
            f"Смещение часового пояса = UTC+{actual}, ожидался UTC+{expected_offset_hours}"

    @allure.step("Проверить кодировку страницы UTF-8")
    def verify_page_charset_utf8(self):
        charset = self.page.evaluate("() => document.characterSet")
        assert charset.upper() == "UTF-8", \
            f"Кодировка страницы: {charset}, ожидалась UTF-8"

    @allure.step("Проверить отсутствие символов замены (U+FFFD) на странице")
    def verify_no_encoding_errors(self):
        has_replacement_char = self.page.evaluate(
            "() => document.body.innerText.includes('\uFFFD')"
        )
        assert not has_replacement_char, \
            "На странице обнаружены символы замены (U+FFFD) — возможна проблема с кодировкой"

    @allure.step("Получить время загрузки страницы в миллисекундах")
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

    @allure.step("Проверить, что медиазапрос prefers-reduced-motion: reduce активен")
    def verify_prefers_reduced_motion_active(self):
        matches = self.page.evaluate(
            "() => window.matchMedia('(prefers-reduced-motion: reduce)').matches"
        )
        assert matches, "prefers-reduced-motion: reduce не активен в браузере"

    @allure.step("Проверить, что элемент не скрыт анимацией (не hidden, не прозрачен)")
    def verify_element_not_hidden_by_animation(self, locator):
        result = locator.evaluate("""
            el => ({
                visibility: getComputedStyle(el).visibility,
                opacity: parseFloat(getComputedStyle(el).opacity),
                display: getComputedStyle(el).display
            })
        """)
        assert result["visibility"] != "hidden", \
            "Элемент скрыт через visibility:hidden — возможно, заблокирован анимацией"
        assert result["display"] != "none", \
            "Элемент скрыт через display:none — возможно, заблокирован анимацией"
        assert result["opacity"] > 0, \
            f"Элемент прозрачен (opacity={result['opacity']}) — возможно, заблокирован анимацией"

    @allure.step("Проверить доступность бокового меню при reduced motion")
    def verify_burger_menu_accessible_with_reduced_motion(self):
        self.burger_menu_btn.tap()
        expect(self.sidebar).to_be_visible()
        self.verify_sidebar_links_are_clickable()
        self.close_sidebar_button.tap()
        expect(self.sidebar).to_be_hidden()

    @allure.step("Получить User-Agent браузера")
    def get_user_agent(self) -> str:
        return self.page.evaluate("() => navigator.userAgent")

    @allure.step("Проверить, что User-Agent является мобильным")
    def verify_user_agent_is_mobile(self):
        ua = self.get_user_agent()
        mobile_keywords = ("Mobile", "Android", "iPhone", "iPad")
        assert any(kw in ua for kw in mobile_keywords), \
            f"navigator.userAgent не является мобильным: {ua}"

    @allure.step("Открыть страницу, перехватить User-Agent из HTTP-запроса и проверить, что он мобильный")
    def open_and_verify_request_user_agent_is_mobile(self, url: str = BASE_URL):
        # page.on("request") + wait_until="domcontentloaded" вызывают deadlock в webkit:
        # listener держит event loop, и DOMContentLoaded никогда не приходит.
        # Решение: wait_until="commit" (headers получены => request уже захвачен),
        # снимаем listener, затем отдельно ждём domcontentloaded без активного слушателя.
        captured = {}

        def on_request(request):
            if not captured and request.resource_type == "document":
                captured["ua"] = request.headers.get("user-agent", "")

        self.page.on("request", on_request)
        try:
            self.page.goto(url, wait_until="commit")
        finally:
            self.page.remove_listener("request", on_request)

        self.page.wait_for_load_state("domcontentloaded")

        ua = captured.get("ua", "")
        mobile_keywords = ("Mobile", "Android", "iPhone", "iPad")
        assert ua, "User-Agent не был перехвачен из HTTP-запроса к серверу"
        assert any(kw in ua for kw in mobile_keywords), \
            f"User-Agent в HTTP-запросе к серверу не является мобильным: {ua}"

    @allure.step("Проверить, что HTML-ответ содержит мобильный meta viewport")
    def verify_response_contains_mobile_viewport(self):
        html = self.page.content()
        assert "viewport" in html, \
            "В HTML-ответе не найден тег <meta name='viewport'>"
        assert "width=device-width" in html, \
            "Meta viewport не содержит width=device-width"

    @allure.step("Проверить, что HTML-ответ содержит классы мобильной навигации")
    def verify_response_contains_mobile_nav_classes(self):
        html = self.page.content()
        mobile_classes = ("bm-burger-button", "bm-menu", "bm-item-list")
        for cls in mobile_classes:
            assert cls in html, \
                f"В HTML-ответе не найден мобильный класс '{cls}'"

    @allure.step("Проверить наличие мобильной навигации (hamburger-меню) в DOM")
    def verify_mobile_navigation_present(self):
        burger_button = self.page.locator(".bm-burger-button")
        expect(burger_button).to_be_visible()

    # --- Методы проверки изоляции контекстов ---

    @allure.step("Получить значение куки session-username")
    def get_session_cookie(self) -> str:
        for cookie in self.page.context.cookies():
            if cookie["name"] == "session-username":
                return cookie["value"]
        return ""

    @allure.step("Проверить, что сессионная кука установлена (контекст аутентифицирован)")
    def verify_session_cookie_exists(self):
        value = self.get_session_cookie()
        assert value, \
            "Кука session-username отсутствует — сессия не создана"

    @allure.step("Проверить, что сессионная кука отсутствует (свежий / разлогиненный контекст)")
    def verify_no_session_cookie(self):
        value = self.get_session_cookie()
        assert not value, \
            f"Кука session-username присутствует в контексте: '{value}' — контексты не изолированы"

    @allure.step("Получить содержимое корзины из localStorage")
    def get_cart_storage_contents(self) -> list:
        return self.page.evaluate(
            "() => JSON.parse(localStorage.getItem('cart-contents') || '[]')"
        )

    @allure.step("Проверить, что cart-contents в localStorage пуст (корзина не унаследована)")
    def verify_cart_storage_is_empty(self):
        contents = self.get_cart_storage_contents()
        assert contents == [], \
            f"localStorage cart-contents не пуст: {contents} — состояние унаследовано из другого контекста"

    @allure.step("Проверить, что в localStorage ровно {expected_count} позиций в корзине")
    def verify_cart_storage_count(self, expected_count: int):
        contents = self.get_cart_storage_contents()
        assert len(contents) == expected_count, \
            (f"localStorage cart-contents содержит {len(contents)} позиций {contents}, "
             f"ожидалось {expected_count} — возможна утечка состояния из другого контекста")

    # --- Методы сохранения артефактов (скриншоты) ---

    @allure.step("Сохранить скриншот: {name}_{device_label}.png")
    def take_screenshot(self, name: str, device_label: str) -> str:
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        filename = f"{name}_{device_label}.png"
        path = screenshots_dir / filename

        self.page.screenshot(path=str(path), full_page=False)

        allure.attach.file(
            str(path),
            name=filename,
            attachment_type=allure.attachment_type.PNG
        )

        return str(path)

    @allure.step("Проверить, что файл скриншота сохранён и не пуст")
    def verify_screenshot_saved(self, path: str):
        p = Path(path)
        assert p.exists(), f"Файл скриншота не создан: {path}"
        assert p.stat().st_size > 0, f"Файл скриншота пуст (0 байт): {path}"

    # --- Методы проверки контраста (WCAG 2.1) ---

    @allure.step("Измерить контраст текст/фон для {selector}")
    def get_contrast_ratio(self, selector: str) -> float:
        result = self.page.evaluate(_GET_ELEMENT_COLORS_JS, selector)
        assert result is not None, f"Элемент не найден в DOM: {selector}"
        fg = _parse_rgb(result["color"])
        bg = _parse_rgb(result["bgColor"])
        ratio = _contrast_ratio(fg, bg)
        allure.attach(
            f"selector: {selector}\n"
            f"color:     {result['color']}\n"
            f"bgColor:   {result['bgColor']}\n"
            f"ratio:     {ratio}:1",
            name="contrast_detail",
            attachment_type=allure.attachment_type.TEXT
        )
        return ratio

    @allure.step("Проверить WCAG 2.1 AA контраст: {label} ≥ {min_ratio}:1")
    def verify_wcag_contrast(self, selector: str, label: str,
                             min_ratio: float = 4.5):
        ratio = self.get_contrast_ratio(selector)
        assert ratio >= min_ratio, (
            f"[WCAG AA FAIL] {label}: контраст {ratio}:1 < требуемых {min_ratio}:1\n"
            f"selector: {selector}"
        )

    def go_to_previous_page(self):
        self.page.go_back(wait_until="load")

    @allure.step(
        "Проверить отсутствие мертвых зон"
    )
    def verify_no_dead_zones(self):

        interactive_elements = self.page.locator(
            """
            button,
            a,
            input,
            select,
            textarea,
            [role='button']
            """
        )

        count = interactive_elements.count()

        for i in range(count):
            element = interactive_elements.nth(i)

            # видим
            assert element.is_visible(), (
                f"Элемент #{i} невидим"
            )

            # активен
            assert element.is_enabled(), (
                f"Элемент #{i} неактивен"
            )

            # имеет размер
            box = element.bounding_box()

            assert box is not None

            assert box["width"] > 0, (
                f"Элемент #{i} width=0"
            )

            assert box["height"] > 0, (
                f"Элемент #{i} height=0"
            )

            # находится в зоне видимости
            in_viewport = element.evaluate("""
            el => {
                const rect = el.getBoundingClientRect()

                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <=
                    window.innerHeight &&
                    rect.right <=
                    window.innerWidth
                )
            }
            """)

            assert in_viewport, (
                f"Элемент #{i} вне viewport"
            )
