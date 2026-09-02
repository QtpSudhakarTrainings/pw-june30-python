from tamash_playwright import expect

# Python port of tests/4cssselectors.spec.ts — a plain CSS-selector locator demo (page.locator()
# with attribute and :has-text() selectors) rather than getBy* locators.


def test_explain_locators(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/auth/login")
    page.locator("input[name='username']").fill("testadmin")
    page.locator("input[placeholder='Password']").fill("Vibetestq@123#")
    page.locator("button:has-text('Login')").click()
    expect(page.locator("h6:has-text('Dashboard')")).to_be_visible()
