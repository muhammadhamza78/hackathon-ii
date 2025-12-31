# Task Management API - Backend

FastAPI backend with JWT authentication for the Task Management System.

## Features

- ✅ User registration with email/password
- ✅ User login with JWT token issuance
- ✅ JWT-based authentication middleware
- ✅ Password hashing with bcrypt (cost factor 12)
- ✅ SQLModel ORM with PostgreSQL
- ✅ Comprehensive test suite
- ✅ User data isolation enforcement

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel 0.0.14+
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Testing**: pytest

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   │   └── auth.py      # Authentication endpoints
│   ├── auth/            # Authentication utilities
│   │   ├── dependencies.py  # get_current_user_id
│   │   ├── jwt.py       # JWT token creation/validation
│   │   └── password.py  # Password hashing
│   ├── db/              # Database configuration
│   │   └── session.py   # Session management
│   ├── models/          # SQLModel data models
│   │   └── user.py      # User model
│   ├── schemas/         # Pydantic request/response schemas
│   │   └── auth.py      # Auth schemas
│   ├── config.py        # Configuration management
│   └── main.py          # FastAPI application
├── tests/               # Test suite
│   ├── conftest.py      # Pytest fixtures
│   └── test_auth.py     # Authentication tests
└── requirements.txt     # Python dependencies
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and configure the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech/dbname?sslmode=require

# JWT Configuration
# Generate a secure secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET_KEY=your-generated-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Application Configuration
ENV=development
DEBUG=True
```

**Important**:
- Replace `DATABASE_URL` with your Neon PostgreSQL connection string
- Generate a new `JWT_SECRET_KEY` using the command above
- NEVER commit `.env` file to version control

### 4. Initialize Database

The application will automatically create tables on startup in development mode.

For production, use Alembic migrations:

```bash
# Initialize Alembic (one-time setup)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head
```

### 5. Run Development Server

```bash
# Start server
python -m uvicorn app.main:app --reload

# Or use the main.py entry point
python app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (201)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-30T10:00:00Z"
}
```

#### Login User

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### Health Check

```http
GET /health
```

**Response (200)**:
```json
{
  "status": "ok",
  "database": "connected"
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestRegistration::test_register_success
```

## Security Features

### Password Security
- ✅ Bcrypt hashing with cost factor 12 (~250-500ms)
- ✅ Automatic salt generation
- ✅ Constant-time comparison (prevents timing attacks)

### JWT Security
- ✅ HS256 algorithm with 256-bit secret key
- ✅ 24-hour token expiry (configurable)
- ✅ User ID in `sub` claim (as string per JWT spec)
- ✅ Signature verification on every protected request

### User Isolation
- ✅ All queries filtered by `user_id` from JWT
- ✅ Cross-user access returns 404 (not 403)
- ✅ User enumeration prevention

## Development

### Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and testable

### Adding Protected Endpoints

Use the `get_current_user_id` dependency:

```python
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.get("/api/tasks")
async def list_tasks(user_id: int = Depends(get_current_user_id)):
    # user_id is guaranteed to be valid and authenticated
    # Always filter queries by user_id
    tasks = get_user_tasks(user_id)
    return {"tasks": tasks}
```

**CRITICAL**: Every query on user data MUST filter by `user_id`:

```python
# ✅ CORRECT
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# ❌ WRONG - Security vulnerability!
tasks = session.exec(select(Task)).all()
```

## Troubleshooting

### Database Connection Issues

- Verify `DATABASE_URL` is correct
- Check Neon database is accessible
- Ensure SSL mode is required (`?sslmode=require`)

### JWT Token Issues

- Verify `JWT_SECRET_KEY` is set and >= 32 characters
- Check token hasn't expired (24 hours default)
- Ensure Authorization header format: `Bearer <token>`

### Import Errors

- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.11+ required)

## Next Steps

- [ ] Implement task CRUD endpoints
- [ ] Add database migrations with Alembic
- [ ] Implement user isolation tests for task endpoints
- [ ] Add refresh token support
- [ ] Implement rate limiting

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- Specifications: `../specs/features/authentication.md`
- API Spec: `../specs/api/rest-endpoints.md`
