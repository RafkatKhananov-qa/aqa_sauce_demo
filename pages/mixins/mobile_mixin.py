import allure
from playwright.sync_api import expect

from config.base import BASE_URL
from utils.logger import get_logger

logger = get_logger("mobile_mixin")


class MobileMixin:
    """Мобильные проверки: viewport, DPR, UA, локаль, часовой пояс, meta-теги."""

    @allure.step("Получить Device Pixel Ratio")
    def get_device_pixel_ratio(self):
        dpr = self.page.evaluate("() => window.devicePixelRatio")
        logger.debug(f"Device Pixel Ratio: {dpr}")
        return dpr

    @allure.step("Проверить Device Pixel Ratio равен {expected_dpr}")
    def verify_device_pixel_ratio(self, expected_dpr: float):
        actual = self.get_device_pixel_ratio()
        logger.debug(f"Проверка DPR: ожидается {expected_dpr}, фактически {actual}")
        assert actual == expected_dpr, \
            f"devicePixelRatio = {actual}, ожидался {expected_dpr}"

    @allure.step("Получить язык браузера (navigator.language)")
    def get_navigator_language(self):
        lang = self.page.evaluate("() => navigator.language")
        logger.debug(f"navigator.language: {lang}")
        return lang

    @allure.step("Проверить язык браузера равен {expected_locale}")
    def verify_navigator_language(self, expected_locale: str):
        actual = self.get_navigator_language()
        logger.debug(f"Проверка языка браузера: ожидается '{expected_locale}', фактически '{actual}'")
        assert actual == expected_locale, \
            f"navigator.language = '{actual}', ожидался '{expected_locale}'"

    @allure.step("Получить смещение часового пояса в часах")
    def get_timezone_offset_hours(self):
        offset = self.page.evaluate("() => -new Date().getTimezoneOffset() / 60")
        logger.debug(f"Смещение часового пояса: UTC+{offset}")
        return offset

    @allure.step("Проверить смещение часового пояса равно UTC+{expected_offset_hours}")
    def verify_timezone_offset_hours(self, expected_offset_hours: int):
        actual = self.get_timezone_offset_hours()
        logger.debug(f"Проверка часового пояса: ожидается UTC+{expected_offset_hours}, фактически UTC+{actual}")
        assert actual == expected_offset_hours, \
            f"Смещение часового пояса = UTC+{actual}, ожидался UTC+{expected_offset_hours}"

    @allure.step("Проверить кодировку страницы UTF-8")
    def verify_page_charset_utf8(self):
        charset = self.page.evaluate("() => document.characterSet")
        logger.debug(f"Кодировка страницы: {charset}")
        assert charset.upper() == "UTF-8", \
            f"Кодировка страницы: {charset}, ожидалась UTF-8"

    @allure.step("Проверить отсутствие символов замены (U+FFFD) на странице")
    def verify_no_encoding_errors(self):
        has_replacement_char = self.page.evaluate(
            "() => document.body.innerText.includes('\uFFFD')"
        )
        if not has_replacement_char:
            logger.debug("Символы замены (U+FFFD) не обнаружены")
        assert not has_replacement_char, \
            "На странице обнаружены символы замены (U+FFFD) — возможна проблема с кодировкой"

    @allure.step("Проверить, что страница не имеет горизонтального скролла")
    def verify_page_does_not_have_horizontal_scroll(self):
        has_horizontal_scroll = self.page.evaluate("""
            () => document.documentElement.scrollWidth > document.documentElement.clientWidth
        """)
        logger.debug(f"Горизонтальный скролл: {'обнаружен' if has_horizontal_scroll else 'отсутствует'}")
        assert not has_horizontal_scroll, "Есть горизонтальный скролл"

    @allure.step("Проверить, что медиазапрос prefers-reduced-motion: reduce активен")
    def verify_prefers_reduced_motion_active(self):
        matches = self.page.evaluate(
            "() => window.matchMedia('(prefers-reduced-motion: reduce)').matches"
        )
        logger.debug(f"prefers-reduced-motion: reduce активен: {matches}")
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
        logger.debug(
            f"Видимость элемента: visibility={result['visibility']}, "
            f"opacity={result['opacity']}, display={result['display']}"
        )
        assert result["visibility"] != "hidden", \
            "Элемент скрыт через visibility:hidden — возможно, заблокирован анимацией"
        assert result["display"] != "none", \
            "Элемент скрыт через display:none — возможно, заблокирован анимацией"
        assert result["opacity"] > 0, \
            f"Элемент прозрачен (opacity={result['opacity']}) — возможно, заблокирован анимацией"

    @allure.step("Проверить доступность бокового меню при reduced motion")
    def verify_burger_menu_accessible_with_reduced_motion(self):
        logger.info("Проверка доступности бокового меню при reduced motion")
        self.burger_menu_btn.tap()
        expect(self.sidebar).to_be_visible()
        self.verify_sidebar_links_are_clickable()
        self.close_sidebar_button.tap()
        expect(self.sidebar).to_be_hidden()

    @allure.step("Получить User-Agent браузера")
    def get_user_agent(self) -> str:
        ua = self.page.evaluate("() => navigator.userAgent")
        logger.debug(f"User-Agent: {ua}")
        return ua

    @allure.step("Проверить, что User-Agent является мобильным")
    def verify_user_agent_is_mobile(self):
        ua = self.get_user_agent()
        mobile_keywords = ("Mobile", "Android", "iPhone", "iPad")
        logger.debug(f"Проверка мобильности User-Agent: {ua}")
        assert any(kw in ua for kw in mobile_keywords), \
            f"navigator.userAgent не является мобильным: {ua}"

    @allure.step("Открыть страницу, перехватить User-Agent из HTTP-запроса и проверить, что он мобильный")
    def open_and_verify_request_user_agent_is_mobile(self, url: str = BASE_URL):
        logger.info(f"Открытие {url} с перехватом User-Agent из HTTP-запроса")
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
        logger.debug(f"Перехваченный User-Agent из HTTP-запроса: {ua}")
        mobile_keywords = ("Mobile", "Android", "iPhone", "iPad")
        assert ua, "User-Agent не был перехвачен из HTTP-запроса к серверу"
        assert any(kw in ua for kw in mobile_keywords), \
            f"User-Agent в HTTP-запросе к серверу не является мобильным: {ua}"

    @allure.step("Проверить, что HTML-ответ содержит мобильный meta viewport")
    def verify_response_contains_mobile_viewport(self):
        logger.debug("Проверка наличия мобильного viewport в HTML")
        html = self.page.content()
        assert "viewport" in html, \
            "В HTML-ответе не найден тег <meta name='viewport'>"
        assert "width=device-width" in html, \
            "Meta viewport не содержит width=device-width"

    @allure.step("Проверить, что HTML-ответ содержит классы мобильной навигации")
    def verify_response_contains_mobile_nav_classes(self):
        logger.debug("Проверка наличия мобильных классов навигации в HTML")
        html = self.page.content()
        mobile_classes = ("bm-burger-button", "bm-menu", "bm-item-list")
        for cls in mobile_classes:
            assert cls in html, \
                f"В HTML-ответе не найден мобильный класс '{cls}'"

    @allure.step("Проверить наличие мобильной навигации (hamburger-меню) в DOM")
    def verify_mobile_navigation_present(self):
        logger.debug("Проверка наличия мобильной навигации в DOM")
        burger_button = self.page.locator(".bm-burger-button")
        expect(burger_button).to_be_visible()
