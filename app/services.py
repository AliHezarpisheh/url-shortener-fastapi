"""Module containing business logic and services."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.models import Url
from app.utils import generate_random_key
from config.base import logger
from toolkit.api.database import get_async_db_session


class UrlShortenerService:
    """Service for URL shortening and redirection."""

    def __init__(self, db_session: async_scoped_session[AsyncSession]) -> None:
        """Initialize the service with a database session."""
        self.db_session = db_session

    async def create_url(self, target_url: str) -> Url:
        """
        Create a shortened URL with a target URL.

        Parameters
        ----------
        target_url : str
            The original URL to be shortened.

        Returns
        -------
        Url
            The created URL object.
        """
        key = generate_random_key(length=5)
        url = await self._create_url(
            target_url=target_url,
            key=key,
        )
        return url

    async def _create_url(self, target_url: str, key: str) -> Url:
        """Create a URL entry in the database.

        Parameters
        ----------
        target_url : str
            The original URL to be shortened.
        key : str
            The generated key for the shortened URL.

        Returns
        -------
        Url
            The created URL object.

        Raises
        ------
        HTTPException
            If a unique constraint is violated.
        """
        stmt = (
            insert(Url)
            .values(
                key=key,
                target_url=target_url,
            )
            .returning(Url)
        )

        async with self.db_session.begin():
            try:
                result = await self.db_session.execute(stmt)
                url = result.scalar_one()
                logger.debug("Successfully created and retrieved the url from db")
                return url
            except IntegrityError:
                logger.error(
                    "Database unique constraint violated for `urls` table",
                    exc_info=True,
                )
                await self.db_session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Unique constraint violated",
                )  # TODO: Improve the error handling

    async def forward_to_target_url(self, url_key: str, request_url: str) -> str:
        """
        Fetch and return the target URL for a given short URL key.

        Parameters
        ----------
        url_key : str
            The key of the shortened URL.
        request_url : str
            The full request URL.

        Returns
        -------
        str
            The target URL corresponding to the key.

        Raises
        ------
        HTTPException
            If the key does not exist or the URL is inactive.
        """
        stmt = select(Url).where(Url.is_active == True, Url.key == url_key)  # noqa: E712

        async with self.db_session.begin():
            try:
                result = await self.db_session.execute(stmt)
                url = result.scalar_one()
                logger.debug("Successfully fetched the target url from db")
                await self.update_clicks(url=url)
                return url.target_url
            except NoResultFound:
                logger.error(
                    "The request url is not found in the db",
                    exc_info=True,
                )
                await self.db_session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"URL `{request_url}` doesn't exist",
                )  # TODO: Improve the error handling

    async def update_clicks(self, url: Url) -> None:
        """
        Increment the click count for a given URL record.

        Parameters
        ----------
        url : Url
            The URL database record for which the click count needs to be updated.
        """
        clicks = url.clicks + 1  # TODO: Think of scalability here, is it handled?
        stmt = update(Url).where(Url.id == url.id).values(clicks=clicks)

        await self.db_session.execute(stmt)


def get_url_shortener_service(
    db_session: Annotated[
        async_scoped_session[AsyncSession], Depends(get_async_db_session)
    ],
) -> UrlShortenerService:
    """Dependency injection for the URL shortener service."""
    return UrlShortenerService(db_session=db_session)
