# Authentication Implementation Tasks

**Feature**: F001 - User Authentication
**Version**: 1.0.0
**Created**: 2025-12-30
**Status**: Task Breakdown
**References**:
- `specs/features/authentication.md`
- `specs/features/plans/authentication-plan.md`
- `specs/api/rest-endpoints.md`
- `specs/database/schema.md`

---

## Task Execution Order

Tasks are organized into **phases** and must be executed in order. Each task lists its dependencies.

**Execution Flow**:
1. **Phase 1**: Backend Setup (Tasks 1-3)
2. **Phase 2**: Database Setup (Tasks 4-6)
3. **Phase 3**: Backend Authentication (Tasks 7-12)
4. **Phase 4**: Frontend Setup (Tasks 13-15)
5. **Phase 5**: Frontend Authentication (Tasks 16-22)
6. **Phase 6**: Integration & Testing (Tasks 23-27)

**Total Tasks**: 27

---

## Phase 1: Backend Setup

### Task 1: Initialize Backend Project Structure

**Layer**: Backend
**Dependencies**: None
**Priority**: P0 (Critical)

**Spec Reference**:
- `specs/architecture.md` (Backend section)

**Description**:
Create the initial FastAPI project structure with proper directory organization.

**Expected Outcome**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── v1/              # API version 1
│   │       ├── __init__.py
│   │       └── auth.py      # Auth endpoints (placeholder)
│   ├── models/              # SQLModel data models
│   │   └── __init__.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   └── __init__.py
│   ├── auth/                # Authentication logic
│   │   └── __init__.py
│   ├── db/                  # Database connection
│   │   └── __init__.py
│   └── config.py            # Configuration management
├── tests/                   # Test directory
│   ├── __init__.py
│   └── conftest.py          # Pytest fixtures
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # Setup instructions
```

**Acceptance Criteria**:
- [ ] Directory structure created
- [ ] `main.py` with basic FastAPI app initialized
- [ ] Empty module files created
- [ ] `.env.example` with required variables listed

---

### Task 2: Install Backend Dependencies

**Layer**: Backend
**Dependencies**: Task 1
**Priority**: P0

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Implementation Checklist)

**Description**:
Install all required Python packages for authentication implementation.

**Required Packages**:
- `fastapi` (0.104+) - Web framework
- `uvicorn[standard]` - ASGI server
- `sqlmodel` (0.0.14+) - ORM
- `psycopg2-binary` - PostgreSQL driver
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT handling
- `python-multipart` - Form data support
- `pydantic[email]` - Email validation
- `pytest` - Testing framework
- `httpx` - HTTP client for testing

**Expected Outcome**:
- `requirements.txt` populated with pinned versions
- All packages installed in virtual environment
- No installation errors

**Acceptance Criteria**:
- [ ] `requirements.txt` created with all dependencies
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Import test successful (`python -c "import fastapi, sqlmodel, passlib, jose"`)

---

### Task 3: Configure Environment Variables

**Layer**: Backend
**Dependencies**: Task 2
**Priority**: P0

**Spec Reference**:
- `specs/features/authentication.md` (Configuration section)
- `specs/features/plans/authentication-plan.md` (Section 7.1)

**Description**:
Set up environment variable configuration for database connection and JWT secrets.

**Required Variables**:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET_KEY` - 256-bit secret for JWT signing
- `JWT_ALGORITHM` - "HS256"
- `JWT_EXPIRY_HOURS` - "24"

**Expected Outcome**:
- `config.py` module with environment variable loading
- `.env.example` template file
- `.env` file created (git-ignored)
- JWT secret generated securely

**Acceptance Criteria**:
- [ ] `config.py` loads environment variables using `pydantic.BaseSettings`
- [ ] `.env.example` contains all required variables with descriptions
- [ ] `.env` added to `.gitignore`
- [ ] JWT_SECRET_KEY generated with `secrets.token_urlsafe(32)`
- [ ] DATABASE_URL configured for Neon PostgreSQL

---

## Phase 2: Database Setup

### Task 4: Create User SQLModel

**Layer**: Backend (Database)
**Dependencies**: Task 3
**Priority**: P0

