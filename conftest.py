import os

import pytest
from dotenv import load_dotenv

load_dotenv()

# The reliable way to guarantee tamash-playwright's self-healing `page` fixture wins over
# pytest-playwright's own — pytest always prefers a conftest.py fixture over a same-named
# plugin fixture.
from tamash_playwright.plugin import page  # noqa: F401,E402

pytest_plugins = [
    "fixtures.base_fixtures",
    "fixtures.base_app_fixtures",
]


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("APP_BASE_URL", "https://qtpsudhakar-vibetestq-hrm.up.railway.app/")


@pytest.fixture(scope="session")
def api_base_url():
    return os.environ.get("API_BASE_URL", "http://localhost:5002/api/")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "headless": False, "args": ["--start-maximized"]}
