# Python port of tests/7apsrtc-getacbuscount.spec.ts. Uses a fixed date ("July 24") like the
# original — a real fragility inherited as-is from the TS source (this will eventually fall in
# the past and stop matching a selectable date). Exercises Locator.all() to iterate matches.


def test_apsrtc_get_ac_bus_count(page):
    page.goto("https://www.apsrtconline.in/oprs-web/")

    from_city = "HYDERABAD"
    to_city = "VIJAYAWADA"

    page.locator("#fromPlaceName").fill(from_city)
    page.locator(f"//span[text()='{from_city}']").click()

    page.locator("#toPlaceName").fill(to_city)
    page.locator(f"//span[text()='{to_city}']").click()

    page.locator("#txtJourneyDate").click()
    page.locator(
        '//div[contains(@class,"ui-datepicker-group") and contains(normalize-space(),"July")]//a[text()="24"]'
    ).click()

    page.locator("#searchBtn").click()

    page.locator("#BtFid").click()
    page.locator('//input[@name="A/C CLASS"]').click()

    all_ac_bus_services = page.locator("div.srvceNO:visible").all()

    print(f"Total AC Buses available from {from_city} to {to_city} on 24th July are : {len(all_ac_bus_services)}")

    for i, bus in enumerate(all_ac_bus_services):
        bus_service_name = bus.text_content()
        print(f"AC Bus Service {i + 1} : {bus_service_name.strip()}")
