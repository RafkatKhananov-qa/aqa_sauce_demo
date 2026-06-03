import allure

from utils.logger import get_logger

logger = get_logger("performance_mixin")


class PerformanceMixin:
    """CDP-метрики, эмуляция сети, память, FCP, CLS, время загрузки."""

    @allure.step("Эмулировать сеть 3G")
    def emulate_3g(self):
        logger.info("Эмуляция 3G сети (download=375KB/s, upload=750KB/s, latency=100ms)")
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": 375 * 1024 / 8,
            "uploadThroughput": 750 * 1024 / 8,
            "latency": 100
        })

    @allure.step("Эмулировать потерю сети")
    def emulate_offline(self):
        logger.info("Эмуляция потери сети — все запросы будут прерваны")
        self.page.route("**/*", lambda route: route.abort())

    @allure.step("Принудительная сборка мусора")
    def force_gc(self):
        logger.debug("Принудительная сборка мусора (HeapProfiler.collectGarbage)")
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("HeapProfiler.enable")
        cdp.send("HeapProfiler.collectGarbage")
        cdp.detach()

    @allure.step("Получить размер используемой JS-памяти")
    def get_memory_usage_bytes(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Performance.enable")
        metrics = cdp.send("Performance.getMetrics")
        value = next(
            m["value"] for m in metrics["metrics"]
            if m["name"] == "JSHeapUsedSize"
        )
        logger.debug(f"JS-память (JSHeapUsedSize): {value} байт")
        return value

    @allure.step("Получить First Contentful Paint в миллисекундах")
    def get_fcp_ms(self):
        result = self.page.evaluate("""
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
        logger.debug(f"First Contentful Paint: {result} мс")
        return result

    @allure.step("Включить отслеживание CLS")
    def setup_cls_tracking(self):
        logger.debug("Включено отслеживание Cumulative Layout Shift")
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
        value = self.page.evaluate("() => window.clsValue")
        logger.debug(f"Cumulative Layout Shift: {value}")
        return value

    @allure.step("Получить время загрузки страницы в миллисекундах")
    def get_load_time_ms(self):
        value = self.page.evaluate(
            "() => performance.timing.loadEventEnd"
            " - performance.timing.navigationStart"
        )
        logger.info(f"Время загрузки страницы: {value} мс")
        return value
