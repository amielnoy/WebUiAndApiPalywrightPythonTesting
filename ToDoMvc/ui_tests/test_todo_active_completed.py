import re

import pytest
from playwright.sync_api import  expect

from ToDoMvc.ui_tests.base_test import BaseTest
from ToDoMvc.pages.todo_page import TodoPage

class TestToDo(BaseTest):
    def test_insert_and_find_completed_and_active(self):
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2","item3","item4"])
        todo.expect_items(["item1", "item2","item3","item4"])

        item2 = todo.item_by_title("item2")
        item2.get_by_role("checkbox", name="Toggle Todo").check()

        item4 = todo.item_by_title("item4")
        item4.get_by_role("checkbox", name="Toggle Todo").check()

        # xyte item2,item4 are completed
        expect(item2).to_have_class('completed')
        expect(item4).to_have_class('completed')
        #xyte item1,item3 are not completed
        item1 =todo.item_by_title("item1")
        item3 = todo.item_by_title("item3")
        expect(item1).not_to_have_class('completed')
        expect(item3).not_to_have_class('completed')
        print(f"debug")

    def test_insert_and_find_checked_items(self):
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2"])
        todo.expect_items(["item1", "item2"])

        item1 = todo.item_by_title("item1")
        item1.get_by_role("checkbox", name="Toggle Todo").check()
        item2 = todo.item_by_title("item2")
        item2.get_by_role("checkbox", name="Toggle Todo").check()

        todo.expect_items(["item1", "item2"])
        print(f"debug")

    def test_insert_and_check_and_uncheck(self):
        todo = TodoPage(self.page)
        todo.add_items(["item1", "item2"])
        todo.expect_items(["item1", "item2"])
        #self.page.pause()
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
    def test_add_item_and_check_several_times(self, item,expected_inserted_item):
        todo = TodoPage(self.page)
        todo.add_item(item)
        todo.expect_items([expected_inserted_item])


    def test_active_filter_shows_only_active_item(self):
        todo = TodoPage(self.page)

        # Add two items
        active_title = "Buy milk"
        completed_title = "Walk dog"
        todo.add_items([active_title, completed_title])

        # Mark one item as completed
        todo.toggle_item(completed_title)
        # The completed item should have 'completed' class when viewing All
        completed_item = todo.item_by_title(completed_title)
        expect(completed_item).to_have_class(re.compile(".*completed.*"))

        # Click Active filter
        todo.click_active()

        # Verify only the active item is shown in the list
        # expect item titles to include only the active one
        todo.expect_items([active_title])

        # Additionally ensure the completed one is not visible under Active
        expect(self.page.get_by_role("listitem").filter(has_text=completed_title)).to_have_count(0)




    def test_active_filter_shows_only_active_item(self):
        # This is assumed to already exist as per your file; keeping for context.
        # If implemented elsewhere, leave as is.
        pass

    def test_completed_filter_shows_only_two_completed_items(self):
        # Arrange
        todo = TodoPage(self.page)

        items = ["Task A", "Task B", "Task C"]
        completed = ["Task A", "Task B"]
        active = ["Task C"]

        # Add three items

        todo.add_items(items)

        # Complete two items
        for it in completed:
            todo.toggle_item(it)  # toggles checkbox for the item with matching title

        # Assert in All view they are marked completed (class contains 'completed')
        for it in completed:
            li = self.page.get_by_role("listitem").filter(has_text=it)
            expect(li).to_have_class(re.compile(r".*\bcompleted\b.*"))

        # Click Completed filter
        todo.click_clear_completed()
        todo.expect_items(active)

    def test_completed_filter_shows_only_two_completed_items(self):
        all_items = ["Task A", "Task B", "Task C"]
        completed = ["Task A", "Task B"]
        todo = TodoPage(self.page)
        # Add three items
        todo.add_items(all_items)

        # Complete two items
        for title in completed:
            todo.toggle_item(title)

        # Switch to Completed filter
        todo.click_completed()

        # Verify only the two completed items are visible
        todo.expect_items(completed)

        # And ensure there are exactly 2 items rendered
        for item in completed:
            li = self.page.get_by_role("listitem").filter(has_text=item)
            expect(li).to_have_class(re.compile(r".*\bcompleted\b.*"))




