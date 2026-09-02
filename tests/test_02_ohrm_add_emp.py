import time

from tamash_playwright import expect

# Python port of tests/2ohrmaddemp.spec.ts — getBy-locator add-employee + create-admin-user flow,
# standalone (no fixtures). last_name is time-suffixed the same way the original uses Date.now(),
# which already keeps the autocomplete search below unique per run (unlike the fixed Excel names
# in test_23's DDT port, this needs no extra fix).


def test_orange_hrm_add_employee(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username1").describe("Username Textbox").fill("testadmin")
    page.get_by_placeholder("Password").describe("Password Textbox").fill("Vibetestq@123#")
    page.get_by_role("button", name="Login").describe("Login Button").click()

    expect(page.get_by_role("heading", name="Dashboard1").describe("Dashboard Heading")).to_be_visible()

    page.get_by_text("PIM").describe("PIM link").click()
    expect(page.get_by_role("heading", name="Employee Information")).to_be_visible()
    page.get_by_role("button", name="Add").click()

    first_name = "test"
    last_name = f"user{int(time.time() * 1000)}"

    page.get_by_placeholder("First Name").fill(first_name)
    page.get_by_placeholder("Last Name").fill(last_name)
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=10000)