**Spec Reference**:
- `specs/database/schema.md` (users table)
- `specs/features/authentication.md` (User Data Model)

**Description**:
Define the User SQLModel class matching the database schema specification.

**Model Specification**:
- Table name: `users`
- Fields: `id`, `email`, `hashed_password`, `created_at`, `updated_at`
- Constraints: email unique, email indexed (case-insensitive)

**Expected Outcome**:
File: `backend/app/models/user.py`

**Model Requirements**:
- `id`: Optional[int], primary_key=True, default=None
- `email`: str, max_length=255, unique=True, index=True
- `hashed_password`: str, max_length=255
- `created_at`: datetime, default_factory=datetime.utcnow
- `updated_at`: datetime, default_factory=datetime.utcnow

**Acceptance Criteria**:
- [ ] User model defined in `models/user.py`
- [ ] All fields match schema specification
- [ ] Email normalized to lowercase before storage (validator)
- [ ] Model imports successfully
- [ ] Type hints correct (passes mypy if used)

---

### Task 5: Setup Database Connection

**Layer**: Backend (Database)
**Dependencies**: Task 4
**Priority**: P0

**Spec Reference**:
- `specs/database/schema.md` (Connection Management)
- `specs/features/plans/authentication-plan.md` (Database connection)

**Description**:
Configure SQLModel database engine and session management with connection pooling.

**Expected Outcome**:
File: `backend/app/db/session.py`

**Requirements**:
- Create SQLModel engine with DATABASE_URL
- Connection pool: size=10, max_overflow=0
- Pool timeout: 30 seconds
- Pool recycle: 3600 seconds
- Dependency function: `get_session()` yields Session

**Acceptance Criteria**:
- [ ] Engine created with pooling configuration
- [ ] `get_session()` dependency function defined
- [ ] Session yielded in context manager (auto-commit/rollback)
- [ ] Connection test successful (can connect to Neon database)

---

### Task 6: Create Database Migration for Users Table

**Layer**: Backend (Database)
**Dependencies**: Task 5
**Priority**: P0

**Spec Reference**:
- `specs/database/schema.md` (users table SQL definition)

**Description**:
Create Alembic migration to create the `users` table with proper indexes.

**Migration Content**:
- CREATE TABLE users with all columns
- CREATE UNIQUE INDEX on LOWER(email)
- Create updated_at trigger (optional, or handle in app)

**Expected Outcome**:
- Alembic initialized (`alembic init alembic`)
- Migration file created
- Migration applied to database

**Acceptance Criteria**:
- [ ] Alembic configured in `alembic.ini`
- [ ] Initial migration generated
- [ ] Migration creates `users` table
- [ ] UNIQUE index on `LOWER(email)` created
- [ ] Migration successfully applied (`alembic upgrade head`)
- [ ] Table exists in database (verified with SQL client)

---

## Phase 3: Backend Authentication

### Task 7: Implement Password Hashing Utility

**Layer**: Backend (Auth)
**Dependencies**: Task 2
**Priority**: P0

**Spec Reference**:
- `specs/features/authentication.md` (Password Storage)
- `specs/features/plans/authentication-plan.md` (Section 2.1, 2.2)

**Description**:
Create utility functions for password hashing and verification using bcrypt.

**Expected Outcome**:
File: `backend/app/auth/password.py`

**Functions**:
- `hash_password(password: str) -> str`: Hash password with bcrypt cost 12
- `verify_password(plain_password: str, hashed_password: str) -> bool`: Verify password

**Requirements**:
- Use `passlib.context.CryptContext` with bcrypt scheme
- Cost factor: 12
- Return hashed password as string
- Constant-time comparison (bcrypt handles this)

**Acceptance Criteria**:
- [ ] `password.py` module created
- [ ] `hash_password()` function returns bcrypt hash
- [ ] Hash format: `$2b$12$...` (bcrypt identifier)
- [ ] `verify_password()` returns True for correct password
- [ ] `verify_password()` returns False for incorrect password
- [ ] Hashing takes ~250-500ms (cost factor 12)

---

### Task 8: Implement JWT Utility Functions

**Layer**: Backend (Auth)
**Dependencies**: Task 3
**Priority**: P0

