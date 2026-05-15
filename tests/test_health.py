from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    data = response.json()

    assert response.status_code == 200
    assert "status" in data
    assert "db_connection" in data