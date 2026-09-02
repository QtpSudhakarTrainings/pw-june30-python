import base64

# Python port of tests/APITests/1SampleAPITestBasicAuth.spec.ts. Uses the api_request_context
# fixture (this package's own addition — see plugin.py — since pytest-playwright's Python
# package, unlike its TS counterpart, provides no standalone request-context fixture at all).


def test_api_login_with_basic_auth(api_request_context):
    credentials = base64.b64encode(b"admin:admin").decode()
    response = api_request_context.get(
        "http://localhost:5002/api/members",
        headers={"Authorization": f"Basic {credentials}"},
    )

    print(response.json())
    print(f"Status Code: {response.status}")
    print(f"Status Text: {response.status_text}")
    print(f"Headers: {response.headers}")


def test_api_login_with_x_api_key_header(api_request_context):
    response = api_request_context.get(
        "http://localhost:5002/api/members",
        headers={"x-api-key": "demo-api-key-12345"},
    )

    print(response.json())
    print(f"Status Code: {response.status}")
    print(f"Status Text: {response.status_text}")
    print(f"Headers: {response.headers}")


def test_api_login_with_bearer_token_jwt(api_request_context):
    response = api_request_context.post(
        "http://localhost:5002/api/auth/login",
        headers={"Content-Type": "application/json"},
        data={"username": "admin", "password": "admin"},
    )

    response_body = response.json()
    print(response_body)

    access_token = response_body["access_token"]

    protected_response = api_request_context.get(
        "http://localhost:5002/api/members",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print(protected_response.json())


def test_api_login_with_oauth2_client_credentials(api_request_context):
    response = api_request_context.post(
        "http://localhost:5002/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "demo-client",
            "client_secret": "demo-secret",
        },
    )

    response_body = response.json()
    print(response_body)

    access_token = response_body["access_token"]

    protected_response = api_request_context.get(
        "http://localhost:5002/api/members",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print(protected_response.json())
