import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import aioredis

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url="redis://localhost", limit=5, window_seconds=60):
        super().__init__(app)
        self.redis_url = redis_url
        self.limit = limit
        self.window = window_seconds
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        if not self.redis:
            self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)

        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        now = int(time.time())
        window_key = f"{key}:{now // self.window}"

        count = await self.redis.get(window_key)
        if count is None:
            await self.redis.set(window_key, 1, ex=self.window)
        elif int(count) < self.limit:
            await self.redis.incr(window_key)
        else:
            return Response(
                content="Too Many Requests",
                status_code=HTTP_429_TOO_MANY_REQUESTS
            )

        return await call_next(request)