**Spec Reference**:
- `specs/features/authentication.md` (JWT Token Payload)
- `specs/features/plans/authentication-plan.md` (Section 1, 2.2)

**Description**:
Create utility functions for JWT token creation and validation.

**Expected Outcome**:
File: `backend/app/auth/jwt.py`

**Functions**:
- `create_access_token(user_id: int, email: str) -> str`: Generate JWT token
- `verify_token(token: str) -> dict`: Verify and decode JWT

**Token Claims**:
- `sub`: str(user_id) - User ID as string
- `email`: email - User email
- `iat`: current UTC timestamp
- `exp`: current UTC + JWT_EXPIRY_HOURS

**Requirements**:
- Use `jose.jwt.encode()` for creation
- Use `jose.jwt.decode()` for verification
- Algorithm: HS256
- Secret: from config.JWT_SECRET_KEY
- Raises `JWTError` on invalid token/expiry

**Acceptance Criteria**:
- [ ] `jwt.py` module created
- [ ] `create_access_token()` generates valid JWT
- [ ] Token payload contains all required claims
- [ ] `sub` claim is string (not integer)
- [ ] `verify_token()` decodes valid token successfully
- [ ] `verify_token()` raises JWTError for expired token
- [ ] `verify_token()` raises JWTError for invalid signature

---

### Task 9: Create Pydantic Schemas for Auth

**Layer**: Backend (Schemas)
**Dependencies**: Task 2
**Priority**: P0

**Spec Reference**:
- `specs/api/rest-endpoints.md` (Auth endpoints request/response schemas)
- `specs/features/authentication.md` (FR1, FR2)

**Description**:
Define Pydantic schemas for request validation and response serialization.

**Expected Outcome**:
File: `backend/app/schemas/auth.py`

**Schemas**:

1. `UserRegisterRequest`:
   - `email`: EmailStr (Pydantic email validation)
   - `password`: str (min_length=8, max_length=128)

2. `UserLoginRequest`:
   - `email`: EmailStr
   - `password`: str

3. `TokenResponse`:
   - `access_token`: str
   - `token_type`: str = "Bearer"
   - `expires_in`: int

4. `UserResponse`:
   - `id`: int
   - `email`: str
   - `created_at`: datetime

**Acceptance Criteria**:
- [ ] All schemas defined in `schemas/auth.py`
- [ ] Email validation uses Pydantic `EmailStr`
- [ ] Password min/max length constraints defined
- [ ] Schemas have proper type hints
- [ ] Example validation: invalid email raises ValidationError

---

### Task 10: Implement get_current_user_id Dependency

**Layer**: Backend (Auth)
**Dependencies**: Task 8
**Priority**: P0

**Spec Reference**:
- `specs/features/authentication.md` (FR3, FR4)
- `specs/features/plans/authentication-plan.md` (Section 2.3)

**Description**:
Create FastAPI dependency function to extract and validate user_id from JWT token.

**Expected Outcome**:
File: `backend/app/auth/dependencies.py`

**Function Signature**:
```python
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> int:
```

**Logic**:
1. Extract token from `credentials.credentials`
2. Call `verify_token(token)` to decode
3. Extract `sub` claim
4. Convert sub (string) to int
5. Return user_id
6. Raise HTTPException(401) on any error

**Acceptance Criteria**:
- [ ] Dependency function defined
- [ ] Uses FastAPI `HTTPBearer()` for automatic header extraction
- [ ] Decodes JWT and extracts user_id
- [ ] Returns integer user_id
- [ ] Raises 401 for missing token
- [ ] Raises 401 for invalid token
- [ ] Raises 401 for expired token
- [ ] Raises 401 for malformed sub claim

---

### Task 11: Implement POST /api/auth/register Endpoint

**Layer**: Backend (API)
**Dependencies**: Tasks 6, 7, 9
**Priority**: P0

**Spec Reference**:
- `specs/api/rest-endpoints.md` (POST /api/auth/register)
- `specs/features/authentication.md` (FR1)
- `specs/features/plans/authentication-plan.md` (Section 2.1)

**Description**:
Create registration endpoint to register new users with email and password.

**Expected Outcome**:
File: `backend/app/api/v1/auth.py`

