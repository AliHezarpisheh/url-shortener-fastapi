"""
Module serves the FastAPI instance for the backend application.

It initializes the FastAPI application, configures middleware, setting lifespan context
manager, and defines routes for handling various HTTP requests.
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config.base import settings

from .healthcheck import router as health_check_router
from .lifespan import lifespan
from .routers import router as url_shortener_router

# Instantiate `FastAPI`
app = FastAPI(
    title=settings.openapi.title,
    version=settings.openapi.version,
    description=settings.openapi.description,
    contact=settings.openapi.contact.model_dump(),
    license_info=settings.openapi.license.model_dump(),
    openapi_tags=[tag.model_dump() for tag in settings.openapi.tags],
    default_response_class=ORJSONResponse,
    redoc_url=None,
    lifespan=lifespan,
)

# Include routers
app.include_router(health_check_router)
app.include_router(url_shortener_router)
