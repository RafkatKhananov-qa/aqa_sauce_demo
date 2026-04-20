import pytest
from config.users import (USER2_NAME, USER3_NAME, USER4_NAME, USER5_NAME,
                          USER_WRONG_PASSWORD, LOGIN_ERROR_MESSAGE, USER_PASSWORD,
                          USER_WRONG_NAME, USERNAME_REQUIRED_MESSAGE, USER1_NAME,
                          PASSWORD_REQUIRED_MESSAGE, SQL_INJECTION_LOGIN, XSS_LOGIN)
from pages.login_page import LoginPage


@pytest.mark.parametrize("username, password", [
    (USER1_NAME, USER_PASSWORD)
])
def test_auth_001(page, username, password):
    login_page = LoginPage(page)

    login_page.open()

    login_page.verify_page_loaded()

    login_page.enter_username(username)
    login_page.verify_username(username)

    login_page.enter_password(password)
    login_page.verify_password(password)

    login_page.click_login()
    login_page.verify_login_success()


@pytest.mark.parametrize("username, password", [
    (USER2_NAME, USER_PASSWORD),
    (USER3_NAME, USER_PASSWORD),
    (USER4_NAME, USER_PASSWORD),
    (USER5_NAME, USER_PASSWORD)
])
def test_auth_002(page, username, password):
    login_page = LoginPage(page)

    login_page.open()

    login_page.verify_page_loaded()

    login_page.enter_username(username)
    login_page.verify_username(username)

    login_page.enter_password(password)
    login_page.verify_password(password)

    login_page.click_login()
    login_page.verify_login_success()


@pytest.mark.parametrize("username, password, error_message", [
    (USER1_NAME, USER_WRONG_PASSWORD, LOGIN_ERROR_MESSAGE),
    (USER_WRONG_NAME, USER_PASSWORD, LOGIN_ERROR_MESSAGE),
    ("", USER_PASSWORD, USERNAME_REQUIRED_MESSAGE),
    (USER1_NAME, "", PASSWORD_REQUIRED_MESSAGE),
    (SQL_INJECTION_LOGIN, USER_PASSWORD, LOGIN_ERROR_MESSAGE),
    (XSS_LOGIN, USER_PASSWORD, LOGIN_ERROR_MESSAGE),
])
def test_auth_003_004_005_006_007_008(page, username, password, error_message):
    login_page = LoginPage(page)

    login_page.open()

    login_page.verify_page_loaded()

    login_page.enter_username(username)
    login_page.verify_username(username)

    login_page.enter_password(password)
    login_page.verify_password(password)

    login_page.click_login()
    login_page.verify_error_message(error_message)


@pytest.mark.parametrize("username, password, error_message", [
    (USER1_NAME, USER_WRONG_PASSWORD, LOGIN_ERROR_MESSAGE),
])
def test_auth_009(page, username, password, error_message):
    login_page = LoginPage(page)

    login_page.open()

    login_page.verify_page_loaded()

    for _ in range(5):

        login_page.enter_username(username)
        login_page.verify_username(username)

        login_page.enter_password(password)
        login_page.verify_password(password)

        login_page.click_login()
        login_page.verify_error_message(error_message)

    login_page.enter_username(USER1_NAME)
    login_page.verify_username(USER1_NAME)

    login_page.enter_password(USER_PASSWORD)
    login_page.verify_password(USER_PASSWORD)

    login_page.click_login()
    login_page.verify_login_success()


@pytest.mark.parametrize("username, password", [
    (USER1_NAME, USER_PASSWORD)
])
def test_auth_010(page, username, password):
    login_page = LoginPage(page)

    login_page.open()

    login_page.verify_page_loaded()

    login_page.enter_username(username)
    login_page.verify_username(username)

    login_page.enter_password(password)
    login_page.verify_password(password)

    login_page.click_login()
    login_page.verify_login_success()

    page.reload()

    login_page.verify_login_success()
