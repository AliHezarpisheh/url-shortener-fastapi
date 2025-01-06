"""Module defining the database models and ORM mappings for the application."""

from sqlalchemy.orm import Mapped, mapped_column

from toolkit.database import Base, CommonMixin


class Url(CommonMixin, Base):
    """Url model, represent a shortened URL with associated metadata."""

    __tablename__ = "urls"

    key: Mapped[str] = mapped_column(
        unique=True, index=True, comment="Unique shortened URL key"
    )
    target_url: Mapped[str] = mapped_column(
        index=True, unique=True, comment="Original URL being shortened"
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, comment="URL activation status (True = active, False = inactive)"
    )
    clicks: Mapped[int] = mapped_column(
        default=0, comment="Number of times the URL has been accessed"
    )

    def __str__(self) -> str:
        """Return a human-readable string representation of the URL."""
        return f"URL: {self.target_url} (Key: {self.key}, Active: {self.is_active})"

    def __repr__(self) -> str:
        """Return a machine-readable string representation of the URL."""
        return (
            f"<Url(key={self.key}, target_url={self.target_url}, "
            f"is_active={self.is_active}, clicks={self.clicks})>"
        )
