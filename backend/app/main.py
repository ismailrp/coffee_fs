from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.logger import error_logger
import time
from app.database import Base, engine

from app.models.user import User
from app.models.coffee import Coffee
from app.models.order import Order
from app.routes.auth import router as auth_router
from app.routes.coffee import router as coffee_router
from app.routes.order import router as order_router
from app.middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    error_logger.error(
        f"GLOBAL ERROR | "
        f"PATH={request.url.path} | "
        f"ERROR={str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )

Base.metadata.create_all(bind=engine)
app.add_middleware(LoggingMiddleware)

@app.get("/")
def root():

    return {
        "message": "Coffee API running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.get("/slow")
def slow_api():

    time.sleep(3)

    return {
        "message": "slow response"
    }

@app.get("/error")
def error_api():
    raise Exception("Simulated error")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    coffee_router,
    prefix="/coffees",
    tags=["Coffees"]
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"]
)

