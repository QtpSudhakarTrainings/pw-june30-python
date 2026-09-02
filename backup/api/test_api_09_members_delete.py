import base64

# Python port of tests/APITests/9SampleAPITestMembersDelete.spec.ts.
#
# DELETE /api/members/:id. Covers: default 204 No Content, verbose=true returning 200 with a
# body, 403 on the protected member (id 1), and 404 for an id that doesn't exist.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def test_delete_member_default_204_no_content(api_request_context):
    created = api_request_context.post(
        BASE_URL, headers=AUTH_HEADER, data={"name": "Delete Target", "gender": "male"}
    )
    member_id = created.json()["id"]

    response = api_request_context.delete(f"{BASE_URL}/{member_id}", headers=AUTH_HEADER)

    print(f"Status Code: {response.status}")

    assert response.status == 204
    assert len(response.body()) == 0

    # Confirm the member is actually gone.
    get_after_delete = api_request_context.get(f"{BASE_URL}/{member_id}", headers=AUTH_HEADER)
    assert get_after_delete.status == 404


def test_delete_member_verbose_returns_200_with_body(api_request_context):
    created = api_request_context.post(
        BASE_URL, headers=AUTH_HEADER, data={"name": "Verbose Delete Target", "gender": "female"}
    )
    member_id = created.json()["id"]

    response = api_request_context.delete(
        f"{BASE_URL}/{member_id}", headers=AUTH_HEADER, params={"verbose": "true"}
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 200
    assert str(member_id) in body["msg"]
    assert not any(member["id"] == member_id for member in body["members"])


def test_delete_protected_member_expect_403(api_request_context):
    response = api_request_context.delete(f"{BASE_URL}/1", headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 403
    assert "protected" in body["msg"]


def test_delete_id_that_does_not_exist_expect_404(api_request_context):
    response = api_request_context.delete(f"{BASE_URL}/9999", headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert "9999" in body["msg"]
