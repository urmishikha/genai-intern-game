import redis
from typing import Optional


class RedisCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    def get(self, key: str) -> Optional[bool]:
        val = self.redis.get(key)
        return bool(int(val)) if val is not None else None

    def set(self, key: str, value: bool, ttl: int = 86400):
        self.redis.set(key, int(value), ex=ttl)