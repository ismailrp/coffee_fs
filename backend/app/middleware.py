import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import app_logger
from app.logger import error_logger
# global error_counter
error_counter = 0

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        global error_counter
        start_time = time.time()

        try:

            response = await call_next(request)

            process_time = (
                time.time() - start_time
            ) * 1000

            log_message = (
                f"{request.method} "
                f"{request.url.path} "
                f"STATUS={response.status_code} "
                f"TIME={process_time:.2f}ms"
            )

            app_logger.info(log_message)

            # slow response simulation
            if process_time > 2000:

                error_logger.error(
                    f"SLOW RESPONSE: {log_message}"
                )

            return response

        except Exception as e:

            process_time = (
                time.time() - start_time
            ) * 1000

            error_logger.error(
                f"{request.method} "
                f"{request.url.path} "
                f"ERROR={str(e)} "
                f"TIME={process_time:.2f}ms"
            )
            
            error_counter += 1

            if error_counter >= 3:

                error_logger.error(
                    "ALERT: ERROR COUNT > 3"
                )

            raise e