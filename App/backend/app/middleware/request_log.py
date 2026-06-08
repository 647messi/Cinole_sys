import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger


logger = get_logger(__name__)


def get_client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")

    if real_ip:
        return real_ip

    return request.client.host if request.client else None


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        method = request.method
        path = request.url.path
        client_ip = get_client_ip(request)

        logger.info(
            "Request started | "
            f"request_id={request_id} | "
            f"method={method} | "
            f"path={path} | "
            f"client_ip={client_ip}"
        )

        try:
            response = await call_next(request)

            duration_ms = round((time.time() - start_time) * 1000, 2)

            logger.info(
                "Request completed | "
                f"request_id={request_id} | "
                f"method={method} | "
                f"path={path} | "
                f"status_code={response.status_code} | "
                f"duration_ms={duration_ms}"
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception:
            duration_ms = round((time.time() - start_time) * 1000, 2)

            logger.exception(
                "Request failed | "
                f"request_id={request_id} | "
                f"method={method} | "
                f"path={path} | "
                f"client_ip={client_ip} | "
                f"duration_ms={duration_ms}"
            )

            raise