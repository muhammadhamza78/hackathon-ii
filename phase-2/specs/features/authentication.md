# Feature Specification: User Authentication

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Feature ID**: F001
**Status:** Specification
**Dependencies**: None (foundational feature)

## Overview

Implement secure user authentication using JWT (JSON Web Tokens) to enable user registration, login, and session management. This feature is foundational and required for all other features.

## Business Requirements

### BR1: User Registration
New users must be able to create an account with email and password.

**Value**: Allows new users to join the platform and start managing tasks.

**User Story**:
> As a new user, I want to register with my email and password, so that I can create an account and access the task management system.

### BR2: User Login
Existing users must be able to authenticate and receive an access token.

**Value**: Enables returning users to securely access their data.

**User Story**:
> As a registered user, I want to log in with my email and password, so that I can access my tasks.

### BR3: Secure Password Storage
User passwords must be securely hashed and never stored in plaintext.

**Value**: Protects user credentials from data breaches.

**User Story**:
> As a user, I expect my password to be stored securely so that my account is protected.

### BR4: JWT Token Issuance
Upon successful login, users receive a JWT token to authenticate subsequent requests.

**Value**: Enables stateless authentication for API access.

**User Story**:
> As a logged-in user, I expect to receive a token that I can use to access protected resources.

### BR5: Token-Based Access Control
Protected endpoints must validate JWT tokens and extract user identity.

**Value**: Ensures only authenticated users can access their data.

**User Story**:
> As a user, I expect that only I can access my tasks when I provide my authentication token.

## Functional Requirements

### User Data Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| email | String | Required, Unique, Max 255 chars, Email format | User email address (login identifier) |
| hashed_password | String | Required, Max 255 chars | Bcrypt/Argon2 hashed password |
| created_at | DateTime | Auto-generated, Immutable | Account creation timestamp |
| updated_at | DateTime | Auto-updated | Last modification timestamp |

**Password Storage**:
- NEVER store plaintext passwords
- Use bcrypt (cost factor 12) or argon2 for hashing
- Salt is automatically handled by bcrypt/argon2

### FR1: User Registration

**Endpoint**: `POST /api/auth/register`

