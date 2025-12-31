"""
Authentication Endpoint Tests
Tests for user registration and login endpoints.

Spec Reference:
- specs/features/authentication.md (Test Scenarios)
- specs/features/plans/authentication-plan.md (Section 9.1)
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.user import User
from app.auth.password import hash_password


class TestRegistration:
    """Test cases for POST /api/auth/register"""

    def test_register_success(self, client: TestClient, session: Session):
        """
        Test successful user registration.

        Spec: TS1 (specs/features/authentication.md)
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password NEVER returned

    def test_register_duplicate_email(self, client: TestClient, session: Session):
        """
        Test registration with duplicate email returns 400.

        Spec: TS2 (specs/features/authentication.md)
        """
        # Create first user
        user = User(
            email="existing@example.com",
            hashed_password=hash_password("password123")
        )
        session.add(user)
        session.commit()

        # Attempt to register with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "existing@example.com",
                "password": "AnotherPass456!"
            }
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_invalid_email(self, client: TestClient):
        """
        Test registration with invalid email returns 422.

        Spec: TS3 (specs/features/authentication.md)
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == 422

    def test_register_short_password(self, client: TestClient):
        """
        Test registration with password < 8 chars returns 422.

        Spec: TS3 (specs/features/authentication.md)
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "short"  # Only 5 chars
            }
        )

        assert response.status_code == 422

    def test_register_long_password(self, client: TestClient):
        """
        Test registration with password > 128 chars returns 422.

        Spec: TS3 (specs/features/authentication.md)
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "a" * 150  # 150 chars, exceeds max
            }
        )

        assert response.status_code == 422

    def test_register_email_case_insensitive(self, client: TestClient, session: Session):
        """
        Test email normalization (case-insensitive).

        Spec: TS6, EC1 (specs/features/authentication.md)
        """
        # Register with uppercase email
        response1 = client.post(
            "/api/auth/register",
            json={
                "email": "User@Example.COM",
                "password": "SecurePass123!"
            }
        )
        assert response1.status_code == 201

        # Attempt to register with lowercase version
        response2 = client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "AnotherPass456!"
            }
        )
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Email already registered"


class TestLogin:
    """Test cases for POST /api/auth/login"""

    def test_login_success(self, client: TestClient, session: Session):
        """
        Test successful login returns JWT token.

        Spec: TS4 (specs/features/authentication.md)
        """
        # Create user
        user = User(
            email="user@example.com",
            hashed_password=hash_password("SecurePass123!")
        )
        session.add(user)
        session.commit()

        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"
        assert data["expires_in"] == 86400  # 24 hours in seconds

    def test_login_wrong_password(self, client: TestClient, session: Session):
        """
        Test login with wrong password returns 401.

        Spec: TS5 (specs/features/authentication.md)
        """
        # Create user
        user = User(
            email="user@example.com",
            hashed_password=hash_password("CorrectPassword123!")
        )
        session.add(user)
        session.commit()

        # Login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": "user@example.com",
                "password": "WrongPassword456!"
            }
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_nonexistent_email(self, client: TestClient):
        """
        Test login with non-existent email returns 401.

        Spec: TS5 (specs/features/authentication.md)
        """
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!"
            }
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_no_enumeration(self, client: TestClient, session: Session):
        """
        Test that error message doesn't reveal whether email or password was wrong.

        Spec: Section 7.7 (specs/features/plans/authentication-plan.md)
        """
        # Create user
        user = User(
            email="user@example.com",
            hashed_password=hash_password("CorrectPassword123!")
        )
        session.add(user)
        session.commit()

        # Wrong password
        response1 = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "WrongPassword"}
        )

        # Non-existent email
        response2 = client.post(
            "/api/auth/login",
            json={"email": "nobody@example.com", "password": "SomePassword"}
        )

        # Both should return same error message
        assert response1.status_code == 401
        assert response2.status_code == 401
        assert response1.json()["detail"] == response2.json()["detail"]
        assert response1.json()["detail"] == "Invalid credentials"

    def test_login_case_insensitive_email(self, client: TestClient, session: Session):
        """
        Test login is case-insensitive for email.

        Spec: TS6 (specs/features/authentication.md)
        """
        # Create user with lowercase email
        user = User(
            email="user@example.com",
            hashed_password=hash_password("SecurePass123!")
        )
        session.add(user)
        session.commit()

        # Login with uppercase email
        response = client.post(
            "/api/auth/login",
            json={
                "email": "User@Example.COM",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data


class TestJWTValidation:
    """Test cases for JWT token validation (get_current_user_id dependency)"""

    def test_protected_endpoint_with_valid_token(self, client: TestClient, session: Session):
        """
        Test that valid JWT token allows access to protected endpoint.

        Spec: TS7 (specs/features/authentication.md)
        """
        # Create user and login
        user = User(
            email="user@example.com",
            hashed_password=hash_password("SecurePass123!")
        )
        session.add(user)
        session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "SecurePass123!"}
        )
        token = login_response.json()["access_token"]

        # Note: We'll need a protected endpoint to test this
        # For now, we verify token was issued successfully
        assert token is not None
        assert len(token) > 0

    def test_protected_endpoint_without_token(self, client: TestClient):
        """
        Test that missing token returns 401.

        Spec: TS8 (specs/features/authentication.md)
        """
        # This will be tested when we have protected endpoints
        # For now, this test serves as a placeholder
        pass

    def test_token_contains_correct_claims(self, client: TestClient, session: Session):
        """
        Test that JWT token contains correct claims.

        Spec: TS10 (specs/features/authentication.md)
        """
        from jose import jwt
        from app.config import settings

        # Create user and login
        user = User(
            email="user@example.com",
            hashed_password=hash_password("SecurePass123!")
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        login_response = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "SecurePass123!"}
        )
        token = login_response.json()["access_token"]

        # Decode token (for testing purposes only)
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        # Verify claims
        assert payload["sub"] == str(user.id)  # User ID as string
        assert payload["email"] == "user@example.com"
        assert "exp" in payload  # Expiration
        assert "iat" in payload  # Issued at


class TestUserIsolation:
    """
    CRITICAL SECURITY TEST: User Isolation

    Spec: Task 25 (specs/features/tasks/authentication-tasks.md)
    """

    def test_user_isolation_placeholder(self, client: TestClient, session: Session):
        """
        Placeholder test for user isolation.

        This test will be fully implemented when we have task CRUD endpoints.
        For now, it demonstrates the test pattern.

        Test Logic:
        1. Create User A and login → token_a
        2. Create User B and login → token_b
        3. User A creates a resource (task)
        4. User B attempts to access User A's resource with token_b
        5. Assert: Returns 404 (not 200, not 403)
        """
        # Create two users
        user_a = User(email="usera@example.com", hashed_password=hash_password("pass123"))
        user_b = User(email="userb@example.com", hashed_password=hash_password("pass456"))
        session.add(user_a)
        session.add(user_b)
        session.commit()
        session.refresh(user_a)
        session.refresh(user_b)

        # Login as both users
        login_a = client.post(
            "/api/auth/login",
            json={"email": "usera@example.com", "password": "pass123"}
        )
        login_b = client.post(
            "/api/auth/login",
            json={"email": "userb@example.com", "password": "pass456"}
        )

        token_a = login_a.json()["access_token"]
        token_b = login_b.json()["access_token"]

        # Both logins should succeed
        assert login_a.status_code == 200
        assert login_b.status_code == 200

        # TODO: When task CRUD endpoints are implemented:
        # 1. User A creates task with token_a
        # 2. User B attempts GET /api/tasks/{task_id} with token_b
        # 3. Assert response.status_code == 404

        assert token_a != token_b  # Tokens should be different
