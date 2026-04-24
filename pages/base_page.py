from config.base import BASE_URL


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url=BASE_URL):
        self.page.goto(url)

    def emulate_3g(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": 375 * 1024 / 8,
            "uploadThroughput": 750 * 1024 / 8,
            "latency": 100
        })

    def get_memory_usage_bytes(self):
        cdp = self.page.context.new_cdp_session(self.page)
        cdp.send("Performance.enable")
        metrics = cdp.send("Performance.getMetrics")
        return next(m["value"] for m in metrics["metrics"] if m["name"] == "JSHeapUsedSize")

    def get_load_time_ms(self):
        return self.page.evaluate(
            "() => performance.timing.loadEventEnd - performance.timing.navigationStart"
        )
