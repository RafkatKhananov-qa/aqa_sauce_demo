import allure
from pages.login_page import LoginPage
from config.users import USER1_NAME, USER_PASSWORD


@allure.feature("Login")
class TestLogin:
    @allure.story("Verifying authorize is successful")
    @allure.title("Авторизация на сайте успешна")
    def test_login_001(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.verify_page_loaded()
        login_page.authorize(USER1_NAME, USER_PASSWORD)
        login_page.verify_login_success()
