import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect


class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self, page,base_url_fe):
        self.page = page
        self.base_url_fe = base_url_fe
        self.page.goto(self.base_url_fe)