from redis import Redis

from app.core.config import settings

redis_connect = Redis(host=settings.REDIS_URL, password=settings.REDIS_PASS)
