from src.pages.login_page import LoginPage
from src.config.config import Config


class TestLogin:
    def test_successful_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login(Config.LOGIN_USERNAME, Config.LOGIN_PASSWORD)
        login_page.expect_login_success()

    def test_failed_login_wrong_username(self, login_page: LoginPage):
        login_page.open()
        login_page.login("wrong_user", Config.LOGIN_PASSWORD)
        login_page.expect_login_failure("Your username is invalid!")

    def test_failed_login_wrong_password(self, login_page: LoginPage):
        login_page.open()
        login_page.login(Config.LOGIN_USERNAME, "wrong_password")
        login_page.expect_login_failure("Your password is invalid!")

    def test_logout_after_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login(Config.LOGIN_USERNAME, Config.LOGIN_PASSWORD)
        login_page.expect_login_success()
        login_page.logout()
        login_page.expect_url_contains("/login")
        login_page.expect_contains_text("#flash", "You logged out of the secure area!")
