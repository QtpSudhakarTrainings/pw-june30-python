from tamash_playwright import expect

# Python port of tests/20CaptureResponse.spec.ts. page.on("request"/"response", ...) isn't
# special-cased by tamash-playwright the way "dialog"/"download" are — it passes straight
# through the patched .on() unchanged, so this also verifies that patch doesn't interfere with
# other event names.


def test_capture_response_from_api_called_from_ui(page):
    def on_request(request):
        if "api/v2" in request.url:
            print(f"Request URL is : {request.url}")
            print(f"Request method is : {request.method}")
            print(f"Request headers are : {request.headers}")
            print(f"Request post data is : {request.post_data}")

    def on_response(response):
        if "api/v2" in response.url:
            print(f"Request URL is : {response.request.url}")
            print(f"Response status code is : {response.status}")

    page.on("request", on_request)
    page.on("response", on_response)

    page.goto("https://vibetestq-osondemand.orangehrm.com/")

    page.get_by_placeholder("Username").fill("testadmin")
    page.get_by_placeholder("Password").fill("Vibetestq@123#")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()

    page.get_by_text("PIM").click()
