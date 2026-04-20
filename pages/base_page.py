from config.base import BASE_URL


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url=BASE_URL):
        self.page.goto(url)
