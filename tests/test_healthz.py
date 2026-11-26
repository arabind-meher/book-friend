import pytest
from django.db import OperationalError, connection


@pytest.mark.django_db
def test_healthz_ok(client):
    response = client.get("/healthz/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok", "redis": "ok"}


@pytest.mark.django_db
def test_healthz_redis_down(client, settings):
    settings.REDIS_URL = "redis://localhost:1/0"

    response = client.get("/healthz/")

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "ok", "redis": "error"}


@pytest.mark.django_db
def test_healthz_database_down(client, monkeypatch):
    def broken_cursor(*args, **kwargs):
        raise OperationalError("database unavailable")

    monkeypatch.setattr(connection, "cursor", broken_cursor)

    response = client.get("/healthz/")

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "error", "redis": "ok"}


def test_healthz_rejects_post(client):
    response = client.post("/healthz/")

    assert response.status_code == 405
