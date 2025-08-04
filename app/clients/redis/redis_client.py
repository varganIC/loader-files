import redis

from app.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)


def acquire_lock(key: str) -> bool:
    return redis_client.set(name=key, value='1', nx=True)


def release_lock(key: str):
    redis_client.delete(key)
