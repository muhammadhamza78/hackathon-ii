# Technical Implementation Plan: JWT-Based Authentication

**Feature**: F001 - User Authentication
**Version**: 1.0.0
**Created**: 2025-12-30
**Status**: Plan
**References**:
- `specs/features/authentication.md`
- `specs/architecture.md` (Section 2: Decision 2)
- `specs/api/rest-endpoints.md` (Auth endpoints)

---

## Executive Summary

This plan details the technical implementation of JWT-based authentication for the Task Management System, covering token issuance from the backend (FastAPI), secure transmission to the frontend (Next.js), and enforcement of user identity across all protected operations.

**Key Design Principle**: Backend is the single source of truth for authentication. Frontend is a thin client that stores and transmits JWT tokens but NEVER validates or trusts token claims directly.

---

## 1. JWT Token Structure and Claims

### Token Specification

**Algorithm**: HS256 (HMAC with SHA-256)
**Secret Key**: 256-bit minimum (32+ characters), stored in `JWT_SECRET_KEY` environment variable
**Expiry**: 24 hours (86400 seconds), configurable via `JWT_EXPIRY_HOURS`

### JWT Payload (Claims)

```json
{
  "sub": "123",
  "email": "user@example.com",
  "exp": 1735650000,
  "iat": 1735563600
}
```

**Standard Claims**:
- `sub` (subject): User ID as **string** (not integer) - JWT standard requires string
- `exp` (expiration): Unix timestamp when token expires
- `iat` (issued at): Unix timestamp when token was issued

**Custom Claims**:
- `email`: User email address (for display purposes only, NOT for authorization)

**Security Note**: The `sub` claim is the authoritative user identity. All authorization decisions MUST use `sub`, never `email` or any other claim.

### Token Format

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Encoded Token Example**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2NTAwMDAsImlhdCI6MTczNTU2MzYwMH0.signature_here
```

**Format**: `{header}.{payload}.{signature}` (Base64URL encoded)

---

## 2. Backend (FastAPI) Implementation Design

### 2.1 Registration Flow

**Endpoint**: `POST /api/auth/register`

**Step-by-Step Logic**:

1. **Request Validation** (Pydantic schema):
   - Email: valid format, max 255 chars
   - Password: min 8 chars, max 128 chars

2. **Email Normalization**:
   - Convert to lowercase: `email.lower().strip()`
   - Ensures case-insensitive uniqueness

3. **Duplicate Check**:
   - Query database: `SELECT id FROM users WHERE email = ?`
   - If exists → return 400 "Email already registered"

4. **Password Hashing**:
   - Library: `passlib` with `bcrypt` backend
   - Cost factor: 12 (approx 250-500ms hashing time)
   - Salt: Automatically handled by bcrypt
   - Example: `pwd_context.hash(password)` → `$2b$12$...`

5. **User Creation**:
   - Insert into database with hashed password
   - Auto-generate `id` (serial primary key)
   - Set `created_at` and `updated_at` to current UTC timestamp

6. **Response**:
   - Return user object WITHOUT password
   - Status: 201 Created

**Security Consideration**: Password NEVER leaves memory in plaintext after hashing. Use secure string handling (e.g., clear password variable after hashing).

---

### 2.2 Login Flow and JWT Issuance

**Endpoint**: `POST /api/auth/login`

**Step-by-Step Logic**:

1. **Request Validation**:
   - Email and password both required

2. **Email Normalization**:
   - Convert to lowercase: `email.lower().strip()`

3. **User Lookup**:
   - Query database: `SELECT id, email, hashed_password FROM users WHERE email = ?`
   - If NOT found → 401 "Invalid credentials" (do NOT reveal email doesn't exist)

4. **Password Verification**:
   - Use bcrypt's constant-time comparison
   - Library: `pwd_context.verify(plain_password, hashed_password)`
   - If invalid → 401 "Invalid credentials" (do NOT reveal password is wrong)

5. **JWT Token Generation**:
   ```python
   import jose.jwt as jwt
   from datetime import datetime, timedelta

   # Prepare payload
   payload = {
       "sub": str(user.id),  # MUST be string per JWT spec
       "email": user.email,
       "iat": datetime.utcnow(),
       "exp": datetime.utcnow() + timedelta(hours=24)
   }

   # Sign token
   token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
   ```

6. **Response**:
   ```json
   {
     "access_token": "eyJhbG...",
     "token_type": "Bearer",
     "expires_in": 86400
   }
   ```

**Error Handling**:
- 401 for invalid credentials (email OR password wrong)
- 422 for validation errors (missing fields)
- NEVER distinguish between "email not found" and "password incorrect"

**Security Consideration**: Use constant-time comparison for passwords to prevent timing attacks. `passlib` handles this automatically.

---

### 2.3 JWT Verification Strategy

**Implementation**: FastAPI Dependency Injection

**Core Function**: `get_current_user_id()`

**Step-by-Step Logic**:

1. **Extract Authorization Header**:
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

   security = HTTPBearer()

   async def get_current_user_id(
       credentials: HTTPAuthorizationCredentials = Depends(security)
   ) -> int:
   ```

