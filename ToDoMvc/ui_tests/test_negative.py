import sys

from playwright.sync_api import Page, expect

from ToDoMvc.pages.todo_page import TodoPage
from ToDoMvc.ui_tests.base_test import BaseTest


class TestNegative(BaseTest):
    def test_cannot_add_empty_or_spaces(self):
        todo = TodoPage(self.page)

        # Press Enter on empty input → no items
        todo.new_todo.press("Enter")
        todo.expect_items([])

        # Spaces-only should also be ignored
        todo.new_todo.fill("   ")
        todo.new_todo.press("Enter")
        todo.expect_items([])

    def test_trims_whitespace_on_add(self):
        todo = TodoPage(self.page)

        todo.add_item("   item1   ")
        # Title should appear trimmed (implementation-dependent in some apps;
        # in TodoMVC demo it’s trimmed)
        todo.expect_items(["item1"])

    def test_edit_esc_cancels_changes(self):
        todo = TodoPage(self.page)
        todo.new_todo.fill("item1")
        edit=todo.new_todo
        edit.dblclick()
        edit.fill("edited_item1")

        undo = "Meta+Z" if sys.platform == "darwin" else "Control+Z"
        edit.press(undo)  # cancel edit
        edit.press("Enter")
        # Text should remain the original value
        todo.expect_items(["item2"])



    def test_xss_is_not_executed_and_is_rendered_as_text(self):
        todo = TodoPage(self.page)

        xss = '<img src=x onerror=alert(1)>'
        dialog_fired = {"seen": False}
        def _no_dialog(dlg):
            dialog_fired["seen"] = True
            dlg.dismiss()

        self.page.on("dialog", _no_dialog)

        todo.add_item(xss)

        # Should render as literal text (not create an <img> tag / not execute JS)
        # 1) no dialog fired
        assert dialog_fired["seen"] is False, "XSS executed (dialog appeared)"

        # 2) text equals the raw string
        titles = todo.item_by_title(xss)
        assert titles.all_text_contents() == [xss]

        # 3) no <img> elements were injected into the list
        expect(todo.list.locator("img")).to_have_count(0)

    def test_clear_completed_is_hidden_when_nothing_completed(self):
        todo = TodoPage(self.page)
        todo.add_items(["a", "b"])

        # No completed items → "Clear completed" should not be visible
        expect(todo.clear_completed_btn).not_to_be_visible()