import time

import allure
import pytest

from playwright.sync_api import expect

from config.base import BASE_URL, INVENTORY_URL
from config.users import USER1_NAME, USER_PASSWORD
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Mobile Performance")
class TestMobilePerformance:
    @allure.story("Производительность на мобильных сетях")
    @allure.title("Загрузка главной страницы при эмуляции 3G")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_001(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.emulate_3g()

        start_time = time.perf_counter()

        login_page.open()
        login_page.verify_critical_content_visible()

        critical_time = time.perf_counter() - start_time

        mobile_page.wait_for_load_state("load")
        load_time = time.perf_counter() - start_time

        assert critical_time < 18, f"Критический контент виден за {critical_time:.2f} сек, лимит 18 сек"
        assert load_time < 19, f"load событие произошло за {load_time:.2f} сек, лимит 19 сек"

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Время отклика кнопки Login на мобильном")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_002(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()

        login_page.fill_username(USER1_NAME)
        login_page.fill_password(USER_PASSWORD)

        start_time = time.perf_counter()

        login_page.tap_login()
        login_page.verify_login_success()

        response_time = time.perf_counter() - start_time

        assert response_time < 1.5, (
        f"Отклик Login составил {response_time:.2f} сек, лимит 1.5 сек"
    )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Нет блокирующих запросов к недоступным доменам")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_003(self, mobile_page):

        failed_requests = []

        def handle_failed_request(request):
            failed_requests.append({
                "url": request.url,
                "failure": request.failure
            })

        mobile_page.on("requestfailed", handle_failed_request)

        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.wait_until_page_fully_loaded()

        assert failed_requests == []

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Кэширование статических ресурсов")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_004(self, mobile_page):
        static_resources = []

        def handle_response(response):
            url = response.url

            if any(url.endswith(ext) for ext in (
                    ".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".webp"
            )):
                headers = response.headers

                static_resources.append({
                    "url": url,
                    "status": response.status,
                    "cache_control": headers.get("cache-control", ""),
                    "etag": headers.get("etag", ""),
                    "expires": headers.get("expires", "")
                })

        mobile_page.on("response", handle_response)

        login_page = LoginPage(mobile_page)

        login_page.open()
        login_page.wait_until_page_fully_loaded()

        mobile_page.reload()
        login_page.wait_until_page_fully_loaded()

        cacheable_resources = [
            resource for resource in static_resources
            if (
                    "max-age" in resource["cache_control"]
                    or resource["etag"]
                    or resource["expires"]
            )
        ]

        assert cacheable_resources, (
            f"Не найдено кэшируемых статических ресурсов. "
            f"Ресурсы: {static_resources}"
        )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Потребление памяти при длительной сессии")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_005(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.open()

        inventory_page.force_gc()
        initial_memory = inventory_page.get_memory_usage_bytes()

        item_ids = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
        for item_id in item_ids:
            logged_in_mobile_page.goto(f"{BASE_URL}inventory-item.html?id={item_id}")
            logged_in_mobile_page.wait_for_load_state("load")

        inventory_page.force_gc()
        final_memory = inventory_page.get_memory_usage_bytes()

        memory_growth = (final_memory - initial_memory) / initial_memory * 100

        assert memory_growth < 20, (
            f"Рост памяти {memory_growth:.2f}% превышает лимит 20%"
        )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Корректная работа при переключении сеть → offline → сеть")
    @pytest.mark.parametrize("logged_in_mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_007(self, logged_in_mobile_page):
        inventory_page = InventoryPage(logged_in_mobile_page)
        inventory_page.open(INVENTORY_URL)
        inventory_page.wait_until_page_fully_loaded()

        initial_items_count = inventory_page.inventory_item.count()

        inventory_page.emulate_offline()

        expect(inventory_page.inventory_item.first).to_be_visible()

        logged_in_mobile_page.unroute("**/*")
        logged_in_mobile_page.reload()

        inventory_page.wait_until_page_fully_loaded()

        final_items_count = inventory_page.inventory_item.count()

        assert initial_items_count == final_items_count, (
            f"Количество товаров изменилось: "
            f"{initial_items_count} -> {final_items_count}"
        )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Замер First Contentful Paint (FCP) на мобильном")
    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 7", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_perf_008(self, mobile_page):
        login_page = LoginPage(mobile_page)

        login_page.open()

        mobile_page.wait_for_load_state("networkidle")

        fcp = login_page.get_fcp_ms()

        assert fcp is not None, "FCP entry не найдена в performance timeline"

        fcp_sec = fcp / 1000

        assert fcp_sec < 3, (
            f"FCP составил {fcp_sec:.2f} сек, лимит 3 сек"
        )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Отсутствие 'мигания' контента при загрузке")
    @pytest.mark.parametrize(
        "mobile_page",
        [
            {"device": "Pixel 7", "browser": "chromium"},
        ],
        indirect=True
    )
    def test_perf_009(self, mobile_page):

        login_page = LoginPage(mobile_page)

        login_page.setup_cls_tracking()

        login_page.open()

        login_page.wait_until_page_fully_loaded()

        cls = login_page.get_cls()

        assert cls < 0.1, (
            f"CLS = {cls:.4f}, лимит < 0.1"
        )

    @allure.story("Производительность на мобильных сетях")
    @allure.title("Оптимизация изображений для мобильных")
    @pytest.mark.parametrize(
        "mobile_page",
        [
            {"device": "Pixel 7", "browser": "chromium"},
        ],
        indirect=True
    )
    def test_perf_010(self, mobile_page):

        login_page = LoginPage(mobile_page)

        login_page.login_and_verify(USER1_NAME, USER_PASSWORD)

        inventory_page = InventoryPage(mobile_page)
        srcset = inventory_page.get_first_image_srcset()
        device_pixel_ratio = inventory_page.get_device_pixel_ratio()

        assert srcset is not None, (
            "У изображения отсутствует srcset"
        )

        assert f"{round(device_pixel_ratio)}x" in srcset, (
            f"В srcset нет изображения для DPR={device_pixel_ratio}"
        )
