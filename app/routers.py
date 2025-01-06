"""Module defining the routing and request handling logic for the API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Request, status
from fastapi.responses import RedirectResponse

from app.models import Url
from app.schemas import UrlOutput
from app.services import UrlShortenerService, get_url_shortener_service
from toolkit.api.enums import OpenAPITagsEnum

router = APIRouter(tags=[OpenAPITagsEnum.URL_SHORTENER])


@router.post(
    "/url",
    status_code=status.HTTP_201_CREATED,
    response_model=UrlOutput,
)
async def create_short_url(
    target_url: Annotated[str, Body(embed=True)],
    url_shortener_service: Annotated[
        UrlShortenerService, Depends(get_url_shortener_service)
    ],
) -> Url:
    """
    Create a shortened URL for a given target URL.

    - **target_url**: The original URL to be shortened.
    \f
    Parameters
    ----------
    target_url : str
        The original URL to be shortened.
    url_shortener_service : UrlShortenerService
        The service handling URL shortening logic.

    Returns
    -------
    Url
        The created URL object containing the shortened URL.
    """
    url = await url_shortener_service.create_url(target_url=target_url)
    return url


@router.get(
    "/{url_key}",
    status_code=status.HTTP_200_OK,
    response_class=RedirectResponse,
)
async def forward_to_target_url(
    url_key: Annotated[str, Path()],
    request: Request,
    url_shortener_service: Annotated[
        UrlShortenerService, Depends(get_url_shortener_service)
    ],
) -> RedirectResponse:
    """
    Redirect to the target URL associated with the given short URL key.

    - **url_key**: The key of the shortened URL.
    \f
    Parameters
    ----------
    url_key : str
        The key of the shortened URL.
    request : Request
        The HTTP request object containing metadata.
    url_shortener_service : UrlShortenerService
        The service handling URL redirection logic.

    Returns
    -------
    RedirectResponse
        A response object redirecting to the target URL.
    """
    target_url = await url_shortener_service.forward_to_target_url(
        url_key=url_key, request_url=str(request.url)
    )
    return RedirectResponse(target_url)


@router.delete(
    "/{url_key}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=RedirectResponse,
)
async def deactivate_url_key(
    url_key: Annotated[str, Path()],
    url_shortener_service: Annotated[
        UrlShortenerService, Depends(get_url_shortener_service)
    ],
) -> RedirectResponse:
    """
    Deactivate a shortened URL key, preventing further redirection.

    - **url_key**: The key of the shortened URL to deactivate.
    \f
    Parameters
    ----------
    url_key : str
        The key of the shortened URL to deactivate.
    url_shortener_service : UrlShortenerService
        The service handling URL deactivation logic.
    """
    await url_shortener_service.deactivate_url_key(url_key=url_key)
