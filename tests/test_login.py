from pages.login_page import LoginPage
from config.users import USER1_NAME, USER1_PASSWORD


def test_login_001(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.verify_page_loaded()
    login_page.authorize(USER1_NAME, USER1_PASSWORD)
    login_page.verify_login_success()
