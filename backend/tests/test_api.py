"""Setup smoke check only; add exercise-specific tests as you build each phase."""
from fastapi.testclient import TestClient

from backend.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_student_endpoint(monkeypatch):
    from backend import main

    rows = [{"name": "Prad", "email": "prad@example.com", "major": "Math"}]
    monkeypatch.setattr(main, "get_supabase_client", lambda: object())
    monkeypatch.setattr(main, "fetch_students", lambda client: rows)
    with TestClient(app) as client:
        response = client.get("/api/students")
    assert response.status_code == 200
    assert response.json() == rows


def test_student_endpoint_failure(monkeypatch):
    from backend import main

    def fail():
        raise RuntimeError("private configuration detail")

    monkeypatch.setattr(main, "get_supabase_client", fail)
    with TestClient(app) as client:
        response = client.get("/api/students")
    assert response.status_code == 503
    assert "private configuration detail" not in response.text
