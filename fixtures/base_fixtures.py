import pytest

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

# Python port of fixtures/basetest.ts: separate, independently-injectable fixtures rather than
# TS's single test.extend() object, since that's the idiomatic pytest way to compose fixtures.


@pytest.fixture
def base_page(page):
    return BasePage(page)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)


@pytest.fixture
def user_credentials():
    return {"username": "testadmin", "password": "Vibetestq@123#"}
