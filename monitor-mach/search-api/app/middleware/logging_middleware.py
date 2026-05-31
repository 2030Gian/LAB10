import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import log_event


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        api = request.url.path
        function = "http_request"

        log_event(
            api=api,
            function=function,
            message=f"START request_id={request_id} method={request.method}",
        )

        try:
            response = await call_next(request)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Latency-ms"] = str(latency_ms)

            log_event(
                api=api,
                function=function,
                message=(
                    f"END request_id={request_id} method={request.method} "
                    f"status={response.status_code} latency_ms={latency_ms}"
                ),
            )

            return response

        except Exception as exc:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            log_event(
                api=api,
                function=function,
                message=(
                    f"END request_id={request_id} method={request.method} "
                    f"status=500 latency_ms={latency_ms} error={str(exc)}"
                ),
                level=logging.ERROR,
            )

            raise