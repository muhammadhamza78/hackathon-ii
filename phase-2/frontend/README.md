# Task Management System - Frontend

Next.js 16+ frontend with JWT authentication for the Task Management System.

## Features

- ✅ User registration with email/password
- ✅ User login with JWT token
- ✅ Protected dashboard routes
- ✅ Automatic token expiry handling
- ✅ JWT token attached to all API requests
- ✅ Better Auth integration (session management)
- ✅ Responsive UI with TailwindCSS

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Authentication**: Better Auth + JWT
- **Styling**: TailwindCSS
- **API Client**: Custom fetch wrapper with auto token injection

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Login page (/)
│   ├── register/
│   │   └── page.tsx          # Registration page
│   ├── dashboard/
│   │   ├── layout.tsx        # Protected dashboard layout
│   │   └── page.tsx          # Dashboard page (placeholder)
│   └── api/auth/[...all]/
│       └── route.ts          # Better Auth API route
├── lib/
│   ├── auth.ts               # Better Auth configuration
│   ├── auth-client.ts        # Better Auth React hooks
│   └── api.ts                # API client with JWT injection
├── types/
│   └── auth.ts               # TypeScript type definitions
├── .env.local                # Environment variables (git-ignored)
└── .env.local.example        # Environment variable template
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create `.env.local` file (copy from `.env.local.example`):

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-here
BETTER_AUTH_URL=http://localhost:3000
```

**Important**:
- `NEXT_PUBLIC_API_URL`: Must point to your running FastAPI backend
- `BETTER_AUTH_SECRET`: Generate with `openssl rand -base64 32`
- NEVER commit `.env.local` to version control

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at **http://localhost:3000**

## Authentication Flow

### Registration Flow

1. User navigates to `/register`
2. User submits email + password (8-128 chars)
3. Frontend sends `POST /api/auth/register` to backend
4. On success, redirects to `/` (login) with success message
5. User logs in with same credentials

### Login Flow

1. User navigates to `/` (login page)
2. User submits email + password
3. Frontend sends `POST /api/auth/login` to backend
4. Backend returns JWT token with 24-hour expiry
5. Frontend stores token in `localStorage`:
   - `jwt_token`: The JWT access token
   - `token_expiry`: Unix timestamp of expiry
   - `user_email`: User's email address
6. Redirect to `/dashboard`

### Protected Routes

All routes under `/dashboard` are protected:

1. Dashboard layout checks for JWT token in `localStorage`
2. Verifies token is not expired
3. If token missing/expired → redirect to `/` (login)
4. If valid → render dashboard content

### API Requests

Use the `apiRequest()` utility from `lib/api.ts`:

```typescript
import { apiGet, apiPost } from "@/lib/api";

// GET request (auth required)
const response = await apiGet("/api/tasks");
const tasks = await response.json();

// POST request (auth required)
const response = await apiPost("/api/tasks", {
  title: "New Task",
  description: "Task description",
  status: "pending"
});

// Request without auth
const response = await apiPost("/api/public-endpoint", data, false);
```

**Automatic Token Injection**:
- API client reads `jwt_token` from `localStorage`
- Adds `Authorization: Bearer <token>` header
- Checks token expiry before request
- Redirects to login on 401 response

## Pages

### `/` - Login Page

- Email and password inputs
- Form validation (client-side)
- Error display for invalid credentials
- Success message after registration
- Link to registration page

### `/register` - Registration Page

- Email input (validated)
- Password input (8-128 chars)
- Confirm password input
- Client-side validation
- Link back to login page

### `/dashboard` - Dashboard (Protected)

- Protected route (requires valid JWT)
- Top navigation with user email and logout button
- Placeholder for task list (Task CRUD feature)
- Auto-logout on token expiry

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | Secret for Better Auth sessions | `generated-secret-32-chars` |
| `BETTER_AUTH_URL` | Frontend URL for Better Auth | `http://localhost:3000` |

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## API Client Usage

The API client (`lib/api.ts`) provides utilities for making authenticated requests:

```typescript
// Import utilities
import { apiRequest, apiGet, apiPost, apiPut, apiDelete } from "@/lib/api";

// GET request
const response = await apiGet("/api/tasks");

// POST request with body
const response = await apiPost("/api/tasks", {
  title: "New Task",
  status: "pending"
});

// PUT request
const response = await apiPut("/api/tasks/1", {
  status: "completed"
});

// DELETE request
const response = await apiDelete("/api/tasks/1");

// Public endpoint (no auth)
const response = await apiPost("/api/public", data, false);
```

**Features**:
- Automatic `Authorization: Bearer <token>` header
- Automatic `Content-Type: application/json` header
- Token expiry check before request
- Global 401 handling (auto-logout and redirect)
- Configurable auth requirement per request

## Security Features

### JWT Token Storage

- Tokens stored in `localStorage` (persists across sessions)
- Expiry timestamp stored alongside token
- Token validated on every protected route access
- Automatic cleanup on expiry/logout

### Protected Routes

- Client-side route protection in dashboard layout
- Token presence + expiry verification
- Auto-redirect to login if unauthorized
- No flash of protected content

### Logout

- Clears all auth data from `localStorage`
- Redirects to login page
- No backend call required (stateless JWT)

## Development

### Running the App

```bash
# Development server (with hot reload)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Type Checking

TypeScript types are defined in `types/auth.ts` matching the backend API:

```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}
```

## Integration with Backend

The frontend communicates with the FastAPI backend:

### Registration

```
Frontend: POST /register (form data)
  ↓
Backend: POST /api/auth/register
  ↓
Backend: Returns user object (201)
  ↓
Frontend: Redirect to login with success message
```

### Login

```
Frontend: POST / (login form)
  ↓
Backend: POST /api/auth/login
  ↓
Backend: Returns JWT token (200)
  ↓
Frontend: Store token in localStorage
  ↓
Frontend: Redirect to /dashboard
```

### Protected API Calls

```
Frontend: API request with JWT
  ↓
API Client: Add Authorization: Bearer <token>
  ↓
Backend: Verify JWT signature
  ↓
Backend: Extract user_id from token
  ↓
Backend: Return user-specific data
```

## Troubleshooting

### "Authentication required" error

- Check if backend is running on `http://localhost:8000`
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

### Token expiry issues

- JWT tokens expire after 24 hours (backend configured)
- Expired tokens trigger auto-logout
- Re-login to get a fresh token

### CORS errors

- Backend must allow `http://localhost:3000` origin
- Check FastAPI CORS middleware configuration
- Verify `allow_credentials=True` is set

### Better Auth errors

- Verify `BETTER_AUTH_SECRET` is set (min 32 characters)
- Check `BETTER_AUTH_URL` matches your frontend URL
- Restart dev server after changing environment variables

## Next Steps

- [ ] Implement Task CRUD UI (Feature F002)
- [ ] Add loading states and skeleton screens
- [ ] Implement E2E tests with Playwright
- [ ] Add refresh token support
- [ ] Implement "Remember me" functionality

## References

- **Specs**: `../specs/features/authentication.md`
- **API Spec**: `../specs/api/rest-endpoints.md`
- **Architecture**: `../specs/architecture.md`
- **Backend README**: `../backend/README.md`
- **Next.js Docs**: https://nextjs.org/docs
- **Better Auth Docs**: https://www.better-auth.com/docs

---

**Frontend Implementation**: Complete
**Authentication Status**: ✅ Fully Functional
**Last Updated**: 2025-12-31
