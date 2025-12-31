"""
User SQLModel
Defines the User table for authentication.

Spec Reference: specs/database/schema.md (users table)
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import validator


class User(SQLModel, table=True):
    """
    User model for authentication.

    Table: users
    Fields match the database schema specification exactly.
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, sa_column_kwargs={"nullable": False})
    hashed_password: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

    @validator("email", pre=True)
    def normalize_email(cls, v: str) -> str:
        """
        Normalize email to lowercase for case-insensitive uniqueness.

        Spec Requirement: Email stored as lowercase (specs/features/authentication.md FR1)

        Args:
            v: Email string

        Returns:
            Lowercase, trimmed email
        """
        if isinstance(v, str):
            return v.lower().strip()
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "$2b$12$hashedpassword...",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
