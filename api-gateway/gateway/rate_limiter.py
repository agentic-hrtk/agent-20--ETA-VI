"""Token-bucket rate limiter backed by Redis — NexaCorp API Gateway."""
import time, os
import redis

_redis = None

def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(os.environ["RATE_LIMIT_REDIS_URL"])
    return _redis

def is_allowed(client_id: str, limit: int = 1000, window: int = 3600) -> bool:
    r   = get_redis()
    key = f"ratelimit:{client_id}:{int(time.time()) // window}"
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window * 2)
    count, _ = pipe.execute()
    return count <= limit

def get_remaining(client_id: str, limit: int = 1000, window: int = 3600) -> int:
    r   = get_redis()
    key = f"ratelimit:{client_id}:{int(time.time()) // window}"
    used = int(r.get(key) or 0)
    return max(0, limit - used)
