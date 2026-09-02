from tamash_playwright import expect

# Python port of tests/13DragAroud.spec.ts. drag_to() with target_position exercises the same
# iframe-scoped patching as the frame-handling test, plus Locator.drag_to()'s coordinate-offset
# option.


def test_handling_drag_and_drop(page):
    page.goto("https://jqueryui.com/draggable/")
    expect(page.get_by_role("heading", name="Draggable")).to_be_visible()

    frame = page.frame_locator("iframe.demo-frame")

    page.wait_for_timeout(2000)

    drag_elm = frame.locator("#draggable").describe("Draggable Element")

    drag_elm.drag_to(frame.locator("body"), target_position={"x": 181, "y": 50})

    page.wait_for_timeout(5000)
