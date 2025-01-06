"""Module defining the Pydantic models for validation and serialization."""

from typing import Annotated

from pydantic import Field

from toolkit.api.schemas import BaseSchema, CommonMixins


class UrlOutput(CommonMixins, BaseSchema):
    """Pydantic model representing the output schema for a shortened URL."""

    key: Annotated[str, Field(description="Unique shortened URL key")]
    secret_key: Annotated[
        str, Field(description="Unique secret key for URL management")
    ]
    target_url: Annotated[str, Field(description="Original URL being shortened")]
    is_active: Annotated[bool, Field(default=True, description="URL activation status")]
    clicks: Annotated[
        int, Field(default=0, description="Number of times URL was accessed")
    ]
