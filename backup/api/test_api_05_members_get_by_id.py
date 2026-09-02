import base64

from tamash_playwright import expect

# Python port of tests/APITests/5SampleAPITestMembersGetById.spec.ts.
#
# GET /api/members/:id - single resource endpoint. Covers: path parameters, 404 for an unknown
# id, and conditional GET via the If-None-Match header (should return 304 Not Modified with no
# body when the ETag matches what the server currently has).
#
# expect(response).to_be_ok() for plain "did this succeed" checks (report-visible, standard
# Playwright API); plain assert stays wherever a *specific* code (404, 304) is the actual point
# of the test — to_be_ok()/not_to_be_ok() only check the 200-299 range, not an exact code.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def test_get_single_member_by_id(api_request_context):
    response = api_request_context.get(f"{BASE_URL}/3", headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert body[0]["id"] == 3


def test_get_member_with_unknown_id_expect_404(api_request_context):
    response = api_request_context.get(f"{BASE_URL}/9999", headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert "9999" in body["msg"]


def test_conditional_get_returns_304(api_request_context):
    # First call: capture the ETag the server computed for this member.
    first = api_request_context.get(f"{BASE_URL}/2", headers=AUTH_HEADER)
    etag = first.headers["etag"]
    print(f"ETag from first call: {etag}")

    expect(first).to_be_ok()
    assert etag

    # Second call: send that ETag back — since nothing changed, the server should skip
    # re-sending the body and reply 304 Not Modified instead.
    second = api_request_context.get(f"{BASE_URL}/2", headers={**AUTH_HEADER, "If-None-Match": etag})

    print(f"Status Code: {second.status}")

    assert second.status == 304
    second_body = second.body()
    assert len(second_body) == 0