2. **Extract Token**:
   - Header format: `Authorization: Bearer <token>`
   - `HTTPBearer()` automatically validates format
   - Extract token: `credentials.credentials`

3. **Verify and Decode Token**:
   ```python
   from jose import jwt, JWTError

   try:
       payload = jwt.decode(
           credentials.credentials,
           JWT_SECRET_KEY,
           algorithms=["HS256"]
       )
   except JWTError:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Unauthorized"
       )
   ```

4. **Verify Expiry**:
   - `jose.jwt.decode()` automatically checks `exp` claim
   - If expired, raises `JWTError`

5. **Extract User ID**:
   ```python
   user_id_str = payload.get("sub")
   if not user_id_str:
       raise HTTPException(status_code=401, detail="Unauthorized")

   try:
       user_id = int(user_id_str)
   except ValueError:
       raise HTTPException(status_code=401, detail="Unauthorized")

   return user_id
   ```

6. **Return User ID**:
   - Type: `int`
   - Guaranteed to be valid and authenticated

**Error Cases → 401 Unauthorized**:
- Missing `Authorization` header
- Invalid header format (not "Bearer <token>")
- Invalid token signature
- Token expired (`exp` claim)
- Token malformed (invalid Base64, missing claims)
- Missing `sub` claim
- Invalid `sub` value (not convertible to integer)

**Security Consideration**:
- NEVER query database during token validation (defeats stateless design)
- User deletion/suspension: Token remains valid until expiry (acceptable for MVP)
- Future: Implement token blacklist if server-side revocation needed

---

### 2.4 Protected Endpoint Pattern

**Usage in All Protected Endpoints**:

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/api/tasks")
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # user_id is GUARANTEED to be valid and authenticated
    # Use it for ALL database queries
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"tasks": tasks}
```

**Key Points**:
- `user_id` is injected by FastAPI dependency system
- If JWT is invalid, `get_current_user_id()` raises 401 BEFORE endpoint logic runs
- Endpoint logic can TRUST that `user_id` is authenticated

---

### 2.5 User ID Enforcement in Database Queries

**CRITICAL SECURITY RULE**: Every query on `tasks` table MUST filter by `user_id`

**Correct Pattern**:
```python
# CREATE: Auto-assign user_id from JWT
task = Task(
    title=request.title,
    description=request.description,
    status=request.status,
    user_id=user_id  # From JWT, NOT from request body
)

