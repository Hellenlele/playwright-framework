from __future__ import annotations
from typing import Optional
from playwright.sync_api import Page, Locator


class TableComponent:
    def __init__(self, page: Page, table_selector: str):
        self.page = page
        self.table = page.locator(table_selector)

    def get_headers(self) -> list[str]:
        return self.table.locator("th").all_inner_texts()

    def get_row_count(self) -> int:
        return self.table.locator("tbody tr").count()

    def get_row(self, row_index: int) -> Locator:
        return self.table.locator("tbody tr").nth(row_index)

    def get_cell(self, row_index: int, col_index: int) -> str:
        return self.get_row(row_index).locator("td").nth(col_index).inner_text()

    def get_row_data(self, row_index: int) -> list[str]:
        return self.get_row(row_index).locator("td").all_inner_texts()

    def get_all_rows(self) -> list[list[str]]:
        count = self.get_row_count()
        return [self.get_row_data(i) for i in range(count)]

    def get_column_values(self, col_index: int) -> list[str]:
        count = self.get_row_count()
        return [self.get_cell(i, col_index) for i in range(count)]

    def find_row_by_text(self, text: str) -> Optional[Locator]:
        rows = self.table.locator("tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            if text in row.inner_text():
                return row
        return None

    def click_cell_action(self, row_index: int, col_index: int, link_text: str = None) -> None:
        cell = self.get_row(row_index).locator("td").nth(col_index)
        if link_text:
            cell.get_by_role("link", name=link_text).click()
        else:
            cell.locator("a").first.click()

    def sort_by_column(self, header_text: str) -> None:
        self.table.get_by_role("columnheader", name=header_text).click()
