import redis.asyncio as redis
import json

# Redis client
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_cached_notes():
    """Get cached notes from Redis"""
    data = await redis_client.get("notes")
    if data:
        return json.loads(data)

async def set_cached_notes(notes, ttl=60):
    """Set notes to Redis with TTL"""
    await redis_client.set("notes", json.dumps(notes), ex=ttl)

async def invalidate_cache():
    """Delete notes cache"""
    await redis_client.delete("notes")