# READ: Filter by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# UPDATE: Verify ownership
task = session.exec(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Ensures user owns this task
    )
).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Verify ownership
task = session.exec(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
session.delete(task)
```

**WRONG Patterns** (Security Vulnerabilities):
```python
# ❌ NEVER accept user_id from request body
task = Task(
    title=request.title,
    user_id=request.user_id  # WRONG! User can spoof this
)

# ❌ NEVER query without user_id filter
tasks = session.exec(select(Task)).all()  # WRONG! Returns all users' tasks

# ❌ NEVER trust URL parameter for user_id
@router.get("/api/users/{user_id}/tasks")
async def list_user_tasks(user_id: int):  # WRONG! User can access others' data
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
```

**Security Consideration**: When task is not found OR user doesn't own it, ALWAYS return 404 (not 403). Returning 403 reveals that the task exists but belongs to someone else (information leak).

---

## 3. Frontend (Next.js) Implementation Design

### 3.1 Registration Flow

**Page**: `/register` (`app/register/page.tsx`)

**Step-by-Step Logic**:

1. **User Input**:
   - Email field (type="email")
   - Password field (type="password")

2. **Client-Side Validation** (before API call):
   - Email format check (HTML5 validation + regex)
   - Password length check (min 8, max 128)
   - Display errors inline

3. **API Call**:
   ```typescript
   const response = await fetch('http://localhost:8000/api/auth/register', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ email, password })
   });
   ```

4. **Handle Response**:
   - **201 Created**: Redirect to `/` (login page) with success message
   - **400 Bad Request**: Display "Email already registered"
   - **422 Validation Error**: Display field-specific errors
   - **Network Error**: Display "Unable to connect. Please try again."

5. **Success Flow**:
   - Store success message in URL param or session storage
   - Redirect to login: `router.push('/?message=registered')`
   - Login page displays: "Account created! Please log in."

**Security Consideration**: NEVER store password in any browser storage (localStorage, sessionStorage, cookies). Password exists only in form state during registration.

---

### 3.2 Login Flow and Token Storage

**Page**: `/` (login page) (`app/page.tsx`)

**Step-by-Step Logic**:

1. **User Input**:
   - Email field
   - Password field

2. **Client-Side Validation**:
   - Email and password both required

3. **API Call**:
   ```typescript
   const response = await fetch('http://localhost:8000/api/auth/login', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ email, password })
   });

   if (!response.ok) {
     const error = await response.json();
     setError(error.detail);
     return;
   }

   const data = await response.json();
   // data = { access_token, token_type, expires_in }
   ```

4. **Token Storage** (on success):
   ```typescript
   // Option 1: localStorage (persists across tabs/sessions)
   localStorage.setItem('token', data.access_token);

   // Option 2: sessionStorage (session only, more secure)
   sessionStorage.setItem('token', data.access_token);

   // Optionally store expiry
   const expiryTime = Date.now() + (data.expires_in * 1000);
   localStorage.setItem('token_expiry', expiryTime.toString());
   ```

5. **Redirect**:
   ```typescript
   router.push('/dashboard');
   ```

6. **Error Handling**:
   - **401 Unauthorized**: Display "Invalid email or password"
   - **422 Validation Error**: Display field errors
   - **Network Error**: Display connection error

**Storage Choice**:
- **localStorage**: Persists across browser tabs and restarts (better UX)
- **sessionStorage**: Cleared when tab closes (better security)
- **Recommendation**: Use `localStorage` for MVP, add "Remember me" toggle later

**Security Consideration**:
- XSS Risk: JWT in localStorage is vulnerable to XSS attacks. Mitigate with:
  - Strict Content Security Policy (CSP)
  - No inline scripts
  - Sanitize all user inputs
- Alternative: Use HttpOnly cookies (requires backend to set cookie, more complex setup)

---

### 3.3 Token Transmission to Backend

**Pattern**: Include JWT token in `Authorization` header for ALL protected API requests

**Implementation** (API client utility):

```typescript
// lib/api.ts
export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle 401 globally (token expired or invalid)
  if (response.status === 401) {
    // Clear token and redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('token_expiry');
    window.location.href = '/';
  }

  return response;
}

