"""
Password Hashing Utilities
Provides secure password hashing and verification using bcrypt.

Spec Reference: specs/features/plans/authentication-plan.md (Section 2.1, 2.2)
"""

from passlib.context import CryptContext


# Configure password hashing context with bcrypt
# Cost factor: 12 (approx 250-500ms hashing time for security)
# Spec Requirement: bcrypt cost factor 12 (specs/features/authentication.md NFR1)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor 12
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt with cost factor 12.

    The salt is automatically generated and included in the hash.
    Hashing intentionally takes ~250-500ms for security against brute force.

    Spec Requirement: specs/features/authentication.md (Password Storage)

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password string in bcrypt format ($2b$12$...)

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> print(hashed)
        $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Dq.gC3GqKnGu
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Uses constant-time comparison to prevent timing attacks.
    Passlib handles this automatically.

    Spec Requirement: specs/features/plans/authentication-plan.md (Section 2.2)

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt hashed password to compare against

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> verify_password("SecurePass123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)
