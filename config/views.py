import redis
from django.conf import settings
from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


def check_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return False
    return True


def check_redis():
    try:
        with redis.Redis.from_url(
            settings.REDIS_URL, socket_connect_timeout=2, socket_timeout=2
        ) as client:
            client.ping()
    except redis.RedisError:
        return False
    return True


@require_GET
def healthz(request):
    checks = {"database": check_database(), "redis": check_redis()}
    healthy = all(checks.values())
    body = {"status": "ok" if healthy else "error"}
    body.update({name: "ok" if ok else "error" for name, ok in checks.items()})
    return JsonResponse(body, status=200 if healthy else 503)
