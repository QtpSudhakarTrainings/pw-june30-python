from datetime import datetime

# Python port of tests/8apsrtc-bookbus.spec.ts. Inherits the original's real fragility as-is:
# bus_service_no="3279" is a specific service that may not run on the computed date, and the
# whole flow depends on live seat availability on a real external booking site — this can fail
# for reasons that have nothing to do with tamash-playwright.


def test_apsrtc_get_ac_bus_book(page):
    page.goto("https://www.apsrtconline.in/oprs-web/")

    from_city = "HYDERABAD"
    to_city = "VIJAYAWADA"

    current_month = datetime.now().strftime("%B")
    search_day = 24

    bus_service_no = "3279"

    page.locator("#fromPlaceName").fill(from_city)
    page.locator(f"//span[text()='{from_city}']").click()

    page.locator("#toPlaceName").fill(to_city)
    page.locator(f"//span[text()='{to_city}']").click()

    page.locator("#txtJourneyDate").click()
    page.locator(
        f'//div[contains(@class,"ui-datepicker-group") and contains(normalize-space(),"{current_month}")]'
        f"//a[text()={search_day}]"
    ).click()

    page.locator("#searchBtn").click()

    page.locator(
        f'//div[@class="srvceNO" and normalize-space()="{bus_service_no}"]/../..//input[@value="Select Seats"]'
    ).click()

    page.locator("#ForwardBoardId").select_option(index=1)
    page.locator("#ForwardDroppingId").select_option(index=1)

    page.locator('input[value="Show layout"]').click()

    page.locator('li[class^="availSeatClass"]').first.click()

    page.locator("#mobileNo").fill("1234567890")
    page.locator("#email").fill("test@vibetestq.com")
    page.locator("#genderCodeIdForward0").select_option(index=1)

    page.locator("#passengerNameForward0").fill("Test User")
    page.locator("#passengerAgeForward0").fill("30")
    page.locator("#concessionIdsForward0").select_option(index=1)

    page.locator('input[value="Continue"]').click()
