import base64

from tamash_playwright import expect

# Python port of tests/APITests/10SampleAPITestFileUpload.spec.ts.
#
# File Upload - http://localhost:5002/api/upload. Covers: multipart/form-data upload (file +
# optional text field), the raw binary download response, 404 when the file doesn't exist, and
# 400 when no file is sent at all.
#
# The upload checks (201 Created) stay plain assert — 201 vs 200 is meaningfully the point being
# tested (was a resource actually *created*). The download check only cares that it succeeded
# (200 is the only success code a GET can return here), so it uses expect(response).to_be_ok().

AUTH_HEADER = {"Authorization": "Basic " + base64.b64encode(b"admin:admin").decode()}
BASE_URL = "http://localhost:5002/api/upload"

_PNG_BYTES = bytes([0x89, 0x50, 0x4E, 0x47])


def test_upload_file_multipart_with_description(api_request_context):
    response = api_request_context.post(
        BASE_URL,
        headers=AUTH_HEADER,
        multipart={
            "file": {"name": "photo.png", "mimeType": "image/png", "buffer": _PNG_BYTES},
            "description": "test upload",
        },
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 201
    assert body["success"] is True
    assert body["fileName"] == "photo.png"
    assert body["description"] == "test upload"
    assert body["size"] == 4
    assert "/api/upload/" in body["url"]


def test_upload_then_download_same_file_as_binary(api_request_context):
    upload_response = api_request_context.post(
        BASE_URL,
        headers=AUTH_HEADER,
        multipart={"file": {"name": "photo2.png", "mimeType": "image/png", "buffer": _PNG_BYTES}},
    )
    url = upload_response.json()["url"]
    print(f"Uploaded file URL: {url}")

    download_response = api_request_context.get(url, headers=AUTH_HEADER)
    download_body = download_response.body()

    print(f"Status Code: {download_response.status}")
    print(f"Content-Type: {download_response.headers.get('content-type')}")

    expect(download_response).to_be_ok()
    assert download_response.headers.get("content-type") == "image/png"
    assert download_body == _PNG_BYTES


def test_download_file_that_does_not_exist_expect_404(api_request_context):
    response = api_request_context.get(f"{BASE_URL}/does-not-exist.png", headers=AUTH_HEADER)
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 404
    assert "not found" in body["message"]


def test_upload_with_no_file_field_expect_400(api_request_context):
    response = api_request_context.post(
        BASE_URL,
        headers=AUTH_HEADER,
        multipart={"description": "no file attached"},
    )
    body = response.json()

    print(body)
    print(f"Status Code: {response.status}")

    assert response.status == 400
    assert body["success"] is False
    assert "No file was uploaded" in body["message"]
