import time
from pathlib import Path

from tamash_playwright import expect

# Python port of tests/15HandlingFileInputs.spec.ts. The original's filechooser flow used
# page.waitForEvent("filechooser") + a manual promise; Python's expect_file_chooser() context
# manager is the idiomatic equivalent (same pattern as expect_download()/expect_page()).

_DEMO_FILE = Path(__file__).resolve().parent.parent / "FileData" / "demo.txt"


def _select_list_item(page, list_name: str, list_option: str) -> None:
    page.locator(f"//label[text()='{list_name}']/../..//div[text()='-- Select --']").click()
    page.get_by_role("option", name=list_option).click()


def test_handling_file_inputs(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill("testadmin")
    page.get_by_placeholder("Password").fill("Vibetestq@123#")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    page.get_by_text("PIM").click()
    expect(page.get_by_role("heading", name="Employee Information")).to_be_visible()

    page.get_by_role("button", name="Add").click()

    first_name = "test"
    page.get_by_placeholder("First Name").fill(first_name)

    last_name = f"user{int(time.time() * 1000)}"
    page.get_by_placeholder("Last Name").fill(last_name)

    page.get_by_role("button", name="Save").click()

    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=10000)

    _select_list_item(page, "Nationality", "Indian")
    _select_list_item(page, "Marital Status", "Married")

    page.locator("//label[text()='Date of Birth']/../..//input[@placeholder='yyyy-mm-dd']").fill("2000-01-01")
    page.get_by_text("Male", exact=True).click()
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Successfully Updated")).to_be_visible()
    page.get_by_role("button", name="Add").click()

    with page.expect_file_chooser() as file_chooser_info:
        page.get_by_text("Browse").click()
    file_chooser = file_chooser_info.value
    file_chooser.set_files(str(_DEMO_FILE))

    page.locator("//h6[text()='Add Attachment']/..//button[normalize-space()='Save']").click()

    expect(page.get_by_text("Successfully Updated")).to_be_visible()

    page.wait_for_timeout(10)