**Endpoint**:
- Method: POST
- Path: `/api/auth/register`
- Request: `UserRegisterRequest`
- Response: `UserResponse` (201 Created)

**Logic** (per plan Section 2.1):
1. Validate request body (automatic via Pydantic)
2. Normalize email: `email.lower().strip()`
3. Check if user exists: `SELECT * FROM users WHERE email = ?`
4. If exists → raise HTTPException(400, "Email already registered")
5. Hash password using `hash_password()`
6. Create user in database
7. Return UserResponse (without password)

**Error Handling**:
- 400: Email already exists
- 422: Validation error (Pydantic automatic)

**Acceptance Criteria**:
- [ ] Endpoint defined in `api/v1/auth.py`
- [ ] Accepts `UserRegisterRequest` body
- [ ] Email normalized to lowercase
- [ ] Duplicate email returns 400 error
- [ ] Password hashed before storage
- [ ] User inserted into database
- [ ] Returns 201 with user object (no password)
- [ ] `created_at` and `updated_at` auto-set

---

### Task 12: Implement POST /api/auth/login Endpoint

**Layer**: Backend (API)
**Dependencies**: Tasks 7, 8, 9
**Priority**: P0

**Spec Reference**:
- `specs/api/rest-endpoints.md` (POST /api/auth/login)
- `specs/features/authentication.md` (FR2)
- `specs/features/plans/authentication-plan.md` (Section 2.2)

**Description**:
Create login endpoint to authenticate users and issue JWT tokens.

**Expected Outcome**:
File: `backend/app/api/v1/auth.py` (same file as Task 11)

**Endpoint**:
- Method: POST
- Path: `/api/auth/login`
- Request: `UserLoginRequest`
- Response: `TokenResponse` (200 OK)

**Logic** (per plan Section 2.2):
1. Validate request body
2. Normalize email: `email.lower().strip()`
3. Query user: `SELECT * FROM users WHERE email = ?`
4. If not found → raise HTTPException(401, "Invalid credentials")
5. Verify password using `verify_password()`
6. If invalid → raise HTTPException(401, "Invalid credentials")
7. Generate JWT using `create_access_token(user.id, user.email)`
8. Return TokenResponse

**Error Handling**:
- 401: Invalid email OR password (NEVER distinguish)
- 422: Validation error

**Acceptance Criteria**:
- [ ] Endpoint defined
- [ ] Email case-insensitive (normalized)
- [ ] User lookup by email
- [ ] Password verified with constant-time comparison
- [ ] JWT token generated with correct claims
- [ ] Returns 200 with `{ access_token, token_type, expires_in }`
- [ ] Invalid credentials return 401 (no enumeration)
- [ ] Error message does NOT reveal which field was wrong

---

## Phase 4: Frontend Setup

### Task 13: Initialize Frontend Project

**Layer**: Frontend
**Dependencies**: None
**Priority**: P0

**Spec Reference**:
- `specs/architecture.md` (Frontend section)
- `specs/ui/pages.md` (Page structure)

**Description**:
Create Next.js 16+ App Router project with TypeScript.

**Expected Outcome**:
```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Login page (/)
│   ├── register/
│   │   └── page.tsx         # Registration page
│   └── dashboard/
│       ├── layout.tsx       # Dashboard layout
│       └── page.tsx         # Task list (placeholder)
├── components/              # Reusable components
│   ├── forms/
│   └── layout/
├── lib/                     # Utilities
│   └── api.ts               # API client (placeholder)
├── types/                   # TypeScript types
│   └── auth.ts              # Auth types (placeholder)
├── public/                  # Static assets
├── .env.local.example       # Environment variables template
├── tsconfig.json            # TypeScript config
├── next.config.js           # Next.js config
└── package.json             # Dependencies
```

**Acceptance Criteria**:
- [ ] Next.js project created (`npx create-next-app@latest`)
- [ ] TypeScript enabled
- [ ] App Router structure (not Pages Router)
- [ ] Directory structure created
- [ ] Dev server runs (`npm run dev`)
- [ ] No build errors

---

### Task 14: Install Frontend Dependencies

**Layer**: Frontend
**Dependencies**: Task 13
**Priority**: P0

