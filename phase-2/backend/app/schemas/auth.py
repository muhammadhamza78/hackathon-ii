"""
Authentication Pydantic Schemas
Defines request and response models for authentication endpoints.

Spec Reference: specs/api/rest-endpoints.md (Authentication Endpoints)
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegisterRequest(BaseModel):
    """
    Request schema for user registration.

    Endpoint: POST /api/auth/register
    Spec: specs/api/rest-endpoints.md
    """

    email: EmailStr = Field(
        ...,
        description="User email address (login identifier)",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (min 8 chars, max 128 chars)",
        examples=["SecurePass123!"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class UserLoginRequest(BaseModel):
    """
    Request schema for user login.

    Endpoint: POST /api/auth/login
    Spec: specs/api/rest-endpoints.md
    """

    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        description="User password",
        examples=["SecurePass123!"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class TokenResponse(BaseModel):
    """
    Response schema for successful login.

    Contains JWT access token and metadata.
    Spec: specs/api/rest-endpoints.md (POST /api/auth/login response)
    """

    access_token: str = Field(
        ...,
        description="JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(
        default="Bearer",
        description="Token type (always 'Bearer')",
        examples=["Bearer"]
    )
    expires_in: int = Field(
        ...,
        description="Token expiry time in seconds",
        examples=[86400]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "expires_in": 86400
            }
        }


class UserResponse(BaseModel):
    """
    Response schema for user data (without password).

    Used for registration response and user profile.
    Spec: specs/api/rest-endpoints.md (POST /api/auth/register response)
    """

    id: int = Field(
        ...,
        description="User ID",
        examples=[1]
    )
    email: str = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )
    created_at: datetime = Field(
        ...,
        description="Account creation timestamp",
        examples=["2025-12-30T10:00:00Z"]
    )

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2025-12-30T10:00:00Z"
            }
        }
