import base64

# Python port of tests/APITests/11SampleAPITestErrorHandling.spec.ts.
#
# General error handling — covers 401 Unauthorized (no credentials sent at all, as distinct from
# 403 Forbidden which means "authenticated, but not allowed") and 404 for a route that doesn't
# exist at all.


def test_protected_endpoint_no_credentials_expect_401(api_request_context):
    response = api_request_context.get("http://localhost:5002/api/members")
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 401


def test_route_that_does_not_exist_expect_404(api_request_context):
    credentials = base64.b64encode(b"admin:admin").decode()
    response = api_request_context.get(
        "http://localhost:5002/api/nope",
        headers={"Authorization": f"Basic {credentials}"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert body["error"] == "not_found"
    assert "/api/nope" in body["message"]
