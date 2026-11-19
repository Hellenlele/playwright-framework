from playwright.sync_api import Page, expect


class ModalComponent:
    def __init__(self, page: Page, modal_selector: str):
        self.page = page
        self.modal = page.locator(modal_selector)

    def is_open(self) -> bool:
        return self.modal.is_visible()

    def wait_until_open(self) -> None:
        expect(self.modal).to_be_visible()

    def wait_until_closed(self) -> None:
        expect(self.modal).to_be_hidden()

    def get_title(self, title_selector: str = "h3") -> str:
        return self.modal.locator(title_selector).inner_text()

    def get_body_text(self, body_selector: str = ".modal-body") -> str:
        return self.modal.locator(body_selector).inner_text()

    def confirm(self, confirm_selector: str = ".modal-footer button:first-child") -> None:
        self.modal.locator(confirm_selector).click()
        self.wait_until_closed()

    def cancel(self, cancel_selector: str = ".modal-footer button:last-child") -> None:
        self.modal.locator(cancel_selector).click()
        self.wait_until_closed()

    def close_by_x(self, close_selector: str = "button.close") -> None:
        self.modal.locator(close_selector).click()
        self.wait_until_closed()

    def close_by_escape(self) -> None:
        self.page.keyboard.press("Escape")
        self.wait_until_closed()
