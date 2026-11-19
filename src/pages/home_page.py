from playwright.sync_api import Page
from src.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    _HEADING = "h1"
    _LINKS = "ul li a"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self) -> "HomePage":
        super().open(self.PATH)
        return self

    def go_to(self, link_text: str) -> "HomePage":
        self.page.get_by_role("link", name=link_text, exact=True).click()
        return self

    def get_heading(self) -> str:
        return self.get_text(self._HEADING)

    def get_all_links(self) -> list[str]:
        return self.page.locator(self._LINKS).all_inner_texts()

    def has_link(self, link_text: str) -> bool:
        return self.page.get_by_role("link", name=link_text).count() > 0
