from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_ok_and_request_id_header_present():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    # Middleware should always return a request id
    assert "x-request-id" in {k.lower(): v for k, v in resp.headers.items()}


def test_meta_contains_name_version_environment():
    resp = client.get("/api/v1/meta")
    assert resp.status_code == 200
    body = resp.json()
    assert "name" in body
    assert "version" in body
    assert "environment" in body


def test_docs_help_has_expected_shape():
    resp = client.get("/api/v1/docs/help")
    assert resp.status_code == 200
    body = resp.json()
    assert body["api_base"] == "/api/v1"
    assert "/api/v1/health" in body["endpoints"]["health"]