**Spec Reference**:
- `specs/ui/components.md` (Styling approach)

**Description**:
Install required npm packages for authentication and UI.

**Required Packages**:
- Core: Already installed by create-next-app (react, next, typescript)
- Styling: `tailwindcss`, `postcss`, `autoprefixer` (or CSS modules)
- Optional: `@types/node`, `@types/react`, `@types/react-dom`

**Expected Outcome**:
- `package.json` with all dependencies
- TailwindCSS configured (if using Tailwind)

**Acceptance Criteria**:
- [ ] Dependencies installed
- [ ] TypeScript types installed
- [ ] TailwindCSS configured (or CSS modules setup)
- [ ] No installation errors
- [ ] Import test successful (`npm run build`)

---

### Task 15: Create TypeScript Types for Auth

**Layer**: Frontend
**Dependencies**: Task 13
**Priority**: P0

**Spec Reference**:
- `specs/api/rest-endpoints.md` (Type Definitions section)

**Description**:
Define TypeScript types for authentication requests and responses matching backend API contracts.

**Expected Outcome**:
File: `frontend/types/auth.ts`

**Types**:
```typescript
export interface RegisterRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  id: number;
  email: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ErrorResponse {
  detail: string | ValidationError[];
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}
```

**Acceptance Criteria**:
- [ ] All auth types defined
- [ ] Types match API specification exactly
- [ ] No TypeScript errors when importing types

---

## Phase 5: Frontend Authentication

### Task 16: Create API Client Utility

**Layer**: Frontend
**Dependencies**: Task 15
**Priority**: P0

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Section 3.3)

**Description**:
Create a reusable API client utility that automatically includes JWT token in Authorization header.

**Expected Outcome**:
File: `frontend/lib/api.ts`

**Functions**:
- `apiRequest(endpoint, options)`: Wrapper around fetch with token injection
- Global 401 handling (redirect to login)

**Features**:
- Auto-includes `Authorization: Bearer <token>` if token exists
- Auto-includes `Content-Type: application/json`
- Handles 401 globally (clear token, redirect to `/`)
- Returns Response object

**Acceptance Criteria**:
- [ ] `apiRequest()` function defined
- [ ] Reads token from localStorage
- [ ] Adds Authorization header if token exists
- [ ] 401 response triggers logout and redirect
- [ ] Base URL configurable via environment variable

---

### Task 17: Create ProtectedRoute Component

**Layer**: Frontend
**Dependencies**: Task 13
**Priority**: P0

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Section 3.4)
- `specs/ui/components.md` (ProtectedRoute)

**Description**:
Create a client component that redirects unauthenticated users to login page.

**Expected Outcome**:
File: `frontend/components/utility/ProtectedRoute.tsx`

**Logic**:
1. Check for token in localStorage
2. Check expiry (if stored)
3. If no token or expired → redirect to `/`
4. Otherwise render children

**Acceptance Criteria**:
- [ ] Component created as "use client"
- [ ] Checks localStorage for token
- [ ] Checks token expiry if available
- [ ] Redirects to `/` if not authenticated
- [ ] Renders children if authenticated

---

### Task 18: Create Login Page

**Layer**: Frontend
**Dependencies**: Tasks 15, 16
**Priority**: P0

**Spec Reference**:
- `specs/ui/pages.md` (Landing / Login page)
- `specs/features/authentication.md` (UI/UX Requirements - Login Page)

**Description**:
Create login page at `/` with email/password form and JWT token storage.

**Expected Outcome**:
File: `frontend/app/page.tsx`

**Features**:
- Email input (type="email", required)
- Password input (type="password", required)
- Login button
- Link to registration page
- Client-side validation
- Error message display
- Token storage on success
- Redirect to `/dashboard` after login

**Logic**:
1. Form submission calls `POST /api/auth/login`
2. On 200: Store token in localStorage, redirect to `/dashboard`
3. On 401: Display "Invalid credentials"
4. On error: Display error message

**Acceptance Criteria**:
- [ ] Login form renders
- [ ] Client-side validation (email format, required fields)
- [ ] Calls login API on submit
- [ ] Stores token in localStorage on success
- [ ] Redirects to `/dashboard` on success
- [ ] Displays error message on failure
- [ ] Link to `/register` works

