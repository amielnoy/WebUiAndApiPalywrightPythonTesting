import random

import pytest
from playwright.sync_api import  expect

from ToDoMvc.ui_tests.base_test import BaseTest
from ToDoMvc.pages.todo_page import TodoPage

class TestToDo(BaseTest):
    def pick_random(self,a: str, b: str) -> str:
        return random.choice([a, b])
    def test_insert_item_than_delete(self):
        title1 = "item1"
        title2 = "item2"
        items_to_add=[title1, title2]
        todo = TodoPage(self.page)
        todo.add_items(items_to_add)
        todo.expect_items(items_to_add)
        count_before=todo.items.count()
        to_complete = self.pick_random(title1, title2)
        todo.toggle_item(to_complete)
        self.completed_items = todo.list.locator("li.completed")
        count_after=self.completed_items.count()
        assert (count_before-count_after)==1
        for item in items_to_add:
            if item != to_complete:
                todo.item_by_title(item).click()
                todo.delete_item(item)
        todo.click_all()
        todo.expect_items([to_complete])

        todo.click_active()
        expect(todo.items).to_have_count(0)

        todo.click_completed()
        todo.expect_items([to_complete])



