import re

import allure

from utils.logger import get_logger

logger = get_logger("accessibility_mixin")

# ---------------------------------------------------------------------------
# WCAG 2.1 contrast helpers
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


class AccessibilityMixin:
    """WCAG-контраст, мёртвые зоны, размеры элементов, перекрытия."""

    @allure.step("Измерить контраст текст/фон для {selector}")
    def get_contrast_ratio(self, selector: str) -> float:
        result = self.page.evaluate(_GET_ELEMENT_COLORS_JS, selector)
        assert result is not None, f"Элемент не найден в DOM: {selector}"
        fg = _parse_rgb(result["color"])
        bg = _parse_rgb(result["bgColor"])
        ratio = _contrast_ratio(fg, bg)
        logger.debug(
            f"Контраст для '{selector}': {ratio}:1 "
            f"(fg={result['color']}, bg={result['bgColor']})"
        )
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
    def verify_wcag_contrast(self, selector: str, label: str, min_ratio: float = 4.5):
        logger.debug(f"Проверка WCAG контраста для '{label}': минимум {min_ratio}:1")
        ratio = self.get_contrast_ratio(selector)
        assert ratio >= min_ratio, (
            f"[WCAG AA FAIL] {label}: контраст {ratio}:1 < требуемых {min_ratio}:1\n"
            f"selector: {selector}"
        )

    @allure.step("Проверить отсутствие мертвых зон")
    def verify_no_dead_zones(self):
        interactive_elements = self.page.locator(
            "button, a, input, select, textarea, [role='button']"
        )

        count = interactive_elements.count()
        logger.info(f"Проверка мёртвых зон: найдено {count} интерактивных элементов")

        for i in range(count):
            element = interactive_elements.nth(i)

            assert element.is_visible(), f"Элемент #{i} невидим"
            assert element.is_enabled(), f"Элемент #{i} неактивен"

            box = element.bounding_box()
            assert box is not None
            assert box["width"] > 0, f"Элемент #{i} width=0"
            assert box["height"] > 0, f"Элемент #{i} height=0"

            in_viewport = element.evaluate("""
                el => {
                    const rect = el.getBoundingClientRect();
                    return (
                        rect.top >= 0 &&
                        rect.left >= 0 &&
                        rect.bottom <= window.innerHeight &&
                        rect.right <= window.innerWidth
                    );
                }
            """)
            assert in_viewport, f"Элемент #{i} вне viewport"

        logger.debug(f"Все {count} интерактивных элементов прошли проверку мёртвых зон")

    @allure.step("Проверить, что высота элемента не меньше {min_height}px")
    def verify_element_height_at_least(self, locator, min_height: int):
        box = locator.bounding_box()
        assert box is not None, "Элемент не найден или не виден"

        actual_height = box["height"]
        logger.debug(f"Высота элемента: {actual_height}px, минимум: {min_height}px")
        assert actual_height >= min_height, \
            f"Высота элемента {actual_height}px меньше {min_height}px"

    @allure.step("Проверить, что ширина элемента не меньше {min_width}px и "
                 "высота элемента не меньше {min_height}px")
    def verify_element_width_and_height_at_least(self, locator, min_width: int, min_height: int):
        box = locator.bounding_box()
        assert box is not None, "Элемент не найден или не виден"

        actual_width = box["width"]
        actual_height = box["height"]
        logger.debug(
            f"Размер элемента: {actual_width}x{actual_height}px, "
            f"минимум: {min_width}x{min_height}px"
        )
        assert actual_width >= min_width, \
            f"Ширина элемента {actual_width}px меньше {min_width}px"
        assert actual_height >= min_height, \
            f"Высота элемента {actual_height}px меньше {min_height}px"

    @allure.step("Проверить, что размер шрифта элемента не меньше {min_size}px")
    def verify_element_font_size_at_least(self, locator, min_size: int):
        font_size = locator.first.evaluate(
            "el => parseFloat(getComputedStyle(el).fontSize)"
        )
        logger.debug(f"Размер шрифта: {font_size}px, минимум: {min_size}px")
        assert font_size >= min_size, \
            f"Font size {font_size}px меньше {min_size}px"

    @allure.step("Проверить размер viewport")
    def verify_viewport_size(self, expected_width: int, expected_height: int):
        logger.debug(f"Проверка размера viewport: ожидается {expected_width}x{expected_height}")
        viewport = self.page.viewport_size
        assert viewport["width"] == expected_width
        assert viewport["height"] == expected_height

        real_width = self.page.evaluate("() => window.innerWidth")
        assert real_width == expected_width

    def is_elements_overlapping(self, locator1, locator2) -> bool:
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

    @allure.step("Проверить, что элемент кликабелен и не перекрыт бейджем корзины")
    def is_badge_overlapping_menu_button(self) -> bool:
        return self.is_elements_overlapping(self.cart_badge, self.burger_menu_btn)

    @allure.step("Проверить, что бейдж корзины не перекрывает кнопку меню")
    def verify_badge_does_not_overlap_menu_button(self):
        logger.debug("Проверка, что бейдж корзины не перекрывает кнопку бургер-меню")
        assert not self.is_badge_overlapping_menu_button(), \
            "Бейдж корзины перекрывает кнопку бургер-меню"
