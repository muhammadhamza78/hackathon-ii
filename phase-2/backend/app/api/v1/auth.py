"""
Authentication API Endpoints
Handles user registration and login.

Spec Reference:
- specs/api/rest-endpoints.md (Authentication Endpoints)
- specs/features/authentication.md (FR1, FR2)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse
)
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.config import settings


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def register(
    request: UserRegisterRequest,
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Register a new user account.

    Spec: specs/features/authentication.md (FR1)
    Endpoint: POST /api/auth/register

    Process:
    1. Validate request body (automatic via Pydantic)
    2. Normalize email to lowercase
    3. Check if email already exists
    4. Hash password using bcrypt (cost factor 12)
    5. Create user in database
    6. Return user object (without password)

    Args:
        request: User registration data (email, password)
        session: Database session (injected)

    Returns:
        UserResponse: Created user object with id, email, created_at

    Raises:
        HTTPException 400: Email already registered
        HTTPException 422: Validation error (automatic)

    Example:
        Request:
            POST /api/auth/register
            {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }

        Response (201):
            {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2025-12-30T10:00:00Z"
            }
    """
    # Email is already normalized by User model validator
    # But we normalize here too for the duplicate check query
    email = request.email.lower().strip()

    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password using bcrypt (cost factor 12)
    # This intentionally takes ~250-500ms for security
    hashed_password = hash_password(request.password)

    # Create new user
    user = User(
        email=email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Return user response (without password)
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate user and receive JWT access token"
)
async def login(
    request: UserLoginRequest,
    session: Session = Depends(get_session)
) -> TokenResponse:
    """
    Login user and issue JWT access token.

    Spec: specs/features/authentication.md (FR2)
    Endpoint: POST /api/auth/login

    Process:
    1. Normalize email to lowercase
    2. Query user by email
    3. If not found → 401 "Invalid credentials"
    4. Verify password using constant-time comparison
    5. If invalid → 401 "Invalid credentials"
    6. Generate JWT token with user_id and email
    7. Return token response

    IMPORTANT: Error message NEVER reveals whether email or password was wrong
    (prevents user enumeration attack)

    Args:
        request: Login credentials (email, password)
        session: Database session (injected)

    Returns:
        TokenResponse: JWT token, token_type, expires_in

    Raises:
        HTTPException 401: Invalid email OR password
        HTTPException 422: Validation error (automatic)

    Example:
        Request:
            POST /api/auth/login
            {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }

        Response (200):
            {
                "access_token": "eyJhbGci...",
                "token_type": "Bearer",
                "expires_in": 86400
            }
    """
    # Normalize email for case-insensitive login
    email = request.email.lower().strip()

    # Query user by email
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    # User not found → 401 (do NOT reveal email doesn't exist)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password using constant-time comparison
    # Passlib's verify_password handles this securely
    if not verify_password(request.password, user.hashed_password):
        # Password incorrect → 401 (do NOT reveal password is wrong)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate JWT access token
    # Token contains: sub (user_id), email, iat, exp
    access_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    # Calculate expiry in seconds
    expires_in = settings.JWT_EXPIRY_HOURS * 3600  # hours to seconds

    return TokenResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=expires_in
    )
