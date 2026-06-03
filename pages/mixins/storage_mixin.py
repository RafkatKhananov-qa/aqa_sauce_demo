import allure

from utils.logger import get_logger

logger = get_logger("storage_mixin")


class StorageMixin:
    """Сессионные куки и localStorage."""

    @allure.step("Получить значение куки session-username")
    def get_session_cookie(self) -> str:
        for cookie in self.page.context.cookies():
            if cookie["name"] == "session-username":
                value = cookie["value"]
                logger.debug(f"Сессионная кука session-username: '{value}'")
                return value
        logger.debug("Сессионная кука session-username не найдена")
        return ""

    @allure.step("Проверить, что сессионная кука установлена (контекст аутентифицирован)")
    def verify_session_cookie_exists(self):
        logger.debug("Проверка наличия сессионной куки")
        value = self.get_session_cookie()
        assert value, \
            "Кука session-username отсутствует — сессия не создана"

    @allure.step("Проверить, что сессионная кука отсутствует (свежий / разлогиненный контекст)")
    def verify_no_session_cookie(self):
        logger.debug("Проверка отсутствия сессионной куки")
        value = self.get_session_cookie()
        assert not value, \
            f"Кука session-username присутствует в контексте: '{value}' — контексты не изолированы"

    @allure.step("Получить содержимое корзины из localStorage")
    def get_cart_storage_contents(self) -> list:
        contents = self.page.evaluate(
            "() => JSON.parse(localStorage.getItem('cart-contents') || '[]')"
        )
        logger.debug(f"Содержимое корзины в localStorage: {contents}")
        return contents

    @allure.step("Проверить, что cart-contents в localStorage пуст (корзина не унаследована)")
    def verify_cart_storage_is_empty(self):
        logger.debug("Проверка, что корзина в localStorage пуста")
        contents = self.get_cart_storage_contents()
        assert contents == [], \
            f"localStorage cart-contents не пуст: {contents} — состояние унаследовано из другого контекста"

    @allure.step("Проверить, что в localStorage ровно {expected_count} позиций в корзине")
    def verify_cart_storage_count(self, expected_count: int):
        contents = self.get_cart_storage_contents()
        logger.debug(
            f"Количество позиций в корзине localStorage: {len(contents)}, "
            f"ожидается: {expected_count}"
        )
        assert len(contents) == expected_count, \
            (f"localStorage cart-contents содержит {len(contents)} позиций {contents}, "
             f"ожидалось {expected_count} — возможна утечка состояния из другого контекста")
