from playwright.sync_api import expect


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

    def open(self, url):
        self.page.goto(url)

    def click_shopping_cart_icon(self):
        self.shopping_cart_icon.click()

    def verify_items_count_in_bucket(self, num: str):
        expect(self.cart_badge).to_have_text(num)

    def verify_bucket_is_empty(self):
        expect(self.cart_badge).to_have_count(0)

    def click_burger_menu_button(self):
        self.burger_menu_btn.click()

    def click_logout_button(self):
        self.logout_button.click()

    def verify_sidebar_links_are_clickable(self):
        for i in range(self.sidebar_links.count()):
            expect(self.sidebar_links.nth(i)).to_be_visible()
            expect(self.sidebar_links.nth(i)).to_be_enabled()
            self.sidebar_links.nth(i).click(trial=True)

    def click_close_sidebar_button(self):
        self.close_sidebar_button.click()

    def verify_sidebar_is_not_visible(self):
        expect(self.sidebar).not_to_be_visible()
