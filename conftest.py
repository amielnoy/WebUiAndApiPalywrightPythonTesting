import os
from dotenv import load_dotenv
import pytest
from api_tests.api_client import APIClient

@pytest.fixture(scope="session")
def api_json_placeholder():
    return APIClient(os.getenv('BASE_URL_API_JPH'))

@pytest.fixture(scope="session")
def api_json_dummy():
    return APIClient(os.getenv('BASE_URL_API_JSON_DUMMY'))

@pytest.fixture(scope='session',autouse=True)
def base_url_fe(load_env):
    return os.getenv('BASE_URL_FE')

@pytest.fixture(scope='session',autouse=True)
def load_env():
    load_dotenv()
# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": False,
#         "slow_mo": 250  # מאט את הפעולות כדי שתוכל לראות מה קורה
#     }