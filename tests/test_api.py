from fastapi.testclient import TestClient
from backend.server import app

client = TestClient(app)


def test_valid_telemetry_log():
    payload = {
        "cpu_usage": 45.5,
        "memory_usage": 60.2,
        "disk_usage": 20.0,
        "host_name": "pytest-node-01",
        "latency": 5.2,
    }

    response = client.post("/log", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "anomaly" in data


def test_invalid_telemetry_log():
    payload = {
        "cpu_usage": "ninety-nine",
        "memory_usage": 60.2,
        "disk_usage": 20.0,
        "host_name": "pytest-node-02",
        "latency": 5.2,
    }

    response = client.post("/log", json=payload)

    assert response.status_code == 422
