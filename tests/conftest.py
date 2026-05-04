import pytest
from playwright.sync_api import sync_playwright

from config.users import USER1_NAME, USER_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def page():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


@pytest.fixture
def mobile_page(request):
    params = request.param

    device_name = params.get("device", "iPhone 11")
    browser_name = params.get("browser", "chromium")

    with sync_playwright() as p:
        device = p.devices[device_name]

        browser_type = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit
        }[browser_name]

        browser = browser_type.launch(headless=False)
        context = browser.new_context(**device)
        page = context.new_page()

        yield page

        context.close()
        browser.close()


@pytest.fixture
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USER_PASSWORD)
    login_page.click_login()
    yield page
