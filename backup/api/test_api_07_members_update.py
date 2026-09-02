import base64
import random
import string

from tamash_playwright import expect

# Python port of tests/APITests/7SampleAPITestMembersUpdate.spec.ts.
#
# PUT /api/members/:id - full replace. Covers: successful replace (requires BOTH name and
# gender), 400 when only one field is sent (PUT is not a partial update), 403 on the protected
# member (id 1), and 404 for an id that doesn't exist.
#
# Names are per-run unique (like the OrangeHRM DDT and members-create ports) — this server
# persists data across runs, and a fixed name risks colliding with a member a previous run left
# behind. Letters only in the suffix: this server's own validation rejects digits in a name.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def _unique_name(base: str) -> str:
    suffix = "".join(random.choices(string.ascii_uppercase, k=5))
    return f"{base} {suffix}"


def test_put_full_update_replace_name_and_gender(api_request_context):
    # Create a member first so we have a safe (non-protected) id to update.
    created = api_request_context.post(
        BASE_URL, headers=AUTH_HEADER, data={"name": _unique_name("Temp Member"), "gender": "male"}
    )
    member_id = created.json()["id"]

    updated_name = _unique_name("Updated Name")
    response = api_request_context.put(
        f"{BASE_URL}/{member_id}",
        headers=AUTH_HEADER,
        data={"name": updated_name, "gender": "female"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    expect(response).to_be_ok()
    assert body["member"]["id"] == member_id
    assert body["member"]["name"] == updated_name
    assert body["member"]["gender"] == "female"


def test_put_with_only_one_field_expect_400(api_request_context):
    response = api_request_context.put(f"{BASE_URL}/3", headers=AUTH_HEADER, data={"name": "New Name"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 400
    assert "PUT requires the full resource" in body["msg"]


def test_put_on_protected_member_expect_403(api_request_context):
    response = api_request_context.put(
        f"{BASE_URL}/1",
        headers=AUTH_HEADER,
        data={"name": "Hacker Name", "gender": "male"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 403
    assert "protected" in body["msg"]


def test_put_on_id_that_does_not_exist_expect_404(api_request_context):
    response = api_request_context.put(
        f"{BASE_URL}/9999",
        headers=AUTH_HEADER,
        data={"name": "Nobody Here", "gender": "male"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert "9999" in body["msg"]
