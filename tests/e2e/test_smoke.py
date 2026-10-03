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


def test_timeseries_endpoint():
    response = client.get("/v1/index/timeseries?days=30")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "headline_apix" in data["data"][0]


def test_heatmap_endpoint():
    response = client.get("/v1/routes/heatmap")
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) > 0
    assert "inflation_pct" in data["routes"][0]


def test_elasticity_endpoint():
    response = client.get("/v1/analytics/elasticity")
    assert response.status_code == 200
    data = response.json()
    assert "horizons" in data
    assert len(data["horizons"]) > 0
    assert "average_fare_inr" in data["horizons"][0]


def test_dgca_backtest_endpoint():
    response = client.get("/v1/backtest/dgca")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "validated"
    assert "correlation_coefficient" in data
    assert len(data["benchmarks"]) > 0


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "/dashboard"


def test_dashboard_endpoint():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Aero-Metrics" in response.text
    assert "timeseriesChart" in response.text