**Authentication**: Not required (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Field Validation**:
- `email`:
  - Required
  - Valid email format (contains @, valid domain)
  - Max 255 characters
  - Case-insensitive (stored as lowercase)
  - Must be unique (not already registered)
- `password`:
  - Required
  - Min 8 characters
  - Max 128 characters
  - No additional complexity requirements for MVP (future: uppercase, numbers, symbols)

**Response (201 Created)**:
```json
{
  "id": 456,
  "email": "user@example.com",
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Note**: Password is NEVER returned in response.

**Business Logic**:
1. Validate request body
2. Normalize email to lowercase
3. Check if email already exists → 400 if exists
4. Hash password using bcrypt (cost factor 12)
5. Create user record in database
6. Return user object (without password)

**Error Cases**:
- 400 Bad Request: Email already exists → `{"detail": "Email already registered"}`
- 422 Validation Error: Invalid email format, password too short/long

**Acceptance Criteria**:
- [ ] User registered with valid email and password returns 201
- [ ] Email is normalized to lowercase before storage
- [ ] Password is hashed (bcrypt/argon2) before storage
- [ ] Duplicate email returns 400 error
- [ ] Invalid email format returns 422
- [ ] Password shorter than 8 chars returns 422
- [ ] Password longer than 128 chars returns 422
- [ ] Response does NOT include password (plain or hashed)
- [ ] created_at and updated_at are set automatically

### FR2: User Login

**Endpoint**: `POST /api/auth/login`

**Authentication**: Not required (public endpoint)

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Field Validation**:
- `email`: Required, email format
- `password`: Required

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**JWT Token Payload**:
```json
{
  "sub": "456",
  "email": "user@example.com",
  "exp": 1735650000,
  "iat": 1735563600
}
```

**JWT Claims**:
- `sub` (subject): User ID (as string)
- `email`: User email
- `exp` (expiration): Token expiry timestamp (Unix timestamp)
- `iat` (issued at): Token issue timestamp (Unix timestamp)

**Business Logic**:
1. Validate request body
2. Normalize email to lowercase
3. Query database for user with matching email
4. If user not found → 401 (invalid credentials)
5. Verify password against hashed_password
6. If password invalid → 401 (invalid credentials)
7. Generate JWT token with user_id and email
8. Set token expiry (24 hours default)
9. Return token response

**Error Cases**:
- 401 Unauthorized: Email not found OR password incorrect → `{"detail": "Invalid credentials"}`
- 422 Validation Error: Email or password missing

**Note**: Do NOT reveal whether email or password was incorrect (prevents enumeration).

**Acceptance Criteria**:
- [ ] Login with correct email and password returns 200 with JWT token
- [ ] Email is case-insensitive for login
- [ ] Incorrect password returns 401
- [ ] Non-existent email returns 401
- [ ] Error message does NOT reveal which field was wrong
- [ ] JWT token contains user_id in `sub` claim
- [ ] JWT token contains email
- [ ] JWT token has expiry set to 24 hours from issue
- [ ] Token type is "Bearer"
- [ ] expires_in is returned in seconds

### FR3: JWT Token Validation

**Implementation**: Middleware/Dependency Injection

**Not an endpoint** - this is authentication logic applied to protected endpoints.

**Process**:
1. Extract `Authorization` header from request
2. Verify header format: `Bearer <token>`
3. Extract token
4. Verify token signature using secret key
5. Check token expiry (exp claim)
6. Extract user_id from `sub` claim
7. Inject user_id into request context (for use in endpoint handlers)

**Error Cases**:
- 401 Unauthorized: Missing Authorization header
- 401 Unauthorized: Invalid header format (not "Bearer <token>")
- 401 Unauthorized: Invalid token signature
- 401 Unauthorized: Token expired
- 401 Unauthorized: Token malformed

**Response (401)**:
```json
{
  "detail": "Unauthorized"
}
```

**Acceptance Criteria**:
- [ ] Valid token allows access to protected endpoint
- [ ] Missing token returns 401
- [ ] Invalid token signature returns 401
- [ ] Expired token returns 401
- [ ] Malformed token returns 401
- [ ] user_id extracted from token is available to endpoint handler

### FR4: Protected Endpoint Pattern

**All protected endpoints MUST**:
- Require JWT token in Authorization header
- Extract user_id from validated token
- Use user_id for data access and isolation
- Return 401 if token is missing or invalid

**Example** (FastAPI dependency):
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> int:
    token = credentials.credentials
    # Verify and decode JWT
    # Extract user_id from 'sub' claim
    # Return user_id or raise HTTPException(401)
    pass
```

**Usage in Endpoint**:
```python
@router.get("/api/tasks")
async def list_tasks(user_id: int = Depends(get_current_user_id)):
    # user_id is guaranteed to be valid
    tasks = await get_user_tasks(user_id)
    return {"tasks": tasks}
```

### FR5: Logout (Client-Side)

**No backend endpoint required.**

**Process**:
- Client removes JWT token from local storage/session storage
- Subsequent requests without token will be rejected (401)

**Note**: Token cannot be invalidated server-side in stateless JWT system. Token remains valid until expiry.

**Future Enhancement**: Token blacklist or refresh tokens for server-side revocation.

## Non-Functional Requirements

### Security

**NFR1: Password Security**
- Passwords hashed with bcrypt (cost factor 12) or argon2
- Salt automatically handled by hashing algorithm
- Plaintext passwords NEVER logged or stored

**NFR2: JWT Security**
- Secret key: Min 256-bit (32 characters), stored in environment variable
- Algorithm: HS256 (HMAC with SHA-256)
- Token expiry: 24 hours (configurable)
- Secret key NEVER committed to version control

**NFR3: Transport Security**
- HTTPS required in production (TLS/SSL)
- HTTP allowed only in local development

**NFR4: Brute Force Protection**
- Not implemented in MVP
- Future: Rate limiting on login endpoint (e.g., 5 attempts per minute per IP)

**NFR5: Session Management**
- Stateless authentication (no server-side session storage)
- Token expiry enforced
- No token refresh in MVP (user must re-login after 24 hours)

### Performance

**NFR6: Authentication Performance**
- Registration: < 500ms (bcrypt hashing is intentionally slow for security)
- Login: < 500ms
- Token validation: < 10ms (signature verification only, no database query)

### Data Protection

**NFR7: Sensitive Data Handling**
- Passwords NEVER logged
- JWT tokens logged only in debug mode (not production)
- Email addresses treated as PII (not shared, not logged excessively)

## Configuration

### Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | Secret key for signing JWT tokens | `your-256-bit-secret-key-here` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_EXPIRY_HOURS` | Token expiry in hours | `24` |

**Security Note**: `JWT_SECRET_KEY` MUST be:
- Min 32 characters (256-bit)
- Randomly generated (not a dictionary word)
- Stored securely (environment variable, not in code)
- Different for each environment (dev, staging, prod)

## UI/UX Requirements

### Registration Page

**URL**: `/register`

**Layout**:
- Email input field (type="email", required)
- Password input field (type="password", required, min 8 chars)
- "Register" submit button
- Link to login page: "Already have an account? Login here"

**Validation Feedback**:
- Show validation errors below fields
- Email format validation (client-side)
- Password length validation (client-side)
- Display server errors (e.g., "Email already registered")

**Success Flow**:
- On successful registration, redirect to login page with message: "Account created! Please log in."

### Login Page

**URL**: `/login` or `/` (landing page)

**Layout**:
- Email input field (type="email", required)
- Password input field (type="password", required)
- "Login" submit button
- Link to registration page: "Don't have an account? Register here"

**Validation Feedback**:
- Show validation errors below fields
- Display server errors (e.g., "Invalid credentials")

**Success Flow**:
- On successful login:
  - Store JWT token in localStorage or sessionStorage
  - Redirect to dashboard (`/dashboard`)

### Authentication State Management

**Client-Side Token Storage**:
- Store JWT token in localStorage (persists across sessions) OR sessionStorage (session only)
- Include token in Authorization header for all API requests

**Protected Routes**:
- Check for token presence before rendering protected pages
- If token missing or expired, redirect to login page

**Logout**:
- Remove token from storage
- Redirect to login page

## Test Scenarios

### TS1: User Registration - Happy Path
1. User submits registration form with valid email and password
2. System hashes password
3. System creates user record
4. System returns 201 with user object (no password)

**Expected**: User registered successfully

### TS2: User Registration - Duplicate Email
1. User A registers with email@example.com
2. User B attempts to register with email@example.com
3. System returns 400 "Email already registered"

**Expected**: Duplicate email rejected

### TS3: User Registration - Validation Errors
1. User submits invalid email → 422
2. User submits password with 5 chars → 422
3. User submits password with 150 chars → 422

**Expected**: Validation errors returned

### TS4: User Login - Happy Path
1. User registers with email and password
2. User logs in with same credentials
3. System verifies password
4. System generates JWT token
5. System returns 200 with token

**Expected**: Login successful, token received

### TS5: User Login - Invalid Credentials
1. User logs in with wrong password → 401 "Invalid credentials"
2. User logs in with non-existent email → 401 "Invalid credentials"

**Expected**: Login rejected, no enumeration

### TS6: User Login - Case Insensitive Email
1. User registers with User@Example.com
2. User logs in with user@example.com
3. System normalizes email and authenticates

**Expected**: Login successful (case-insensitive)

### TS7: Protected Endpoint Access
1. User logs in and receives token
2. User includes token in Authorization header
3. User accesses protected endpoint (e.g., GET /api/tasks)
4. System validates token and returns data

**Expected**: Access granted

### TS8: Protected Endpoint - Missing Token
1. User accesses protected endpoint without token
2. System returns 401 "Unauthorized"

**Expected**: Access denied

### TS9: Protected Endpoint - Expired Token
1. User logs in and receives token with 1-second expiry
2. User waits 2 seconds
3. User accesses protected endpoint with expired token
4. System returns 401 "Unauthorized"

**Expected**: Access denied (token expired)

### TS10: Token Contains Correct Claims
1. User logs in
2. Decode JWT token (for testing)
3. Verify `sub` claim contains user_id
4. Verify `email` claim contains user email
5. Verify `exp` claim is 24 hours from issue

**Expected**: Token claims are correct

## Edge Cases

### EC1: Email Normalization
- Email with uppercase letters → Stored as lowercase
- Email with leading/trailing spaces → Trimmed before storage

### EC2: Password Edge Cases
- Password with exactly 8 chars → Accepted
- Password with exactly 128 chars → Accepted
- Password with 129 chars → Rejected (422)
- Password with special characters → Accepted

### EC3: JWT Token Edge Cases
- Token with invalid signature → 401
- Token with missing claims → 401
- Token with malformed structure → 401

### EC4: Concurrent Registration
- Two users attempt to register with same email simultaneously
- Database unique constraint ensures only one succeeds
- Second request returns 400

### EC5: Password Hash Cost
- Bcrypt cost factor 12 → Approx 250-500ms hashing time
- Acceptable for registration and login (intentional security tradeoff)

## Dependencies

**Depends On**:
- Database: Users table must exist
- Environment: JWT_SECRET_KEY must be configured

**Blocks**:
- F002 (Task CRUD): All task operations require authentication

## Out of Scope

The following are explicitly OUT OF SCOPE for this feature:

- Password reset / forgot password flow
- Email verification
- Two-factor authentication (2FA)
- OAuth / Social login (Google, GitHub, etc.)
- Refresh tokens
- Token blacklist (server-side revocation)
- Rate limiting / brute force protection
- Account deletion
- Profile updates (change email/password)
- Remember me functionality
- Session management (concurrent logins)

## Acceptance Criteria Summary

**Feature is DONE when**:
- [ ] User registration endpoint implemented and tested
- [ ] User login endpoint implemented and tested
- [ ] JWT token generation and validation implemented
- [ ] Password hashing (bcrypt/argon2) implemented
- [ ] Protected endpoint pattern implemented (dependency injection)
- [ ] All validation rules enforced
- [ ] All error cases return correct status codes
- [ ] UI allows registration and login
- [ ] Client stores and uses JWT token
- [ ] Integration tests pass with >80% coverage
- [ ] Manual testing completed for all flows

## References

- See: `specs/architecture.md` (Security and Authentication sections)
- See: `specs/database/schema.md` (User table definition)
- See: `specs/api/rest-endpoints.md` (Auth endpoints)
- See: `.specify/memory/constitution.md` (JWT Authentication Mandatory principle)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
