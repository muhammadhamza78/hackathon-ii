"""
FastAPI Application Entry Point
Main application configuration and startup.

Spec Reference: specs/architecture.md (Backend section)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings


# Create FastAPI application
app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)


# Configure CORS for frontend access
# Allow Next.js frontend to access API
# Update allowed_origins after deploying frontend to Vercel
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://127.0.0.1:3000",
    # Add your Vercel deployment URLs here after deployment:
    # "https://your-app.vercel.app",
    # "https://your-app-*.vercel.app",  # Preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# Include routers
app.include_router(auth.router)
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.on_event("startup")
async def startup_event():
    """
    Application startup event.

    Initialize database tables (development only).
    In production, use Alembic migrations instead.
    """
    if settings.DEBUG:
        # Only auto-create tables in development
        init_db()


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.

    Returns API information and available endpoints.
    """
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns service status and database connectivity.
    Spec: specs/api/rest-endpoints.md (Health Check Endpoint)
    """
    from app.db.session import engine
    from sqlmodel import text

    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception:
        return {
            "status": "degraded",
            "database": "disconnected"
        }


if __name__ == "__main__":
    import uvicorn

    # Run development server
    # For production, use: uvicorn app.main:app --host 0.0.0.0 --port 8000
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
