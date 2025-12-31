"""
JWT Token Utilities
Provides JWT token creation and validation.

Spec Reference: specs/features/plans/authentication-plan.md (Section 1, 2.2)
"""

from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings


def create_access_token(user_id: int, email: str) -> str:
    """
    Generate a JWT access token for authenticated user.

    Token Claims:
    - sub (subject): User ID as string (JWT standard requires string)
    - email: User email (for display only, NOT for authorization)
    - iat (issued at): Current UTC timestamp
    - exp (expiration): Current UTC + JWT_EXPIRY_HOURS

    Spec Requirement: specs/features/authentication.md (JWT Token Payload)

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token(123, "user@example.com")
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi...
    """
    now = datetime.utcnow()
    expires = now + timedelta(hours=settings.JWT_EXPIRY_HOURS)

    payload = {
        "sub": str(user_id),  # MUST be string per JWT spec
        "email": email,
        "iat": now,
        "exp": expires
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Validates:
    - Token signature (using JWT_SECRET_KEY)
    - Token expiration (exp claim)
    - Token structure (proper JWT format)

    Spec Requirement: specs/features/plans/authentication-plan.md (Section 2.3)

    Args:
        token: JWT token string to verify

    Returns:
        Decoded payload dictionary containing claims (sub, email, exp, iat)

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        >>> token = create_access_token(123, "user@example.com")
        >>> payload = verify_token(token)
        >>> print(payload["sub"])
        '123'
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        # Raises on:
        # - Invalid signature
        # - Expired token (exp claim)
        # - Malformed token
        # - Missing required claims
        raise e
