import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("smartshop.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start_time = time.perf_counter()

        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": request_id},
        )

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                f"Request failed: {request.method} {request.url.path}",
                extra={"request_id": request_id},
            )
            raise

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)

        logger.info(
            (
                f"Request completed: {request.method} {request.url.path} "
                f"status={response.status_code} duration_ms={duration_ms}"
            ),
            extra={"request_id": request_id},
        )

        return response