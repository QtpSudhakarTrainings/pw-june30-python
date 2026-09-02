import time

from tamash_playwright import expect

# Python port of tests/6OhrmAddEmpAdmin.spec.ts — the same add-employee/create-admin-user flow
# as test_02, but built almost entirely from raw CSS and XPath locators instead of getBy*, to
# exercise page.locator() specifically (heavier CSS/XPath coverage than the getBy-based ports).


def test_orange_hrm_add_employee_using_css_and_xpath(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.locator('input[placeholder="Username"]').fill("testadmin")
    page.locator('//input[@placeholder="Password"]').fill("Vibetestq@123#")
    page.locator("//button[normalize-space()='Login']").click()

    expect(page.locator("//h6[normalize-space()='Dashboard']")).to_be_visible()

    page.locator("//a[normalize-space()='PIM']").click()
    page.locator("//button[normalize-space()='Add']").click()

    first_name = "test"
    page.locator('input[placeholder="First Name"]').fill(first_name)

    last_name = f"user{int(time.time() * 1000)}"
    page.locator('input[placeholder="Last Name"]').fill(last_name)

    emp_id = page.locator("//label[text()='Employee Id']/../..//input").input_value()
    print(f"Employee ID is : {emp_id}")

    page.locator("//button[normalize-space()='Save']").click()

    expect(page.locator("//h6[normalize-space()='Personal Details']")).to_be_visible(timeout=10000)

    page.locator("//a[normalize-space()='Admin']").click()
    page.locator("//button[normalize-space()='Add']").click()

    page.locator("//label[text()='User Role']/following::div[text()='-- Select --'][1]").click()
    page.locator("//div[@role='listbox']//span[text()='Admin']").click()

    full_name = f"{first_name} {last_name}"
    page.locator('input[placeholder="Type for hints..."]').fill(full_name)

    page.locator(f"//div[@role='listbox']//span[contains(text(),'{last_name}')]").click()

    page.locator("//label[text()='Status']/../..//div[text()='-- Select --']").click()
    page.locator("//div[@role='listbox']//span[text()='Enabled']").click()

    page.locator("//label[text()='Username']/following::input[1]").fill(f"{first_name}{last_name}")
    page.locator("//label[text()='Password']/../..//input").fill("Vibetestq@123#")
    page.locator("//label[text()='Confirm Password']/../..//input").fill("Vibetestq@123#")

    page.locator("//button[normalize-space()='Save']").click()

    expect(page.get_by_text("successful")).to_be_visible(timeout=10000)
