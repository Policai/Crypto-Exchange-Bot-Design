import logging
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from backend.api import admin_routes, finance_routes, user_routes
from backend.models.database import Base, engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Crypto Exchange API")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
@limiter.limit("20/minute")
def health(_request: Request):
    return {"ok": True}


app.include_router(user_routes.router)
app.include_router(finance_routes.router)
app.include_router(admin_routes.router)
