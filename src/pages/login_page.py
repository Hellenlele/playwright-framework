from playwright.sync_api import Page
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    _USERNAME = "#username"
    _PASSWORD = "#password"
    _SUBMIT = 'button[type="submit"]'
    _FLASH = "#flash"
    _LOGOUT = "a[href='/logout']"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self) -> "LoginPage":
        super().open(self.PATH)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.type(self._USERNAME, username)
        self.type(self._PASSWORD, password)
        self.click(self._SUBMIT)
        return self

    def flash_message(self) -> str:
        return self.get_text(self._FLASH)

    def logout(self) -> "LoginPage":
        self.click(self._LOGOUT)
        return self

    def expect_login_success(self) -> None:
        self.expect_url_contains("/secure")
        self.expect_contains_text(self._FLASH, "You logged into a secure area!")

    def expect_login_failure(self, message: str) -> None:
        self.expect_contains_text(self._FLASH, message)
