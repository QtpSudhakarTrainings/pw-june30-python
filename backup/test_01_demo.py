# Python port of tests/1demo.spec.ts — the simplest possible smoke test.


def test_demo(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill("admin")
    page.get_by_placeholder("Password").fill("admin@123#")
    page.get_by_role("button", name="Login").click()

    page.wait_for_timeout(10000)
