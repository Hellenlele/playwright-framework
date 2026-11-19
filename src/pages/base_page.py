import re
from playwright.sync_api import Page, Locator, expect
from src.config.config import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(Config.TIMEOUT)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        self.page.goto(f"{Config.BASE_URL}{path}")

    def reload(self) -> None:
        self.page.reload()

    def go_back(self) -> None:
        self.page.go_back()

    def go_forward(self) -> None:
        self.page.go_forward()

    @property
    def url(self) -> str:
        return self.page.url

    @property
    def title(self) -> str:
        return self.page.title()

    # ── Locators ──────────────────────────────────────────────────────────────

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def get_by_role(self, role: str, **kwargs) -> Locator:
        return self.page.get_by_role(role, **kwargs)

    def get_by_label(self, label: str) -> Locator:
        return self.page.get_by_label(label)

    def get_by_placeholder(self, placeholder: str) -> Locator:
        return self.page.get_by_placeholder(placeholder)

    def get_by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    # ── Interactions ──────────────────────────────────────────────────────────

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def double_click(self, selector: str) -> None:
        self.page.locator(selector).dblclick()

    def right_click(self, selector: str) -> None:
        self.page.locator(selector).click(button="right")

    def type(self, selector: str, text: str) -> None:
        self.page.locator(selector).fill(text)

    def clear(self, selector: str) -> None:
        self.page.locator(selector).clear()

    def press(self, selector: str, key: str) -> None:
        self.page.locator(selector).press(key)

    def hover(self, selector: str) -> None:
        self.page.locator(selector).hover()

    def focus(self, selector: str) -> None:
        self.page.locator(selector).focus()

    def check(self, selector: str) -> None:
        self.page.locator(selector).check()

    def uncheck(self, selector: str) -> None:
        self.page.locator(selector).uncheck()

    def select_option(self, selector: str, value: str = None, label: str = None, index: int = None) -> None:
        locator = self.page.locator(selector)
        if label:
            locator.select_option(label=label)
        elif index is not None:
            locator.select_option(index=index)
        else:
            locator.select_option(value=value)

    def upload_file(self, selector: str, file_path: str) -> None:
        self.page.locator(selector).set_input_files(file_path)

    def drag_and_drop(self, source: str, target: str) -> None:
        self.page.drag_and_drop(source, target)

    # ── Reading values ────────────────────────────────────────────────────────

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def get_attribute(self, selector: str, attr: str) -> str:
        return self.page.locator(selector).get_attribute(attr)

    def get_value(self, selector: str) -> str:
        return self.page.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        return self.page.locator(selector).is_enabled()

    def is_checked(self, selector: str) -> bool:
        return self.page.locator(selector).is_checked()

    # ── Assertions (auto-retry via Playwright expect) ─────────────────────────

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_contains_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_value(self, selector: str, value: str) -> None:
        expect(self.page.locator(selector)).to_have_value(value)

    def expect_url(self, url: str) -> None:
        expect(self.page).to_have_url(url)

    def expect_url_contains(self, partial: str) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(partial)))

    def expect_title(self, title: str) -> None:
        expect(self.page).to_have_title(title)

    def expect_checked(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_checked()

    def expect_not_checked(self, selector: str) -> None:
        expect(self.page.locator(selector)).not_to_be_checked()

    def expect_enabled(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_enabled()

    def expect_disabled(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_disabled()

    def expect_count(self, selector: str, count: int) -> None:
        expect(self.page.locator(selector)).to_have_count(count)

    # ── Alerts / Dialogs ──────────────────────────────────────────────────────

    def accept_dialog(self, prompt_text: str = None) -> None:
        """Register a one-shot handler that accepts the next dialog."""
        def handler(dialog):
            if prompt_text:
                dialog.accept(prompt_text)
            else:
                dialog.accept()
        self.page.once("dialog", handler)

    def dismiss_dialog(self) -> None:
        self.page.once("dialog", lambda d: d.dismiss())

    # ── iFrames ───────────────────────────────────────────────────────────────

    def frame_locator(self, selector: str):
        return self.page.frame_locator(selector)

    # ── Scrolling ─────────────────────────────────────────────────────────────

    def scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_element(self, selector: str) -> None:
        self.page.locator(selector).scroll_into_view_if_needed()

    # ── JavaScript ────────────────────────────────────────────────────────────

    def execute_js(self, script: str, *args):
        return self.page.evaluate(script, *args)

    # ── Tabs / Windows ────────────────────────────────────────────────────────

    def open_new_tab(self) -> Page:
        return self.page.context.new_page()

    def wait_for_new_tab(self):
        """Use as context manager: `with self.wait_for_new_tab() as new_page`."""
        return self.page.context.expect_page()

    # ── Waiting ───────────────────────────────────────────────────────────────

    def wait_for_url(self, url: str) -> None:
        self.page.wait_for_url(url)

    def wait_for_selector(self, selector: str) -> None:
        self.page.wait_for_selector(selector)

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        self.page.wait_for_load_state(state)

    # ── Screenshot ────────────────────────────────────────────────────────────

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path, full_page=True)

    def screenshot_element(self, selector: str, path: str) -> None:
        self.page.locator(selector).screenshot(path=path)