---

### Task 19: Create Registration Page

**Layer**: Frontend
**Dependencies**: Tasks 15, 16
**Priority**: P0

**Spec Reference**:
- `specs/ui/pages.md` (Registration page)
- `specs/features/authentication.md` (UI/UX Requirements - Registration Page)

**Description**:
Create registration page at `/register` with email/password form.

**Expected Outcome**:
File: `frontend/app/register/page.tsx`

**Features**:
- Email input (type="email", required, max 255)
- Password input (type="password", required, min 8, max 128)
- Register button
- Link to login page
- Client-side validation
- Error message display
- Redirect to `/` with success message

**Logic**:
1. Form submission calls `POST /api/auth/register`
2. On 201: Redirect to `/` with success message
3. On 400: Display "Email already registered"
4. On 422: Display validation errors

**Acceptance Criteria**:
- [ ] Registration form renders
- [ ] Client-side validation (email, password length)
- [ ] Character counter for password (optional)
- [ ] Calls register API on submit
- [ ] Redirects to `/` on success with message
- [ ] Displays error messages appropriately
- [ ] Link to `/` (login) works

---

### Task 20: Create Dashboard Layout with Auth Check

**Layer**: Frontend
**Dependencies**: Task 17
**Priority**: P0

**Spec Reference**:
- `specs/ui/pages.md` (Dashboard layout)

**Description**:
Create dashboard layout that enforces authentication and displays navigation.

**Expected Outcome**:
File: `frontend/app/dashboard/layout.tsx`

**Features**:
- Wraps children with ProtectedRoute
- Navigation bar with logout button
- User email display (from JWT - optional)

**Logic**:
1. ProtectedRoute checks authentication
2. If authenticated, render NavBar + children
3. Logout button clears token and redirects to `/`

**Acceptance Criteria**:
- [ ] Layout uses ProtectedRoute component
- [ ] Unauthenticated users redirected to login
- [ ] Navigation bar displays
- [ ] Logout button clears token from localStorage
- [ ] Logout redirects to `/`

---

### Task 21: Create Dashboard Placeholder Page

**Layer**: Frontend
**Dependencies**: Task 20
**Priority**: P0

**Spec Reference**:
- `specs/ui/pages.md` (Dashboard page)

**Description**:
Create a simple dashboard page to verify authentication flow (placeholder for task list).

**Expected Outcome**:
File: `frontend/app/dashboard/page.tsx`

**Content**:
- Page title: "My Tasks"
- Message: "Task list will be implemented in next phase"
- Logout button (or uses one from layout)

**Acceptance Criteria**:
- [ ] Page renders when authenticated
- [ ] Protected route prevents unauthenticated access
- [ ] Page displays user is logged in

---

### Task 22: Implement Auto-Redirect for Logged-in Users

**Layer**: Frontend
**Dependencies**: Task 18
**Priority**: P1

**Spec Reference**:
- `specs/ui/pages.md` (Login page redirect behavior)

**Description**:
Add logic to login and register pages to redirect already-logged-in users to dashboard.

**Expected Outcome**:
Updated files: `app/page.tsx`, `app/register/page.tsx`

**Logic**:
- On page load, check if token exists in localStorage
- If exists and not expired, redirect to `/dashboard`

**Acceptance Criteria**:
- [ ] Login page redirects if token exists
- [ ] Register page redirects if token exists
- [ ] Logged-in users can't access login/register pages

---

## Phase 6: Integration & Testing

### Task 23: Write Backend Unit Tests for Auth Utilities

**Layer**: Backend (Testing)
**Dependencies**: Tasks 7, 8
**Priority**: P1

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Section 9.1)

**Description**:
Create unit tests for password hashing and JWT utilities.

**Expected Outcome**:
File: `backend/tests/test_auth_utils.py`

**Test Coverage**:
- `test_hash_password()` - Returns bcrypt hash
- `test_verify_password_correct()` - Returns True for correct password
- `test_verify_password_incorrect()` - Returns False for incorrect password
- `test_create_access_token()` - Generates valid JWT
- `test_verify_token_valid()` - Decodes valid token
- `test_verify_token_expired()` - Raises error for expired token
- `test_verify_token_invalid_signature()` - Raises error for tampered token

