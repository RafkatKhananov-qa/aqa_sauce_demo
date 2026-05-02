import re
import time

import allure
from playwright.sync_api import expect
import pytest

from config.base import BASE_URL


@allure.epic("Saucedemo mobile")
@allure.parent_suite("SauceDemo mobile")
class TestCheckoutMobile:

    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 11", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_check_mobile_001(self, mobile_page):
        mobile_page.goto(BASE_URL)
        assert mobile_page.viewport_size["width"] < 415

    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "Pixel 5", "browser": "chromium"},
                             ],
                             indirect=True)
    def test_check_mobile_002(self, mobile_page):
        mobile_page.goto("https://demo.playwright.dev/todomvc")
        task_input = mobile_page.locator(".new-todo")
        task_input.fill("Task1")
        task_input.press('Enter')
        task_input.fill("Task2")
        task_input.press('Enter')
        check_all_tasks_button = mobile_page.locator(".toggle-all + label")
        check_all_tasks_button.tap()
        time.sleep(5)
        task_items = mobile_page.locator("//li[@data-testid='todo-item']")
        for i in range(task_items.count()):
            expect(task_items.nth(i)).to_have_class("completed")

    @pytest.mark.parametrize("mobile_page",
                             [
                                 {"device": "iPhone 11", "browser": "webkit"},
                                 {"device": "iPad Mini", "browser": "webkit"},
                             ],
                             indirect=True)
    def test_check_mobile_003(self, mobile_page):
        mobile_page.goto("https://google.com")
        expect(mobile_page).to_have_title(re.compile("Google"))
