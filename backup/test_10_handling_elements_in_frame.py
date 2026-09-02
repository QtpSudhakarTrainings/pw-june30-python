from tamash_playwright import expect

# Python port of tests/10HandlingElementsInFrame.spec.ts. Exercises tamash-playwright's iframe
# support: page.frame_locator() is patched (recursively) so a Locator resolved inside the iframe
# still gets healing/reporting, scoped correctly to the frame rather than the outer page.


def test_handling_elements_in_other_frames(page):
    page.goto("https://jqueryui.com/droppable/")
    expect(page.get_by_role("heading", name="Droppable")).to_be_visible()

    frame = page.frame_locator("iframe.demo-frame")

    page.wait_for_timeout(2000)

    drag_elm = frame.locator("#draggable").describe("Draggable Element")
    drop_elm = frame.locator("#droppable").describe("Droppable Element")

    drag_elm.drag_to(drop_elm)

    page.wait_for_timeout(5000)
