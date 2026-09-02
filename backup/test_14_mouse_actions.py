# Python port of tests/14MouseActions.spec.ts. TS groups these under test.describe("mouse
# actions") purely for organization — a shared file already provides that grouping in pytest, so
# no equivalent wrapper is needed.


def test_mouse_actions_double_click(page):
    page.goto("https://api.jquery.com/dblclick/")

    frame = page.frame_locator("div.code-demo iframe")
    target = frame.locator('//span[text()="Double click the block"]/../div').describe("Double-click Demo Block")

    target.scroll_into_view_if_needed()
    target.highlight()

    page.wait_for_timeout(2000)

    target.dblclick()
    page.wait_for_timeout(2000)

    target.dblclick()
    page.wait_for_timeout(2000)


def test_mouse_actions_right_click(page):
    page.goto("https://swisnl.github.io/jQuery-contextMenu/demo.html")

    page.wait_for_timeout(1000)
    page.locator("//span[text()='right click me']").click(button="right")
    page.wait_for_timeout(2000)


def test_mouse_actions_hover(page):
    page.goto("https://api.jquery.com/mouseover/")

    frame = page.frame_locator("div.code-demo iframe")
    # .nth(0) rather than .first — a real method call, so it's actually healable/reported, unlike
    # .first (a Python property; see bindings.py's _CHAIN_METHODS comment for why that gap exists).
    target = frame.locator("div.in").nth(0).describe("Hover Demo Block")

    target.scroll_into_view_if_needed()
    page.wait_for_timeout(2000)
    target.hover()
    page.wait_for_timeout(2000)
