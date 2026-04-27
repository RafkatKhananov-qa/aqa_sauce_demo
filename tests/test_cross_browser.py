import pytest
from playwright.sync_api import sync_playwright
from config.users import USER1_NAME, USER_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(params=[
    pytest.param(("chromium", (1920, 1080), True), id="chromium-headless"),
    pytest.param(("chromium", (1366, 768), False), id="chromium-headed"),
    pytest.param(("chromium", (375, 667), True), id="chrome-mobile"),
    pytest.param(("firefox", (375, 667), True), id="firefox-headless"),
    pytest.param(("firefox", (1920, 1080), False), id="firefox-headed"),
    pytest.param(("firefox", (1920, 1080), True), id="firefox-desktop"),
    pytest.param(("chromium", (1920, 1080), True), id="chrome-desktop"),
    pytest.param(("webkit", (1366, 768), True), id="webkit-headless"),
    pytest.param(("webkit", (375, 667), False), id="webkit-headed"),
])
def custom_page(request):
    browser_name, (width, height), headless = request.param
    with sync_playwright() as pw:
        browser_type = getattr(pw, browser_name)
        browser = browser_type.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": width, "height": height}
        )
        page = context.new_page()
        yield page
        browser.close()


def test_cross_browser(custom_page):
    login_page = LoginPage(custom_page)
    login_page.login_and_verify(USER1_NAME, USER_PASSWORD)
