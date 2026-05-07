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

    device_name = params["device"]
    browser_name = params["browser"]
    landscape = params.get("landscape", False)

    with sync_playwright() as pw:
        browser = getattr(pw, browser_name).launch()

        device = pw.devices[device_name].copy()

        if landscape:
            device["viewport"] = {
                "width": device["viewport"]["height"],
                "height": device["viewport"]["width"]
            }

        context = browser.new_context(**device)

        page = context.new_page()

        yield page

        context.close()
        browser.close()


@pytest.fixture
def logged_in_mobile_page(request):
    params = request.param

    device_name = params["device"]
    browser_name = params["browser"]
    landscape = params.get("landscape", False)

    with sync_playwright() as pw:
        browser = getattr(pw, browser_name).launch()

        device = pw.devices[device_name].copy()

        if landscape:
            device["viewport"] = {
                "width": device["viewport"]["height"],
                "height": device["viewport"]["width"]
            }

        context = browser.new_context(**device)
        page = context.new_page()

        login_page = LoginPage(page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.verify_page_does_not_have_horizontal_scroll()
        login_page.verify_username_input_type()
        login_page.verify_password_input_type()
        login_page.authorize(USER1_NAME, USER_PASSWORD, use_tap=True)
        login_page.verify_login_success()

        yield page

        browser.close()


@pytest.fixture
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USER_PASSWORD)
    login_page.click_login()
    yield page
