import base64
import random
import string

from tamash_playwright import expect

# Python port of tests/APITests/8SampleAPITestMembersPatch.spec.ts.
#
# PATCH /api/members/:id - partial update. Covers: updating just one field at a time, 400 when
# the body is empty, and 403 on the protected member (id 1).
#
# Names are per-run unique — this server persists data across runs (confirmed: "Patch Target"
# from an earlier run caused a 409 Conflict here), same lesson as the other members_* ports.
# Letters only in the suffix: this server's own validation rejects digits in a name.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def _unique_name(base: str) -> str:
    suffix = "".join(random.choices(string.ascii_uppercase, k=5))
    return f"{base} {suffix}"


def test_patch_update_only_gender(api_request_context):
    name = _unique_name("Patch Target")
    created = api_request_context.post(BASE_URL, headers=AUTH_HEADER, data={"name": name, "gender": "male"})
    member_id = created.json()["id"]

    response = api_request_context.patch(f"{BASE_URL}/{member_id}", headers=AUTH_HEADER, data={"gender": "female"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert body["member"]["id"] == member_id
    assert body["member"]["name"] == name
    assert body["member"]["gender"] == "female"


def test_patch_update_only_name(api_request_context):
    created = api_request_context.post(
        BASE_URL, headers=AUTH_HEADER, data={"name": _unique_name("Rename Target"), "gender": "male"}
    )
    member_id = created.json()["id"]

    renamed = _unique_name("Renamed Member")
    response = api_request_context.patch(f"{BASE_URL}/{member_id}", headers=AUTH_HEADER, data={"name": renamed})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert body["member"]["id"] == member_id
    assert body["member"]["name"] == renamed
    assert body["member"]["gender"] == "male"


def test_patch_with_empty_body_expect_400(api_request_context):
    response = api_request_context.patch(f"{BASE_URL}/3", headers=AUTH_HEADER, data={})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 400
    assert "at least a name or gender" in body["msg"]


def test_patch_on_protected_member_expect_403(api_request_context):
    response = api_request_context.patch(f"{BASE_URL}/1", headers=AUTH_HEADER, data={"name": "Hacker Name"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 403
    assert "protected" in body["msg"]
