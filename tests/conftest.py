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
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USER_PASSWORD)
    login_page.click_login()
    yield page
