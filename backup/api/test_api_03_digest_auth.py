import hashlib
import re
import secrets

# Python port of tests/APITests/3SampleAPITestDigestAuth.spec.ts.
#
# Digest Auth never sends the password over the wire (unlike Basic Auth, which just
# base64-encodes it — not even encrypted). Instead it's a challenge/response handshake:
#   1) Call the endpoint with no credentials -> server replies 401 and includes a
#      "WWW-Authenticate" header with a realm + nonce (challenge).
#   2) Hash username/password/nonce/etc into a "response" value and resend the request with an
#      "Authorization: Digest ..." header.


def _parse_digest_header(header: str) -> dict[str, str]:
    params: dict[str, str] = {}
    for match in re.finditer(r'(\w+)=(?:"([^"]*)"|([^\s,]+))', header):
        params[match.group(1)] = match.group(2) if match.group(2) is not None else match.group(3)
    return params


def _md5(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


def test_api_login_with_digest_auth(api_request_context):
    username = "admin"
    password = "admin"
    uri = "/api/members"

    # Step 1: Unauthenticated request to receive the digest challenge.
    challenge_response = api_request_context.get(f"http://localhost:5002{uri}")
    auth_header = challenge_response.headers["www-authenticate"]
    challenge = _parse_digest_header(auth_header)

    nonce = challenge["nonce"]
    realm = challenge["realm"]
    qop = challenge.get("qop")
    opaque = challenge.get("opaque")

    # nc (nonce count) and cnonce (client nonce) are required whenever the server asks for
    # qop="auth" — they let the server detect replay attacks.
    nc = "00000001"
    cnonce = secrets.token_hex(8)

    # HA1/HA2 are the two halves of the digest algorithm (RFC 7616):
    #   HA1 = md5(username:realm:password)
    #   HA2 = md5(method:uri)
    #   response = md5(HA1:nonce:nc:cnonce:qop:HA2)
    ha1 = _md5(f"{username}:{realm}:{password}")
    ha2 = _md5(f"GET:{uri}")
    response_hash = _md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}") if qop else _md5(f"{ha1}:{nonce}:{ha2}")

    # Step 2: Resend the request with the computed digest credentials.
    digest_header = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
        f'uri="{uri}", response="{response_hash}"'
    )
    if qop:
        digest_header += f", qop={qop}, nc={nc}, cnonce=\"{cnonce}\""
    if opaque:
        digest_header += f', opaque="{opaque}"'

    response = api_request_context.get(f"http://localhost:5002{uri}", headers={"Authorization": digest_header})
    print(response.json())