// Usage
const response = await apiRequest('/api/tasks', { method: 'GET' });
const data = await response.json();
```

**Key Points**:
- Token is added automatically to all requests via utility function
- 401 responses trigger global logout (clear token, redirect to login)
- Frontend NEVER parses or validates JWT payload (backend responsibility)

**Security Consideration**: NEVER send token in URL query parameters or request body. Always use `Authorization` header.

---

### 3.4 Protected Route Handling

**Pattern**: Redirect unauthenticated users to login before rendering protected pages

**Implementation** (middleware or layout):

**Option 1: Server Component (Preferred for Next.js App Router)**:
```typescript
// app/dashboard/layout.tsx
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default function DashboardLayout({ children }) {
  const token = cookies().get('token');

  if (!token) {
    redirect('/');
  }

  return <>{children}</>;
}
```

**Option 2: Client Component**:
```typescript
// components/ProtectedRoute.tsx
'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function ProtectedRoute({ children }) {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expiry = localStorage.getItem('token_expiry');

    if (!token || (expiry && Date.now() > parseInt(expiry))) {
      // No token or expired
      localStorage.removeItem('token');
      localStorage.removeItem('token_expiry');
      router.push('/');
    }
  }, [router]);

  // Optimistic render (assumes token exists)
  return <>{children}</>;
}

