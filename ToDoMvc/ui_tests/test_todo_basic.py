import pytest
from playwright.sync_api import  expect

from ToDoMvc.ui_tests.base_test import BaseTest
from ToDoMvc.pages.todo_page import TodoPage

class TestToDo(BaseTest):

    def test_add_item(self):
        todo_page = TodoPage(self.page)
        item_name='item1'
        todo_page.add_item(item_name)
        todo_page.expect_items([item_name])

    def test_insert_and_find_items(self):
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2"])
        todo.expect_items(["item1", "item2"])

        item2 = todo.item_by_title("item2")
        item2.get_by_role("checkbox", name="Toggle Todo").check()
        todo.expect_items(["item1", "item2"])
        print(f"debug")

    def test_insert_and_find_checked_items(self):
        #page.goto(os.environ["BASE_URL_FE"])
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2"])
        todo.expect_items(["item1", "item2"])

        item1 = todo.item_by_title("item1")
        item1.get_by_role("checkbox", name="Toggle Todo").check()
        item2 = todo.item_by_title("item2")
        item2.get_by_role("checkbox", name="Toggle Todo").check()

        todo.expect_items(["item1", "item2"])

    def test_insert_and_check_and_uncheck(self):
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2"])
        todo.expect_items(["item1", "item2"])
        # check item1
        todo.toggle_item("item1")
        # uncheck item1
        box=todo.toggle_item("item1")
        expect(box).not_to_have_class("completed")
        todo.expect_items(["item1", "item2"])

    def test_insert_item_than_delete(self):
        title="item1"
        todo = TodoPage(self.page)
        todo.add_items([title])
        todo.expect_items([title])
        todo.item_by_title("item1").click()
        todo.delete_item(title)
        todo.expect_items([])

    @pytest.mark.parametrize('item, expected_inserted_item', [
        ('item1', 'item1'),
        ('item2', 'item2')
    ])
    def test_forms(self, item,expected_inserted_item):
        todo = TodoPage(self.page)
        todo.add_item(item)
        todo.expect_items([expected_inserted_item])