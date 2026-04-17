import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def page():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
