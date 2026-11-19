from playwright.sync_api import Page


class FormComponent:
    def __init__(self, page: Page):
        self.page = page

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def fill_by_label(self, label: str, value: str) -> None:
        self.page.get_by_label(label).fill(value)

    def fill_by_placeholder(self, placeholder: str, value: str) -> None:
        self.page.get_by_placeholder(placeholder).fill(value)

    def tick_checkbox(self, selector: str, checked: bool = True) -> None:
        locator = self.page.locator(selector)
        if checked:
            locator.check()
        else:
            locator.uncheck()

    def select_radio(self, selector: str) -> None:
        self.page.locator(selector).check()

    def upload_file(self, selector: str, file_path: str) -> None:
        self.page.locator(selector).set_input_files(file_path)

    def submit(self, selector: str = 'button[type="submit"]') -> None:
        self.page.locator(selector).click()

    def get_validation_message(self, selector: str) -> str:
        return self.page.locator(selector).evaluate("el => el.validationMessage")

    def is_valid(self, selector: str) -> bool:
        return self.page.locator(selector).evaluate("el => el.validity.valid")
