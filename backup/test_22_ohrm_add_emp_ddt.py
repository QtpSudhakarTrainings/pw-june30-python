import json
import time
from pathlib import Path

from tamash_playwright import expect

# Python port of tests/22ohrmaddempDDT.spec.ts. Nearly identical flow to test_02, but reads
# login credentials directly from testdata/users.json (json.load) rather than a fixture — the
# TS original imports users.json directly too, without going through basetest.ts/baseAppTest.ts.

_CREDS_PATH = Path(__file__).resolve().parent.parent / "testdata" / "users.json"


def test_orange_hrm_add_employee_with_json_creds(page):
    creds = json.loads(_CREDS_PATH.read_text(encoding="utf-8"))["userCreds"]

    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill(creds["adminCreds"]["username"])
    page.get_by_placeholder("Password").fill(creds["adminCreds"]["password"])
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    page.get_by_text("PIM").click()
    expect(page.get_by_role("heading", name="Employee Information")).to_be_visible()
    page.get_by_role("button", name="Add").click()

    first_name = "test"
    last_name = f"user{int(time.time() * 1000)}"

    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=10000)

    page.get_by_role("link", name="Admin").click()
    page.get_by_role("button", name="Add").click()

    page.get_by_text("-- Select --").first.click()
    page.get_by_role("listbox").get_by_text("Admin").click()

    page.get_by_placeholder("Type for hints...").fill(f"{first_name} {last_name}")
    page.get_by_role("listbox").get_by_text(f"{first_name} {last_name}").click()

    page.locator("//label[text()='Status']/../..//div[text()='-- Select --']").click()
    page.get_by_role("listbox").get_by_text("Enabled").click()

    page.locator("//label[text()='Username']/../..//input").fill(f"{first_name}{last_name}")

    page.locator("input[type=password]").first.fill("TestAdmin@123#")
    page.locator("input[type=password]").nth(1).fill("TestAdmin@123#")

    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Successfully Saved")).to_be_visible(timeout=10000)
    expect(page.get_by_role("heading", name="System Users")).to_be_visible(timeout=10000)

    page.get_by_alt_text("profile picture").click()
    page.get_by_text("Logout").click()

    page.get_by_placeholder("Username").fill(f"{first_name}{last_name}")
    page.get_by_placeholder("Password").fill("TestAdmin@123#")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
