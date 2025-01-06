"""Custom fixtures and configurations for pytest tests."""

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session

from app.main import app
from config.database import AsyncDatabaseConnection
from toolkit.api.database import get_async_db_session
from toolkit.database.orm import Base


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command line option for pytest.

    Parameters
    ----------
    parser : pytest.Parser
        The pytest parser object.
    """
    parser.addoption(
        "--dburl",
        action="store",
        default=("postgresql+asyncpg://postgres:postgres@localhost/test_url_shortener"),
        help="URL of the database, used for tests",
    )


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
def db_url(request: pytest.FixtureRequest) -> str:
    """
    Fixture to retrieve the database URL from pytest command line options.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The request object for accessing pytest configurations.

    Returns
    -------
    str
        The database URL.
    """
    database_url: str = request.config.getoption("--dburl")
    return database_url


@pytest.fixture(scope="session")
def db(db_url: str) -> AsyncDatabaseConnection:
    """Async database connection objects for testing."""
    return AsyncDatabaseConnection(database_url=db_url)


@pytest.fixture(scope="function")
async def db_engine(db: AsyncDatabaseConnection) -> AsyncGenerator[None, None]:
    """
    Fixture providing a SQLAlchemy async engine instance connected to the database.

    The main purpose of the fixture is creating and dropping tables, at start and end
    of the test session. Also, it close the engine after the test session.

    Parameters
    ----------
    db : AsyncDatabaseConnection
        The object for managing database objects.

    Yields
    ------
    Generator[Engine, None, None]
        A generator yielding the SQLAlchemy engine instance.
    """
    engine = db.get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db.close_engine()


@pytest.fixture(scope="function")
async def db_session(
    db: AsyncDatabaseConnection, db_engine: AsyncEngine
) -> AsyncGenerator[async_scoped_session[AsyncSession], None]:
    """
    Fixture providing an async scoped SQLAlchemy session.

    Parameters
    ----------
    db : AsyncDatabaseConnection
        The object for managing database objects.

    Returns
    -------
    async_scoped_session[AsyncSession]
        An async scoped SQLAlchemy session.
    """
    session = db.get_session()
    yield session
    await session.rollback()

    # Truncate all tables after each test function.
    for table in reversed(Base.metadata.sorted_tables):
        stmt = text(f"TRUNCATE {table.name} CASCADE;")
        await session.execute(stmt)
        await session.commit()

    await session.close()


@pytest.fixture(autouse=True)
def override_get_db_session(
    db_session: async_scoped_session[AsyncSession], db_engine: AsyncEngine
):
    """
    Override the get_async_db_session dependency to use the provided database session.

    Parameters
    ----------
    db_session : sqlalchemy.orm.Session
        The test database session to be used instead of the default session.
    """

    async def _get_async_test_db_session() -> (
        AsyncGenerator[async_scoped_session[AsyncSession], None]
    ):
        """
        Get a test database session.

        Yields
        ------
        Session
            A test database session.
        """
        yield db_session

    app.dependency_overrides[get_async_db_session] = _get_async_test_db_session
