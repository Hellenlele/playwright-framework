from playwright.sync_api import Page
from src.pages.home_page import HomePage


EXPECTED_LINKS = [
    "A/B Testing",
    "Add/Remove Elements",
    "Checkboxes",
    "Disappearing Elements",
    "Drag and Drop",
    "Dropdown",
    "Dynamic Content",
    "Dynamic Controls",
    "Dynamic Loading",
    "File Download",
    "File Upload",
    "Form Authentication",
    "Frames",
    "Hovers",
    "Infinite Scroll",
    "JavaScript Alerts",
    "Key Presses",
    "Multiple Windows",
    "Nested Frames",
    "Redirect Link",
    "Sortable Data Tables",
    "Status Codes",
    "Typos",
    "WYSIWYG Editor",
]


class TestHomePageLoad:
    def test_title(self, page: Page):
        home = HomePage(page).open()
        home.expect_title("The Internet")

    def test_heading(self, page: Page):
        home = HomePage(page).open()
        assert home.get_heading() == "Welcome to the-internet"

    def test_page_url(self, page: Page):
        home = HomePage(page).open()
        home.expect_url_contains("the-internet.herokuapp.com")


class TestHomePageNavigation:
    def test_go_to_login_page(self, page: Page):
        home = HomePage(page).open()
        home.go_to("Form Authentication")
        home.expect_url("https://the-internet.herokuapp.com/login")

    def test_go_to_checkboxes(self, page: Page):
        home = HomePage(page).open()
        home.go_to("Checkboxes")
        home.expect_url("https://the-internet.herokuapp.com/checkboxes")

    def test_go_to_dropdown(self, page: Page):
        home = HomePage(page).open()
        home.go_to("Dropdown")
        home.expect_url("https://the-internet.herokuapp.com/dropdown")

    def test_go_to_drag_and_drop(self, page: Page):
        home = HomePage(page).open()
        home.go_to("Drag and Drop")
        home.expect_url("https://the-internet.herokuapp.com/drag_and_drop")

    def test_go_to_javascript_alerts(self, page: Page):
        home = HomePage(page).open()
        home.go_to("JavaScript Alerts")
        home.expect_url("https://the-internet.herokuapp.com/javascript_alerts")


class TestHomePageLinks:
    def test_all_expected_links_present(self, page: Page):
        home = HomePage(page).open()
        for link_text in EXPECTED_LINKS:
            assert home.has_link(link_text), f"Link not found: '{link_text}'"

    def test_links_list_is_not_empty(self, page: Page):
        home = HomePage(page).open()
        assert len(home.get_all_links()) > 0

    def test_links_count(self, page: Page):
        home = HomePage(page).open()
        assert len(home.get_all_links()) >= len(EXPECTED_LINKS)
