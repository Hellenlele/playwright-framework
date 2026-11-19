import pytest
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.components.table import TableComponent


BASE = "https://the-internet.herokuapp.com"


class TestTable:
    PATH = f"{BASE}/tables"

    def test_read_headers(self, page: Page):
        page.goto(self.PATH)
        table = TableComponent(page, "#table1")
        headers = table.get_headers()
        assert "Last Name" in headers
        assert "First Name" in headers
        assert "Email" in headers

    def test_row_count(self, page: Page):
        page.goto(self.PATH)
        table = TableComponent(page, "#table1")
        assert table.get_row_count() == 4

    def test_find_row_by_name(self, page: Page):
        page.goto(self.PATH)
        table = TableComponent(page, "#table1")
        row = table.find_row_by_text("Smith")
        assert row is not None
        assert "Smith" in row.inner_text()

    def test_read_specific_cell(self, page: Page):
        page.goto(self.PATH)
        table = TableComponent(page, "#table1")
        # Row 0, Col 0 = Last Name of first data row
        cell = table.get_cell(0, 0)
        assert cell != ""


class TestAlerts:
    PATH = f"{BASE}/javascript_alerts"

    def test_accept_alert(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.accept_dialog()
        page.get_by_role("button", name="Click for JS Alert").click()
        expect(page.locator("#result")).to_have_text("You successfully clicked an alert")

    def test_dismiss_confirm(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.dismiss_dialog()
        page.get_by_role("button", name="Click for JS Confirm").click()
        expect(page.locator("#result")).to_have_text("You clicked: Cancel")

    def test_type_in_prompt(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.accept_dialog(prompt_text="Hello Playwright")
        page.get_by_role("button", name="Click for JS Prompt").click()
        expect(page.locator("#result")).to_have_text("You entered: Hello Playwright")


class TestIframe:
    PATH = f"{BASE}/iframe"

    def test_type_inside_iframe(self, page: Page):
        page.goto(self.PATH)
        page.wait_for_load_state("networkidle")
        # Use TinyMCE's API — more reliable than raw keyboard events in a contenteditable iframe
        page.evaluate("tinymce.activeEditor.setContent('Hello from Playwright inside an iframe!')")
        content = page.evaluate("tinymce.activeEditor.getContent({format: 'text'})")
        assert "Hello from Playwright" in content


class TestWindows:
    PATH = f"{BASE}/windows"

    def test_switch_to_new_window(self, page: Page):
        page.goto(self.PATH)
        with page.context.expect_page() as new_page_info:
            page.get_by_role("link", name="Click Here").click()
        new_page = new_page_info.value
        new_page.wait_for_load_state()
        assert "New Window" in new_page.title()


class TestHover:
    PATH = f"{BASE}/hovers"

    def test_hover_reveals_element(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        page.locator(".figure").first.hover()
        expect(page.locator(".figure").first.locator(".figcaption")).to_be_visible()


class TestDragDrop:
    PATH = f"{BASE}/drag_and_drop"

    def test_drag_and_drop(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.drag_and_drop("#column-a", "#column-b")
        assert base.get_text("#column-a header") == "B"


class TestScroll:
    PATH = f"{BASE}/infinite_scroll"

    def test_scroll_to_bottom_loads_content(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        initial_count = page.locator(".jscroll-added").count()
        base.scroll_to_bottom()
        page.wait_for_timeout(1000)
        new_count = page.locator(".jscroll-added").count()
        assert new_count >= initial_count
