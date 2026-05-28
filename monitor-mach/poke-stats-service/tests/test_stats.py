from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "PokeStats"
    assert response.json()["status"] == "UP"


def test_pokemon_not_found():
    response = client.get("/stats/not-a-real-pokemon")

    assert response.status_code == 404