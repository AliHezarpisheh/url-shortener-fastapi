"""Module defining Pydantic models for OpenAPI settings."""

from pydantic import AnyHttpUrl, BaseModel, EmailStr
from pydantic_settings import BaseSettings


class ContactSettings(BaseModel):
    """Contact information for the API."""

    name: str
    email: EmailStr


class LicenseSettings(BaseModel):
    """License information for the API."""

    name: str
    url: AnyHttpUrl


class TagSettings(BaseModel):
    """Tag information for the API."""

    name: str
    description: str


class OpenAPISettings(BaseSettings):
    """Settings for OpenAPI configuration."""

    title: str
    version: str
    description: str
    contact: ContactSettings
    license: LicenseSettings
    tags: list[TagSettings]
