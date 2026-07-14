import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)

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
            duration_seconds = time.perf_counter() - start_time

            # Do not collect metrics about the metrics endpoint itself.
            if request.url.path != "/metrics":
                HTTP_REQUESTS_TOTAL.labels(
                    method=request.method,
                    path=request.url.path,
                    status_code="500",
                ).inc()

                HTTP_REQUEST_DURATION_SECONDS.labels(
                    method=request.method,
                    path=request.url.path,
                ).observe(duration_seconds)

            logger.exception(
                f"Request failed: {request.method} {request.url.path}",
                extra={"request_id": request_id},
            )
            raise

        duration_seconds = time.perf_counter() - start_time
        duration_ms = round(duration_seconds * 1000, 2)

        # Use FastAPI's route template when available.
        # Example:
        #   /orders/{order_id}
        # instead of
        #   /orders/O1004
        route = request.scope.get("route")
        metric_path = getattr(route, "path", request.url.path)

        if request.url.path != "/metrics":
            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                path=metric_path,
                status_code=str(response.status_code),
            ).inc()

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=request.method,
                path=metric_path,
            ).observe(duration_seconds)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)

        logger.info(
            (
                f"Request completed: "
                f"{request.method} {request.url.path} "
                f"status={response.status_code} "
                f"duration_ms={duration_ms}"
            ),
            extra={"request_id": request_id},
        )

        return response