"""
Authentication Dependencies
FastAPI dependency functions for JWT token validation and user extraction.

Spec Reference: specs/features/plans/authentication-plan.md (Section 2.3)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.auth.jwt import verify_token


# HTTP Bearer token security scheme
# Automatically extracts "Authorization: Bearer <token>" header
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    FastAPI dependency to extract and validate user_id from JWT token.

    This dependency:
    1. Extracts token from Authorization header (via HTTPBearer)
    2. Verifies token signature and expiry
    3. Extracts user_id from 'sub' claim
    4. Returns user_id as integer

    Spec Requirement: specs/features/authentication.md (FR3, FR4)

    Args:
        credentials: Automatically injected by HTTPBearer dependency

    Returns:
        int: Authenticated user's ID

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or malformed

    Example Usage:
        @router.get("/api/tasks")
        async def list_tasks(user_id: int = Depends(get_current_user_id)):
            # user_id is guaranteed to be valid and authenticated
            tasks = get_user_tasks(user_id)
            return tasks

    Error Cases (all raise 401):
    - Missing Authorization header
    - Invalid header format (not "Bearer <token>")
    - Invalid token signature
    - Expired token
    - Malformed token
    - Missing 'sub' claim
    - Invalid 'sub' value (not convertible to int)
    """
    token = credentials.credentials

    try:
        # Verify token signature and expiry
        # Raises JWTError if invalid, expired, or malformed
        payload = verify_token(token)

        # Extract user_id from 'sub' claim
        # JWT spec requires 'sub' to be string, so we convert to int
        user_id_str = payload.get("sub")

        if not user_id_str:
            # Token missing 'sub' claim
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )

        # Convert string to integer
        try:
            user_id = int(user_id_str)
        except ValueError:
            # 'sub' claim is not a valid integer
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )

        return user_id

    except JWTError:
        # Token verification failed (invalid signature, expired, malformed)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
