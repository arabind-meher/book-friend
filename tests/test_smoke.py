import pytest
from django.db import connection


def test_settings_load(settings):
    assert settings.SECRET_KEY


@pytest.mark.django_db
def test_database_is_postgres():
    assert connection.vendor == "postgresql"
