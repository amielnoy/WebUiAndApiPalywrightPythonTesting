import re

from playwright.sync_api import Page, expect
# page_objects/todo_page.py
from playwright.sync_api import Page

class TodoPage:
    TOGGLE_TODO="Toggle Todo"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo = page.get_by_placeholder("What needs to be done?")
        self.list = page.locator("ul.todo-list")
        self.items = self.list.get_by_test_id("todo-item")
        self.item_titles = self.items.get_by_test_id("todo-title")
        self.all_link = page.get_by_role("link", name="All", exact=True)
        self.completed_link = page.get_by_role("link", name="Completed", exact=True)
        self.active_link = page.get_by_role("link", name="Active", exact=True)
        self.clear_completed_btn = page.locator("footer .clear-completed")

    def add_item(self, text: str) -> None:
        self.new_todo.fill(text)
        self.new_todo.press("Enter")

    def add_items(self, texts: list[str]):
        for t in texts:
            self.add_item(t)

    def item_by_title(self, title: str):
        return self.items.filter(has_text=title)

    def expect_items(self, titles: list[str]):
        expect(self.item_titles,"not all expected found").to_have_text(titles)
        expect(self.items,"the item count is different than expected").to_have_count(len(titles))

    def toggle_item(self, title: str):
        box=self.page.get_by_role("listitem").filter(has_text=title).get_by_label("Toggle Todo")
        if box.is_checked():
            box.uncheck()
        else:
            box.check()
        return box

    def delete_item(self,title):
        delete_item = self.page.get_by_role("listitem").filter(has_text=title).get_by_label("Delete")
        delete_item.click()
    def remove_item(self, title: str):
        item = self.item_by_title(title)
        item.get_by_role("checkbox", name="Toggle Todo").uncheck()
        expect(item).not_to_have_class("completed")

    def clear_completed(self):
        self.active_link.click()
        expect(self.items).not_to_have_class("completed")

    def click_all(self):
        self.all_link.click()

    def click_active(self):
        self.active_link.click()

    def click_completed(self):
        self.completed_link.click()

    def click_clear_completed(self):
        self.clear_completed_btn.click()


