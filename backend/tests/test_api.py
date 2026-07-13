from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_mock_data_endpoint_returns_seeded_records():
    response = client.get("/mock-data")

    assert response.status_code == 200

    payload = response.json()

    assert len(payload["customers"]) == 15
    assert len(payload["orders"]) == 15
    assert "SmartShop Refund Policy" in payload["policy"]


def test_demo_cases_endpoint():
    response = client.get("/demo-cases")

    assert response.status_code == 200

    payload = response.json()

    assert len(payload["demo_cases"]) >= 4