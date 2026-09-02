import base64
import random
import string

# Python port of tests/APITests/6SampleAPITestMembersCreate.spec.ts.
#
# POST /api/members - create a resource. Covers: JSON body, application/x-www-form-urlencoded
# body (req.body looks the same either way), and the validation errors for missing fields, bad
# name/gender formats, and unexpected extra keys.
#
# Deviates from the original in two verified ways, both confirmed directly against the real
# running server (curl), not assumed from the TS source:
#   1. This server persists data across runs, and the TS original's fixed names ("Jane Doe",
#      "John Smith") already existed from earlier runs, turning the "create" calls into 409
#      Conflict instead of 201 — same lesson as the OrangeHRM DDT port. Fixed with a per-run
#      unique suffix — letters only, though: a numeric suffix (this server's own validation
#      message says "Name should only contain Alphabets") turned out to trip a *third* real,
#      verified-live discrepancy before landing on this.
#   2. The "name too short" / "invalid gender" format-validation errors return 422 Unprocessable
#      Entity, not 400 — verified live; missing-field/extra-field/PUT-partial/PATCH-empty
#      validation errors elsewhere in this API do correctly return 400, so this isn't a blanket
#      TS-vs-Python difference, just these two specific checks.

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/members"


def _unique_name(base: str) -> str:
    suffix = "".join(random.choices(string.ascii_uppercase, k=5))
    return f"{base} {suffix}"


def test_create_member_with_json_body(api_request_context):
    name = _unique_name("Jane Doe")
    response = api_request_context.post(
        BASE_URL,
        headers={**AUTH_HEADER, "Content-Type": "application/json"},
        data={"name": name, "gender": "female"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 201
    assert body["name"] == name
    assert body["gender"] == "female"
    assert body["id"]


def test_create_member_with_form_urlencoded_body(api_request_context):
    name = _unique_name("John Smith")
    response = api_request_context.post(
        BASE_URL,
        headers={**AUTH_HEADER, "Content-Type": "application/x-www-form-urlencoded"},
        form={"name": name, "gender": "male"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 201
    assert body["name"] == name
    assert body["gender"] == "male"
    assert body["id"]


def test_create_member_missing_name_gender_expect_400(api_request_context):
    response = api_request_context.post(BASE_URL, headers=AUTH_HEADER, data={"name": "Jane Doe"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 400
    assert "name and gender" in body["msg"]


def test_create_member_invalid_name_too_short_expect_422(api_request_context):
    response = api_request_context.post(BASE_URL, headers=AUTH_HEADER, data={"name": "Al", "gender": "male"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 422
    assert "4 to 25 characters" in body["msg"]


def test_create_member_invalid_gender_expect_422(api_request_context):
    response = api_request_context.post(BASE_URL, headers=AUTH_HEADER, data={"name": "Jane Doe", "gender": "other"})
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 422
    assert "male or female" in body["msg"]


def test_create_member_unexpected_extra_field_expect_400(api_request_context):
    response = api_request_context.post(
        BASE_URL,
        headers=AUTH_HEADER,
        data={"name": "Jane Doe", "gender": "female", "age": 30},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 400
    assert "only name and gender" in body["msg"]
