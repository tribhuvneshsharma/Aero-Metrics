from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "apix-api"


def test_headline_endpoint():
    response = client.get("/v1/index/headline")
    assert response.status_code == 200
    data = response.json()
    assert "headline_apix" in data
    assert data["quality_metadata"]["quality_status"] == "pass"

