# Python port of tests/12HadlingShadowDom.spec.ts. Shadow DOM content is only reachable via
# CSS/role/text-based locators (not XPath) — get_by_text()/get_by_placeholder() pierce shadow
# roots the same way Playwright's own CSS engine does, no special handling needed on our side.


def test_handling_shadow_dom_elements(page):
    page.goto("https://vibetestq.com/testweb/sandbox/")

    page.get_by_text("Drag, Drop & Shadow").click()
    page.get_by_placeholder("Type inside shadow DOM...").fill("hello shadow dom")

    page.wait_for_timeout(3000)
