
class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url):
        self.page.goto(url)
