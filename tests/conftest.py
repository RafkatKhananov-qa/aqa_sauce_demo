import pytest
from playwright.sync_api import sync_playwright
from config.users import USER1_NAME, USER1_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def page():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


@pytest.fixture
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.verify_page_loaded()
    login_page.enter_username(USER1_NAME)
    login_page.verify_username(USER1_NAME)
    login_page.enter_password(USER1_PASSWORD)
    login_page.verify_password(USER1_PASSWORD)
    login_page.click_login()
    login_page.verify_login_success()
    yield page
