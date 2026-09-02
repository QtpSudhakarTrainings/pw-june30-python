from datetime import datetime

# Python port of tests/11AlertHandling.spec.ts. Exercises tamash-playwright's dialog tracking:
# page.once("dialog", ...) is wrapped so whichever terminal method the handler calls (here,
# dialog.accept()) shows up in the report, same as page.on("dialog", ...) does.
#
# Playwright Python's expect() only supports Locator/Page/APIResponse targets (unlike TS's
# Jest-style expect(), which accepts any value) — a plain dialog.message string uses a plain
# assert instead, which is the idiomatic Python equivalent.


def test_alert_handling(page):
    page.goto("https://www.apsrtconline.in/oprs-web/")

    from_city = "HYDERABAD"
    to_city = "VIJAYAWADA"

    current_date = datetime.now()
    current_month = current_date.strftime("%B")
    search_day = 30

    # page.once fires for exactly one dialog then removes itself — the idiom for a dialog whose
    # message changes each time it appears, rather than page.on() which stays registered.
    def expect_start_place_alert(dialog):
        print("Start place alert displayed")
        assert "Please select start place." in dialog.message
        dialog.accept()

    page.once("dialog", expect_start_place_alert)

    page.get_by_role("button", name="Check Availability").click()
    page.wait_for_timeout(1000)

    page.locator("#fromPlaceName").fill(from_city)
    page.locator(f"//span[text()='{from_city}']").click()

    def expect_end_place_alert(dialog):
        print("End place alert displayed")
        assert "Please select end place." in dialog.message
        dialog.accept()

    page.once("dialog", expect_end_place_alert)

    page.get_by_role("button", name="Check Availability").click()
    page.wait_for_timeout(1000)

    page.locator("#toPlaceName").fill(to_city)
    page.locator(f"//span[text()='{to_city}']").click()

    page.locator("#txtJourneyDate").click()

    page.locator(
        f'//div[contains(@class,"ui-datepicker-group") and contains(normalize-space(),"{current_month}")]'
        f"//a[text()={search_day}]"
    ).click()

    page.locator("#searchBtn").click()
