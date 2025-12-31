"""
Database Session Management
Configures SQLModel engine and provides session dependency.

Spec Reference: specs/database/schema.md (Connection Management)
"""

from sqlmodel import Session, create_engine
from typing import Generator
from app.config import settings


# Create SQLModel engine with connection pooling
# Pool size: 10 connections (Neon free tier limit)
# Max overflow: 0 (no additional connections beyond pool)
# Pool timeout: 30 seconds
# Pool recycle: 3600 seconds (1 hour)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=3600,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Yields a SQLModel Session that automatically commits on success
    and rolls back on exception.

    Yields:
        Session: SQLModel database session

    Example:
        @app.get("/api/users")
        def get_users(session: Session = Depends(get_session)):
            users = session.exec(select(User)).all()
            return users
    """
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """
    Initialize database tables.

    Creates all tables defined in SQLModel models.
    Note: In production, use Alembic migrations instead.

    This is only for development/testing purposes.
    """
    from sqlmodel import SQLModel
    from app.models.user import User  # Import all models here
    from app.models.task import Task

    SQLModel.metadata.create_all(engine)
