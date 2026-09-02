# Python port of tests/APITests/2SampleAPITestOAuth2ClientCreds.spec.ts.
#
# OAuth2 "Client Credentials" grant is used for machine-to-machine auth (no user/username-
# password involved — just a client_id + client_secret that identifies the calling
# application/service).


def test_api_login_with_oauth2_client_credentials(api_request_context):
    # Step 1: Exchange client_id + client_secret for an access_token. grant_type=client_credentials
    # tells the auth server which OAuth2 flow to use.
    token_response = api_request_context.post(
        "http://localhost:5002/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "demo-client",
            "client_secret": "demo-secret",
        },
    )
    token_body = token_response.json()
    print(token_body)
    token = token_body["access_token"]

    # Step 2: Use the access_token as a Bearer token on the protected API call, same as the JWT
    # flow — OAuth2 client-credentials tokens are typically presented the same way once issued.
    response = api_request_context.get(
        "http://localhost:5002/api/members",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(response.json())