// Usage in page
export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  );
}
```

**Comparison**:
- **Server Component**: No flash of content, more secure (token in httpOnly cookie)
- **Client Component**: Easier to implement, token in localStorage

**Recommendation**: Start with **Client Component** (Option 2) for simplicity. Migrate to **Server Component** (Option 1) if httpOnly cookies are implemented.

---

### 3.5 Logout Flow

**Process**:

1. **Remove Token from Storage**:
   ```typescript
   function handleLogout() {
     localStorage.removeItem('token');
     localStorage.removeItem('token_expiry');

     // Optionally call backend to log event (for analytics)
     // await apiRequest('/api/auth/logout', { method: 'POST' });

     router.push('/');
   }
   ```

2. **Redirect to Login**:
   - Navigate to `/` (login page)

**Backend Endpoint** (optional, for analytics only):
- `POST /api/auth/logout` (no-op for JWT, just logs event)
- Token remains valid until expiry (stateless JWT limitation)

**Security Consideration**: Client-side logout is NOT secure (user can keep token). Token remains valid until expiry. For secure logout, implement token blacklist on backend (out of scope for MVP).

---

## 4. User ID Extraction and Enforcement

### 4.1 Backend: Extracting user_id from JWT

**Already covered in Section 2.3** (JWT Verification Strategy)

**Key Points**:
- `user_id` extracted from `sub` claim
- Converted from string to integer
- Injected into endpoint as dependency
- NO database query needed during extraction

---

### 4.2 Backend: Enforcing user_id in Queries

**Pattern**: Every database query on `tasks` table MUST include `WHERE user_id = ?`

**CREATE**:
```python
@router.post("/api/tasks")
async def create_task(
    request: CreateTaskRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        user_id=user_id  # Auto-assign from JWT
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**READ (List)**:
```python
@router.get("/api/tasks")
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"tasks": tasks}
```

**READ (Single)**:
```python
@router.get("/api/tasks/{task_id}")
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Ownership check
        )
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
```

**UPDATE**:
```python
@router.put("/api/tasks/{task_id}")
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**DELETE**:
```python
@router.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    task = session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return
```

**Testing Enforcement**:
- Unit test: Verify `WHERE` clause includes `user_id`
- Integration test: User A creates task, User B attempts to access → 404

---

### 4.3 Frontend: NO user_id Handling

**Critical Point**: Frontend NEVER extracts, parses, or validates user_id from JWT token.

**Wrong Pattern** (DO NOT DO THIS):
```typescript
// ❌ WRONG: Parsing JWT on frontend
const payload = JSON.parse(atob(token.split('.')[1]));
const userId = payload.sub;  // NEVER TRUST THIS
```

**Reason**: Client-side code is not trustworthy. A malicious user can modify JWT in browser and claim any user_id. Backend MUST be the sole authority on user identity.

**Correct Pattern**: Frontend treats JWT as opaque token, only includes it in `Authorization` header. Backend handles all user_id extraction and validation.

---

## 5. Error Handling: Unauthorized vs Forbidden

### 5.1 HTTP Status Codes

**401 Unauthorized**: Authentication failed (who are you?)
- Missing JWT token
- Invalid JWT signature
- Expired JWT token
- Malformed JWT token

**404 Not Found**: Resource not found OR user doesn't own resource (what you want doesn't exist or you can't see it)
- Task with given ID doesn't exist
- Task exists but belongs to different user (ownership check failed)

**403 Forbidden**: NOT USED in this system
- Reason: Revealing "exists but you can't access it" is an information leak
- Instead: Return 404 for both "doesn't exist" and "not yours"

**422 Validation Error**: Request data invalid
- Missing required fields
- Invalid data types
- Constraint violations (e.g., email format, password length)

---

### 5.2 Backend Error Responses

**401 Unauthorized**:
```python
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized"
)
```

**Response**:
```json
{
  "detail": "Unauthorized"
}
```

**404 Not Found** (resource missing OR not owned):
```python
if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
```

**Response**:
```json
{
  "detail": "Task not found"
}
```

**422 Validation Error** (automatic via Pydantic):
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

### 5.3 Frontend Error Handling

**Global 401 Handling** (in API client):
```typescript
if (response.status === 401) {
  // Token invalid or expired
  localStorage.removeItem('token');
  localStorage.removeItem('token_expiry');
  window.location.href = '/';  // Redirect to login
  return;
}
```

**404 Handling** (in component):
```typescript
if (response.status === 404) {
  setError('Task not found');
  // Optionally redirect back to task list
}
```

**422 Validation Error Handling**:
```typescript
if (response.status === 422) {
  const errors = await response.json();
  // Display field-specific errors
  errors.detail.forEach(err => {
    const field = err.loc[err.loc.length - 1];
    setFieldError(field, err.msg);
  });
}
```

---

## 6. Responsibility Matrix

| Responsibility | Frontend (Next.js) | Backend (FastAPI) |
|----------------|-------------------|-------------------|
| **Password Hashing** | ❌ Never | ✅ Yes (bcrypt, cost 12) |
| **JWT Token Generation** | ❌ Never | ✅ Yes (on login) |
| **JWT Token Signing** | ❌ Never | ✅ Yes (HS256, secret key) |
| **JWT Token Storage** | ✅ Yes (localStorage/sessionStorage) | ❌ No |
| **JWT Token Transmission** | ✅ Yes (Authorization header) | ❌ No (receives via header) |
| **JWT Token Validation** | ❌ Never (treats as opaque) | ✅ Yes (signature, expiry) |
| **user_id Extraction** | ❌ Never | ✅ Yes (from `sub` claim) |
| **user_id Enforcement** | ❌ Never | ✅ Yes (in all queries) |
| **Ownership Verification** | ❌ Never | ✅ Yes (WHERE user_id = ?) |
| **401 Error Handling** | ✅ Yes (logout + redirect) | ✅ Yes (raise exception) |
| **404 Error Display** | ✅ Yes (show message) | ✅ Yes (return 404) |
| **Client-Side Validation** | ✅ Yes (email, password length) | ❌ No (redundant) |
| **Server-Side Validation** | ❌ No | ✅ Yes (Pydantic schemas) |
| **HTTPS Enforcement** | ❌ No (browser handles) | ✅ Yes (in production) |
| **CORS Configuration** | ❌ No | ✅ Yes (allow frontend origin) |
| **Secret Key Management** | ❌ Never has access | ✅ Yes (env variable) |
| **Token Expiry Check (client)** | ✅ Optional (UX optimization) | ✅ Yes (authoritative) |
| **Logout** | ✅ Yes (remove token) | ❌ No (stateless) |

---

## 7. Security Considerations

### 7.1 JWT Secret Key Management

**Requirements**:
- **Length**: Minimum 32 characters (256-bit)
- **Randomness**: Cryptographically secure random string
- **Storage**: Environment variable (`JWT_SECRET_KEY`), NEVER in code
- **Rotation**: Different secret per environment (dev, staging, prod)

**Generation** (example):
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

**Environment Setup**:
```bash
# .env (backend)
JWT_SECRET_KEY=your-super-secret-256-bit-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
```

**CRITICAL**: Add `.env` to `.gitignore`. NEVER commit secrets to version control.

---

### 7.2 Token Transmission Security

**HTTPS in Production**:
- REQUIRED for production deployment
- JWT tokens transmitted in plain text over HTTP are vulnerable to interception
- Local development: HTTP acceptable (localhost only)

**Authorization Header** (not URL/body):
- ✅ Correct: `Authorization: Bearer <token>`
- ❌ Wrong: `/api/tasks?token=<token>` (logged in server logs, browser history)
- ❌ Wrong: `{ "token": "<token>" }` in request body (non-standard)

---

### 7.3 XSS (Cross-Site Scripting) Protection

**Risk**: JWT stored in localStorage/sessionStorage is vulnerable to XSS attacks.

**Mitigations**:
1. **Content Security Policy (CSP)**:
   - Disallow inline scripts
   - Whitelist trusted script sources

2. **Input Sanitization**:
   - Sanitize all user inputs before rendering (React does this by default)
   - NEVER use `dangerouslySetInnerHTML` with user content

3. **HttpOnly Cookies** (future enhancement):
   - Store JWT in httpOnly cookie (not accessible to JavaScript)
   - Backend sets cookie on login
   - Browser automatically includes cookie in requests
   - More secure but requires backend to handle cookie setting

---

### 7.4 CSRF (Cross-Site Request Forgery) Protection

**Risk**: If using cookies for JWT storage, vulnerable to CSRF attacks.

**Current Design**: Using `Authorization` header (not cookies) → NOT vulnerable to CSRF

**If Migrating to HttpOnly Cookies**:
- Implement CSRF tokens (SameSite cookie attribute, CSRF token in header)
- Out of scope for MVP

---

### 7.5 Password Security

**Hashing**:
- ✅ bcrypt (cost 12) or argon2
- ❌ NOT MD5, SHA1, SHA256 (too fast, not designed for passwords)

**Salt**:
- Automatically handled by bcrypt/argon2
- Unique salt per password

**Storage**:
- Plaintext password NEVER logged or stored
- Clear password from memory after hashing

**Transmission**:
- HTTPS in production (password transmitted encrypted)
- POST body (not URL query parameter)

---

### 7.6 Token Expiry and Revocation

**Expiry**:
- 24 hours (86400 seconds)
- Backend checks `exp` claim automatically
- Client can optionally check expiry for UX (pre-emptive logout)

**Revocation** (Limitation of Stateless JWT):
- Token CANNOT be invalidated before expiry
- If user logs out, token remains valid until expiry
- Acceptable for MVP (24-hour window)

**Future Enhancement** (out of scope):
- Token blacklist on backend (store revoked tokens in Redis)
- Refresh tokens (short-lived access token + long-lived refresh token)

---

### 7.7 User Enumeration Prevention

**Registration**:
- When email already exists → 400 "Email already registered"
- Acceptable to reveal existence (UX tradeoff)

**Login**:
- When email OR password wrong → 401 "Invalid credentials"
- NEVER distinguish between "email not found" and "password incorrect"
- Prevents attackers from enumerating valid emails

---

## 8. Authentication Flow Diagrams

### 8.1 Registration Flow

```
User                 Frontend              Backend               Database
 |                      |                     |                      |
 |-- Enter email/pw --->|                     |                      |
 |                      |-- POST /register -->|                      |
 |                      |                     |-- Normalize email -->|
 |                      |                     |-- Check duplicate -->|
 |                      |                     |<-- Email exists? ----|
 |                      |                     |                      |
 |                      |                     |-- Hash password ---->|
 |                      |                     |-- INSERT user ------>|
 |                      |                     |<-- User created -----|
 |                      |<-- 201 Created -----|                      |
 |<-- Redirect to / ----|                     |                      |
 |                      |                     |                      |
