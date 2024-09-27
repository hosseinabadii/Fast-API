import redis.asyncio as redis

from app.config import settings

token_blacklist = redis.Redis.from_url(url=settings.redis_url)


async def add_jti_to_blacklist(jti: str) -> None:
    await token_blacklist.set(name=jti, value="", ex=settings.redis_jti_expire, nx=True)


async def jti_in_blacklist(jti: str) -> bool:
    jti = await token_blacklist.get(name=jti)
    return jti is not None