**Acceptance Criteria**:
- [ ] All tests defined
- [ ] Tests pass with `pytest`
- [ ] Coverage > 90% for auth utilities

---

### Task 24: Write Backend Integration Tests for Auth Endpoints

**Layer**: Backend (Testing)
**Dependencies**: Tasks 11, 12
**Priority**: P0

**Spec Reference**:
- `specs/features/authentication.md` (Test Scenarios)
- `specs/features/plans/authentication-plan.md` (Section 9.1)

**Description**:
Create integration tests for registration and login endpoints.

**Expected Outcome**:
File: `backend/tests/test_auth_endpoints.py`

**Test Coverage**:
- **Registration**:
  - `test_register_success()` - Returns 201 with user object
  - `test_register_duplicate_email()` - Returns 400
  - `test_register_invalid_email()` - Returns 422
  - `test_register_short_password()` - Returns 422
  - `test_register_email_case_insensitive()` - Normalizes email

- **Login**:
  - `test_login_success()` - Returns 200 with JWT
  - `test_login_invalid_password()` - Returns 401
  - `test_login_nonexistent_email()` - Returns 401
  - `test_login_case_insensitive_email()` - Works with any case

- **JWT Validation**:
  - `test_protected_endpoint_with_valid_token()` - Returns 200
  - `test_protected_endpoint_without_token()` - Returns 401
  - `test_protected_endpoint_with_expired_token()` - Returns 401

**Acceptance Criteria**:
- [ ] All tests defined and passing
- [ ] Uses test database (not production)
- [ ] Database cleaned between tests
- [ ] Coverage > 80% for auth endpoints

---

### Task 25: Write User Isolation Security Test

**Layer**: Backend (Testing)
**Dependencies**: Task 24
**Priority**: P0 (Critical for security)

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Section 9.1 - Security Tests)

