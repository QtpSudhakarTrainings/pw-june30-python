from tamash_playwright import expect

# Python port of tests/9HandlingElementsInOtherPages.spec.ts. Exercises bind_context(): the new
# page opened by clicking "OrangeHRM, Inc" (a target="_blank" link) is expected to already be
# healing/reporting-wrapped with no explicit bind_page() call, purely from the context's own
# "page" event listener set up when the primary `page` fixture ran.


def test_handling_elements_in_other_pages(page, context):
    page.goto("https://vibetestq-osondemand.orangehrm.com/auth/login")
    expect(page.get_by_alt_text("company-branding")).to_be_visible()

    with context.expect_page() as new_page_info:
        page.get_by_role("link", name="OrangeHRM, Inc").click()
    new_page = new_page_info.value

    opened_pages = context.pages
    print(f"number of opened pages: {len(opened_pages)}")
    for opened_page in opened_pages:
        print(opened_page.title())

    new_page.get_by_placeholder("Your email address").fill("test@vibetestq.com")
    new_page.wait_for_timeout(3000)

    page.bring_to_front()
    page.get_by_placeholder("Username").fill("Admin")
    page.wait_for_timeout(3000)
