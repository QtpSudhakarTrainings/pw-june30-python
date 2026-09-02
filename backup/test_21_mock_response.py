import json

from tamash_playwright import expect

# Python port of tests/21MockResponse.spec.ts. Exercises route.fetch() + route.fulfill() with a
# modified body — route.fulfill() is one of the terminal methods tamash-playwright's route
# tracking watches for, so this also confirms fetching the real response first doesn't interfere
# with that.
#
# Deliberately omits the original's trailing page.pause() — that opens the interactive Playwright
# Inspector and blocks forever waiting for a human, which would hang an automated test run.


def test_mock_response_from_api_called_from_ui(page):
    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill("testadmin")
    page.get_by_placeholder("Password").fill("Vibetestq@123#")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    page.get_by_text("PIM").click()

    page.locator("//label[text()='Employee Id']/../..//input").fill("0010")

    def handle_route(route):
        response = route.fetch()
        body = response.json()
        print(json.dumps(body))

        body["data"][0]["employeeId"] = "0011"
        modified_body = json.dumps(body)

        route.fulfill(response=response, body=modified_body)
        print(modified_body)

    page.route("**/api/v2/pim/employees*", handle_route)

    page.locator("//button[normalize-space()='Search']").click()

    expect(page.get_by_text("Record Found")).to_be_visible()