**Description**:
Create security test to verify user isolation (user A cannot access user B's data).

**Expected Outcome**:
File: `backend/tests/test_security.py`

**Test**: `test_user_isolation_on_protected_endpoint()`

**Logic** (example with placeholder endpoint):
1. Create User A, login, get token_a
2. Create User B, login, get token_b
3. User A creates a resource (will be task in next phase)
4. User B attempts to access User A's resource with token_b
5. Assert: Returns 404 (not 200, not 403)

**Acceptance Criteria**:
- [ ] Test creates two users
- [ ] Test verifies cross-user access returns 404
- [ ] Test passes (user isolation enforced)
- [ ] Can be extended for task CRUD in next phase

---

### Task 26: Write Frontend E2E Tests for Auth Flow

**Layer**: Frontend (Testing)
**Dependencies**: Tasks 18, 19, 20
**Priority**: P1

**Spec Reference**:
- `specs/features/plans/authentication-plan.md` (Section 9.2)

**Description**:
Create end-to-end tests for authentication user flows using Playwright or Cypress.

**Expected Outcome**:
File: `frontend/tests/e2e/auth.spec.ts`

**Test Coverage**:
- `test_registration_flow()` - Register → success message → redirect
- `test_login_flow()` - Login → redirect to dashboard
- `test_logout_flow()` - Logout → redirect to login
- `test_protected_route_without_token()` - Dashboard redirects to login
- `test_already_logged_in_redirects()` - Login page redirects to dashboard

**Acceptance Criteria**:
- [ ] E2E framework installed (Playwright or Cypress)
- [ ] All tests defined and passing
- [ ] Tests run against local backend API
- [ ] Token storage/removal verified

---

### Task 27: Create Manual Testing Checklist

**Layer**: Both (Documentation)
**Dependencies**: All implementation tasks
**Priority**: P1

**Spec Reference**:
- `specs/features/authentication.md` (Acceptance Criteria Summary)

**Description**:
Create a manual testing checklist for QA to verify authentication implementation.

**Expected Outcome**:
File: `specs/features/tasks/authentication-manual-testing.md`

**Checklist Items**:
- [ ] User can register with valid email/password
- [ ] Duplicate email shows error
- [ ] Invalid email format shows error
- [ ] Short password shows error
- [ ] User can login with registered credentials
- [ ] Invalid credentials show error (no enumeration)
- [ ] Token stored in localStorage after login
- [ ] Dashboard accessible after login
- [ ] Dashboard redirects to login when not authenticated
- [ ] Logout clears token and redirects to login
- [ ] Already logged-in users can't access login page
- [ ] Token expires after 24 hours (or configured time)
- [ ] API returns 401 for requests without token
- [ ] API returns 401 for requests with expired token

**Acceptance Criteria**:
- [ ] Checklist document created
- [ ] All scenarios from specs included
- [ ] Clear pass/fail criteria for each item

---

## Task Dependencies Graph

```
Phase 1: Backend Setup
├── Task 1: Backend Project Structure
├── Task 2: Install Backend Dependencies (depends on Task 1)
└── Task 3: Configure Environment (depends on Task 2)

Phase 2: Database Setup
├── Task 4: Create User Model (depends on Task 3)
├── Task 5: Setup DB Connection (depends on Task 4)
└── Task 6: Create Migration (depends on Task 5)

Phase 3: Backend Authentication
├── Task 7: Password Hashing (depends on Task 2)
├── Task 8: JWT Utilities (depends on Task 3)
├── Task 9: Pydantic Schemas (depends on Task 2)
├── Task 10: get_current_user_id Dependency (depends on Task 8)
├── Task 11: POST /register (depends on Tasks 6, 7, 9)
└── Task 12: POST /login (depends on Tasks 7, 8, 9)

Phase 4: Frontend Setup
├── Task 13: Frontend Project
├── Task 14: Install Frontend Dependencies (depends on Task 13)
└── Task 15: TypeScript Types (depends on Task 13)

Phase 5: Frontend Authentication
├── Task 16: API Client (depends on Task 15)
├── Task 17: ProtectedRoute Component (depends on Task 13)
├── Task 18: Login Page (depends on Tasks 15, 16)
├── Task 19: Registration Page (depends on Tasks 15, 16)
├── Task 20: Dashboard Layout (depends on Task 17)
├── Task 21: Dashboard Page (depends on Task 20)
└── Task 22: Auto-Redirect (depends on Task 18)

Phase 6: Testing
├── Task 23: Backend Unit Tests (depends on Tasks 7, 8)
├── Task 24: Backend Integration Tests (depends on Tasks 11, 12)
├── Task 25: Security Test (depends on Task 24)
├── Task 26: Frontend E2E Tests (depends on Tasks 18, 19, 20)
└── Task 27: Manual Testing Checklist (depends on all)
```

---

## Task Summary

**Total Tasks**: 27
**Critical Path Tasks** (P0): 22
**Enhancement Tasks** (P1): 5

**By Layer**:
- Backend: 12 tasks (Tasks 1-12)
- Frontend: 9 tasks (Tasks 13-22)
- Testing: 5 tasks (Tasks 23-27)
- Documentation: 1 task (Task 27)

**By Phase**:
- Phase 1 (Backend Setup): 3 tasks
- Phase 2 (Database): 3 tasks
- Phase 3 (Backend Auth): 6 tasks
- Phase 4 (Frontend Setup): 3 tasks
- Phase 5 (Frontend Auth): 7 tasks
- Phase 6 (Testing): 5 tasks

**Estimated Completion**:
- Backend: ~8-12 hours (Tasks 1-12)
- Frontend: ~6-10 hours (Tasks 13-22)
- Testing: ~4-6 hours (Tasks 23-27)
- **Total**: ~18-28 hours for complete authentication implementation

---

## Next Steps After Completion

Once all 27 tasks are completed:

1. **Verify Acceptance Criteria**: Ensure all checkboxes are checked for each task
2. **Run Full Test Suite**: All tests (unit, integration, E2E) must pass
3. **Security Audit**: Review user isolation implementation (Task 25 critical)
4. **Create ADR-002**: Document JWT authentication decision
5. **Update PHR**: Record implementation completion
6. **Proceed to Task CRUD**: Authentication is prerequisite for F002 (Task CRUD)

---

**Task Breakdown Author**: AI Agent
**Review Status**: Pending User Approval
**Next Command**: `/sp.implement` after task approval
