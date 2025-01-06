"""Module defining general type annotations for the app."""

from typing import TypeAlias

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
