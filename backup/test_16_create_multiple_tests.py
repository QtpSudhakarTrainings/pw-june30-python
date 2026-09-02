import time

import pytest

from tamash_playwright import expect
from tamash_playwright.bindings import bind_page

# Python port of tests/16CreateMultipleTests.spec.ts. TS uses test.describe.configure({mode:
# 'serial'}) plus beforeAll/afterAll to share one Page across ordered tests; a class-scoped
# fixture is the pytest equivalent — pytest already runs a class's tests in definition order
# within one worker, so no extra "serial" configuration is needed. bind_page() is called
# explicitly here since this page is created directly from `browser`, bypassing the `page`
# fixture (and therefore bind_context()) entirely.


@pytest.fixture(scope="class")
def shared_page(browser):
    page = browser.new_page()
    bind_page(page)
    yield page
    page.close()


class TestGroupSerial:
    def test_login(self, shared_page):
        shared_page.goto("https://vibetestq-osondemand.orangehrm.com/")

        shared_page.get_by_placeholder("Username").fill("testadmin")
        shared_page.get_by_placeholder("Password").fill("Vibetestq@123#")
        shared_page.get_by_role("button", name="Login").click()

        expect(shared_page.get_by_role("heading", name="Dashboard")).to_be_visible()

    def test_add_employee(self, shared_page):
        shared_page.get_by_text("PIM").click()

        expect(shared_page.get_by_role("heading", name="Employee Information")).to_be_visible()

        shared_page.get_by_role("button", name="Add").click()

        first_name = "test"
        shared_page.get_by_placeholder("First Name").fill(first_name)

        last_name = f"user{int(time.time() * 1000)}"
        shared_page.get_by_placeholder("Last Name").fill(last_name)

        shared_page.get_by_role("button", name="Save").click()

        expect(shared_page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=10000)
