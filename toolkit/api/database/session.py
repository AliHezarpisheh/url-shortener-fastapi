"""Dependency injection module for database session dependency, mainly the session."""

from collections.abc import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from config.base import db, logger


async def get_async_db_session() -> (
    AsyncGenerator[async_scoped_session[AsyncSession], None]
):
    """
    Dependency injection module for async database session.

    This module provides an asynchronous generator function `get_async_db_session
    for injecting an async scoped database session into FastAPI endpoints. It manages
    database transactions, logging errors, and raising custom HTTP exceptions in
    case of database-related or unexpected issues.

    Raises
    ------
    HTTPException
        If a SQLAlchemy error or any other unexpected exception occurs, a
        HTTP exception is raised with an appropriate status code and detail.

    Yields
    ------
    AsyncGenerator[async_scoped_session[AsyncSession], None]
        The async scoped session object that can be used for database operations
        within the FastAPI route or service.

    Examples
    --------
    Use this dependency in your FastAPI endpoints to interact with the database:

        @app.get("/some-db-route/")
        async def some_db_route(db_session: \
Annotated[AsyncSession, Depends(get_async_db_session)]):
            # Interact with the database using `db_session`
            pass
    """
    db_session = db.get_session()
    try:
        yield db_session
    except HTTPException:
        raise
    except SQLAlchemyError:
        await db_session.rollback()
        logger.error("Database error occurred", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Some services are not available! Check the application logs for "
                "more details."
            ),
        )
    finally:
        await db_session.close()