```

### 8.2 Login Flow

```
User                 Frontend              Backend               Database
 |                      |                     |                      |
 |-- Enter email/pw --->|                     |                      |
 |                      |-- POST /login ----->|                      |
 |                      |                     |-- Normalize email -->|
 |                      |                     |-- SELECT user ------>|
 |                      |                     |<-- User data --------|
 |                      |                     |-- Verify password -->|
 |                      |                     |-- Generate JWT ----->|
 |                      |<-- 200 + JWT -------|                      |
 |                      |-- Store token ----->|                      |
 |<-- Redirect to /dash-|                     |                      |
 |                      |                     |                      |
```

### 8.3 Protected Request Flow

```
User                 Frontend              Backend               Database
 |                      |                     |                      |
 |-- Request tasks ---->|                     |                      |
 |                      |-- GET /api/tasks -->|                      |
 |                      |  (Authorization:    |                      |
 |                      |   Bearer <token>)   |                      |
 |                      |                     |-- Verify JWT ------->|
 |                      |                     |-- Extract user_id -->|
 |                      |                     |-- SELECT tasks ------>|
 |                      |                     |  WHERE user_id=? ---->|
 |                      |                     |<-- Tasks -------------|
 |                      |<-- 200 + tasks -----|                      |
 |<-- Display tasks ----|                     |                      |
 |                      |                     |                      |
