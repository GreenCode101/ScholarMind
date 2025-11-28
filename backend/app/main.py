from fastapi import FastAPI
from app.routers import auth, user
import logging
from app.core.security import setup_middlewares
from app.core.logger import configure_logging, LogLevels
from app.core.security import setup_middlewares
from app.core.rate_limiter import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

configure_logging(LogLevels.info)
logger = logging.getLogger("app")
logger.info("Starting ScholarMind application")


app = FastAPI(
    title="ScholarMind",
    version="1.0.0",
    description="An AI-powered platform to assist students with their academic needs.",
    docs_url="/",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

setup_middlewares(app)

app.include_router(auth.router)
app.include_router(user.router)
