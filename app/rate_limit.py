from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, status


class InMemoryRateLimiter:
    def __init__(self, limit: int, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    def check(self, client_id: str) -> None:
        now = monotonic()
        timestamps = self.requests[client_id]
        while timestamps and timestamps[0] <= now - self.window_seconds:
            timestamps.popleft()
        if len(timestamps) >= self.limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many messages. Please wait a minute and try again.")
        timestamps.append(now)