```

### 8.4 Unauthorized Request Flow

```
User                 Frontend              Backend
 |                      |                     |
 |-- Request tasks ---->|                     |
 |   (no token)         |-- GET /api/tasks -->|
 |                      |  (no Auth header)   |
 |                      |                     |-- Verify JWT ------->|
 |                      |                     |   (missing)          |
 |                      |<-- 401 Unauthorized-|                      |
 |                      |-- Clear token ----->|                      |
 |<-- Redirect to / ----|                     |                      |
 |                      |                     |                      |
```

---

## 9. Testing Strategy

### 9.1 Backend Tests

**Unit Tests**:
- Password hashing (bcrypt)
- JWT token generation
- JWT token validation
- user_id extraction from JWT

**Integration Tests**:
- Registration endpoint (201, 400, 422)
- Login endpoint (200, 401, 422)
- Protected endpoints with valid token (200)
- Protected endpoints without token (401)
- Protected endpoints with expired token (401)
- Protected endpoints with invalid signature (401)

**Security Tests**:
- Cross-user access attempts (User A tries to access User B's task → 404)
- user_id spoofing in request body (should be ignored)
- Token tampering (modify payload → 401)

**Example Test** (pytest):
```python
def test_user_isolation(client, db_session):
    # User A registers and logs in
    user_a = create_user(db_session, "a@example.com", "password")
    token_a = login_user(client, "a@example.com", "password")

    # User A creates task
    response = client.post(
        "/api/tasks",
        json={"title": "Task A"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    task_id = response.json()["id"]

    # User B registers and logs in
    user_b = create_user(db_session, "b@example.com", "password")
    token_b = login_user(client, "b@example.com", "password")

    # User B tries to access User A's task
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
```

---

### 9.2 Frontend Tests

**Component Tests**:
- Login form validation
- Registration form validation
- Token storage after successful login
- Token removal on logout

**Integration Tests**:
- Login flow (UI → API → redirect)
- Registration flow (UI → API → redirect)
- Protected route redirect (no token → login page)
- API client includes Authorization header

**End-to-End Tests** (Playwright/Cypress):
- Full registration + login flow
- Login → create task → logout
- Access protected page without token (redirects to login)

---

## 10. Implementation Checklist

### Backend

- [ ] Install dependencies: `passlib[bcrypt]`, `python-jose[cryptography]`, `python-multipart`
- [ ] Configure environment variables: `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRY_HOURS`
- [ ] Create User model (SQLModel) with email and hashed_password
- [ ] Implement password hashing utility (passlib)
- [ ] Implement JWT generation utility (jose)
- [ ] Implement JWT validation utility (jose)
- [ ] Create `get_current_user_id()` dependency
- [ ] Implement `POST /api/auth/register` endpoint
- [ ] Implement `POST /api/auth/login` endpoint
- [ ] Apply `get_current_user_id` dependency to all protected endpoints
- [ ] Enforce `WHERE user_id = ?` in all task queries
- [ ] Write unit tests for auth utilities
- [ ] Write integration tests for auth endpoints
- [ ] Write security tests for user isolation

### Frontend

- [ ] Create login page (`app/page.tsx`)
- [ ] Create registration page (`app/register/page.tsx`)
- [ ] Implement token storage (localStorage)
- [ ] Implement API client utility with Authorization header
- [ ] Implement global 401 error handling (logout + redirect)
- [ ] Implement ProtectedRoute component
- [ ] Apply ProtectedRoute to dashboard pages
- [ ] Implement logout functionality
- [ ] Write component tests for forms
- [ ] Write E2E tests for auth flows

---

## 11. Open Questions and Future Enhancements

### Open Questions

**Q1**: Should we use localStorage or sessionStorage for JWT storage?
- **Recommendation**: localStorage (better UX, persists across tabs)
- **Alternative**: sessionStorage (better security, session only)

**Q2**: Should we implement client-side token expiry check?
- **Recommendation**: Yes (optional, for UX optimization)
- **Implementation**: Check expiry before API calls, pre-emptive logout

**Q3**: Should we add a "Remember me" checkbox?
- **Recommendation**: Not in MVP
- **Future**: Use shorter expiry (1 hour) if unchecked, longer (7 days) if checked

### Future Enhancements (Out of Scope for MVP)

1. **Refresh Tokens**:
   - Short-lived access token (15 mins) + long-lived refresh token (7 days)
   - More secure but more complex

2. **Token Blacklist**:
   - Store revoked tokens in Redis
   - Check blacklist during token validation
   - Enables server-side logout

3. **HttpOnly Cookies**:
   - Store JWT in httpOnly cookie (not accessible to JavaScript)
   - More secure against XSS
   - Requires CSRF protection

4. **Rate Limiting**:
   - Limit login attempts (5 per minute per IP)
   - Prevent brute force attacks

5. **Password Reset**:
   - Email-based password reset flow
   - Requires email service integration

6. **Email Verification**:
   - Send verification email on registration
   - Require verification before login

7. **Two-Factor Authentication (2FA)**:
   - TOTP-based 2FA (Google Authenticator)
   - SMS-based 2FA

---

## 12. References

- JWT Specification: RFC 7519 (https://tools.ietf.org/html/rfc7519)
- JWT Best Practices: RFC 8725 (https://tools.ietf.org/html/rfc8725)
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- Passlib Documentation: https://passlib.readthedocs.io/
- Python-JOSE Documentation: https://python-jose.readthedocs.io/
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

---

**Plan Author**: AI Agent
**Review Status**: Pending User Approval
**Next Step**: Proceed to task breakdown (`/sp.tasks`) after plan approval
