import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.components.form import FormComponent
from src.components.dropdown import DropdownComponent


BASE = "https://the-internet.herokuapp.com"


class TestCheckboxes:
    PATH = f"{BASE}/checkboxes"

    def test_check_first_checkbox(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.check("input[type='checkbox']:nth-child(1)")
        base.expect_checked("input[type='checkbox']:nth-child(1)")

    def test_uncheck_second_checkbox(self, page: Page):
        page.goto(self.PATH)
        base = BasePage(page)
        base.uncheck("input[type='checkbox']:nth-child(3)")
        base.expect_not_checked("input[type='checkbox']:nth-child(3)")


class TestDropdown:
    PATH = f"{BASE}/dropdown"

    def test_select_option_1_by_label(self, page: Page):
        page.goto(self.PATH)
        dd = DropdownComponent(page)
        dd.select_by_label("#dropdown", "Option 1")
        assert dd.get_selected("#dropdown") == "Option 1"

    def test_select_option_2_by_value(self, page: Page):
        page.goto(self.PATH)
        dd = DropdownComponent(page)
        dd.select_by_value("#dropdown", "2")
        assert dd.get_selected("#dropdown") == "Option 2"

    def test_all_options_listed(self, page: Page):
        page.goto(self.PATH)
        dd = DropdownComponent(page)
        options = dd.get_all_options("#dropdown")
        assert "Option 1" in options
        assert "Option 2" in options


class TestFileUpload:
    PATH = f"{BASE}/upload"

    def test_upload_file(self, page: Page, tmp_path: Path):
        upload_file = tmp_path / "test_upload.txt"
        upload_file.write_text("playwright upload test")

        page.goto(self.PATH)
        form = FormComponent(page)
        form.upload_file("#file-upload", str(upload_file))
        form.submit("#file-submit")

        expect(page.locator("#uploaded-files")).to_have_text("test_upload.txt")
