import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from DataUtils.excel_data_util import read_excel_file
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

# Python port of fixtures/baseAppTest.ts. TS groups related fixtures into two typed objects
# (App, AppData); SimpleNamespace gives the same dotted access (App.base_page, AppData.excel_data)
# without needing a dataclass per grouping.

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CREDS_PATH = _PROJECT_ROOT / "testdata" / "users.json"
_EXCEL_PATH = _PROJECT_ROOT / "FileData" / "employees.xlsx"


@pytest.fixture
def App(page):
    return SimpleNamespace(
        base_page=BasePage(page),
        login_page=LoginPage(page),
        dashboard_page=DashboardPage(page),
    )


@pytest.fixture
def AppData():
    creds = json.loads(_CREDS_PATH.read_text(encoding="utf-8"))["userCreds"]
    return SimpleNamespace(
        user_credentials=creds["guestCreds"],
        admin_creds=creds["adminCreds"],
        all_creds=creds,
        excel_data=read_excel_file(str(_EXCEL_PATH)),
    )
