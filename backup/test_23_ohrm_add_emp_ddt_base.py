import time

from tamash_playwright import expect

# Python port of tests/23ohrmaddempDDTBAse.spec.ts. Exercises the App/AppData fixtures (a
# SimpleNamespace-based port of baseAppTest.ts's grouped fixtures) and Excel-driven data-driven
# testing via DataUtils/excel_data_util.py. Each Excel row creates an employee, promotes them to
# an Admin-role system user, logs out, and logs back in as that new user before the next row.
#
# Deviates from the original in one way: the TS version searches the "Type for hints..."
# autocomplete for the plain Excel firstname/lastname, which — against this shared, persistent
# remote demo — accumulates a same-named employee from every prior run, eventually resolving to
# several identical matches (a real strict-mode violation this session's testing surfaced, no
# selector strategy can disambiguate "5 elements that all say John Doe"). A per-run numeric
# suffix on the last name keeps every run's full name unique and searchable.


def test_orange_hrm_add_employee_ddt(page, App, AppData):
    App.base_page.navigate_to("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill(AppData.admin_creds["username"])
    page.get_by_placeholder("Password").fill(AppData.admin_creds["password"])
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    for row in AppData.excel_data:
        page.get_by_text("PIM").click()
        expect(page.get_by_role("heading", name="Employee Information")).to_be_visible()
        page.get_by_role("button", name="Add").click()

        first_name = row["firstname"]
        last_name = f"{row['lastname']}{int(time.time() * 1000) % 100000}"

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
