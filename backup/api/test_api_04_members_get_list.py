import base64

from tamash_playwright import expect

# Python port of tests/APITests/4SampleAPITestMembersGetList.spec.ts.
#
# GET /api/members - list endpoint. Covers: query parameters (gender/sort/sortBy/page/limit),
# response headers (ETag, Cache-Control, Last-Modified, Expires, X-Visit-Count), cookies (the
# "visits" counter cookie), content negotiation via the Accept header, and the 404 returned when
# a filter matches nothing.
#
# Status checks use expect(response).to_be_ok() where only "did this succeed" matters (standard
# Playwright APIResponseAssertions — verified it only has to_be_ok()/not_to_be_ok(), a 200-299
# range check, nothing status-code-specific) so those checks show up in the report. Everywhere a
# *specific* code is the point of the test (404 here), plain assert stays — to_be_ok() can't tell
# 404 apart from any other non-2xx, so it would silently accept a regression to the wrong error
# code. Playwright's expect() also can't take plain values at all (numbers, strings, lists) —
# unlike TS's Jest-style expect() — so body/header-field checks stay plain assert regardless.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def test_get_all_members_default(api_request_context):
    response = api_request_context.get(BASE_URL, headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert isinstance(body, list)
    assert len(body) > 0


def test_get_members_filtered_by_gender_sorted_descending(api_request_context):
    response = api_request_context.get(
        BASE_URL,
        headers=AUTH_HEADER,
        params={"gender": "male", "sort": "desc", "sortBy": "name"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert len(body) > 0
    for member in body:
        assert member["gender"].lower() == "male"

    names = [member["name"] for member in body]
    assert names == sorted(names, reverse=True)


def test_get_members_with_pagination(api_request_context):
    response = api_request_context.get(BASE_URL, headers=AUTH_HEADER, params={"page": "1", "limit": "2"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert len(body["data"]) <= 2
    assert body["pagination"]["currentPage"] == 1
    assert body["pagination"]["limit"] == 2


def test_get_members_unknown_gender_expect_404(api_request_context):
    response = api_request_context.get(BASE_URL, headers=AUTH_HEADER, params={"gender": "unknown"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert "unknown" in body["msg"]


def test_get_all_members_inspect_caching_headers(api_request_context):
    response = api_request_context.get(BASE_URL, headers=AUTH_HEADER)
    headers = response.headers

    print(f"ETag: {headers.get('etag')}")
    print(f"Cache-Control: {headers.get('cache-control')}")
    print(f"Last-Modified: {headers.get('last-modified')}")
    print(f"Expires: {headers.get('expires')}")
    print(f"X-Visit-Count: {headers.get('x-visit-count')}")

    expect(response).to_be_ok()
    assert headers.get("etag")
    assert headers.get("cache-control") == "public, max-age=10"
    assert headers.get("last-modified")
    assert headers.get("expires")
    assert int(headers.get("x-visit-count")) > 0


def test_get_all_members_twice_visit_count_increments(api_request_context):
    # The APIRequestContext persists cookies automatically between calls made with the same
    # api_request_context fixture, so the second call sends back the "visits" cookie the first
    # call set.
    first = api_request_context.get(BASE_URL, headers=AUTH_HEADER)
    first_count = int(first.headers["x-visit-count"])
    print(f"First X-Visit-Count: {first_count}")

    second = api_request_context.get(BASE_URL, headers=AUTH_HEADER)
    second_count = int(second.headers["x-visit-count"])
    print(f"Second X-Visit-Count: {second_count}")

    assert second_count == first_count + 1


def test_get_all_members_content_negotiation_xml(api_request_context):
    response = api_request_context.get(BASE_URL, headers={**AUTH_HEADER, "Accept": "application/xml"})
    text = response.text()

    print(text)
    print(f"Content-Type: {response.headers.get('content-type')}")

    expect(response).to_be_ok()
    assert "application/xml" in response.headers.get("content-type", "")
    assert text.strip().startswith("<?xml")
    assert "<members>" in text


def test_get_all_members_content_negotiation_html(api_request_context):
    response = api_request_context.get(BASE_URL, headers={**AUTH_HEADER, "Accept": "text/html"})
    text = response.text()

    print(text)
    print(f"Content-Type: {response.headers.get('content-type')}")

    expect(response).to_be_ok()
    assert "text/html" in response.headers.get("content-type", "")
    assert "<table" in text


def test_get_all_members_content_negotiation_csv(api_request_context):
    response = api_request_context.get(BASE_URL, headers={**AUTH_HEADER, "Accept": "text/plain"})
    text = response.text()

    print(text)
    print(f"Content-Type: {response.headers.get('content-type')}")

    expect(response).to_be_ok()
    assert "text/plain" in response.headers.get("content-type", "")
    assert text.split("\n")[0] == "id,name,gender"
