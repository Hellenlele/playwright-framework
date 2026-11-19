from playwright.sync_api import Page


class DropdownComponent:
    def __init__(self, page: Page):
        self.page = page

    # ── Native <select> ───────────────────────────────────────────────────────

    def select_by_label(self, selector: str, label: str) -> None:
        self.page.locator(selector).select_option(label=label)

    def select_by_value(self, selector: str, value: str) -> None:
        self.page.locator(selector).select_option(value=value)

    def select_by_index(self, selector: str, index: int) -> None:
        self.page.locator(selector).select_option(index=index)

    def get_selected(self, selector: str) -> str:
        return self.page.locator(selector).evaluate(
            "el => el.options[el.selectedIndex].text"
        )

    def get_all_options(self, selector: str) -> list[str]:
        return self.page.locator(selector).evaluate(
            "el => Array.from(el.options).map(o => o.text)"
        )

    # ── Custom / JS dropdowns ─────────────────────────────────────────────────

    def custom_open(self, trigger_selector: str) -> None:
        self.page.locator(trigger_selector).click()

    def custom_select(self, option_selector: str) -> None:
        self.page.locator(option_selector).click()

    def custom_select_by_text(self, trigger_selector: str, option_text: str) -> None:
        self.page.locator(trigger_selector).click()
        self.page.get_by_role("option", name=option_text).click()

    def custom_search_and_select(self, trigger_selector: str, search_input_selector: str, text: str) -> None:
        self.page.locator(trigger_selector).click()
        self.page.locator(search_input_selector).fill(text)
        self.page.get_by_role("option", name=text).click()
