from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "PokeImages"
    assert response.json()["status"] == "UP"


def test_root_is_running():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "PokeImages"
