"""
Pytest Configuration and Fixtures
Provides test fixtures for database and API client.

Spec Reference: specs/features/plans/authentication-plan.md (Section 9.1)
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.db.session import get_session


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a test database session using SQLite in-memory database.

    Yields a fresh database session for each test.
    Automatically cleans up after test completes.

    Yields:
        Session: Test database session
    """
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Drop all tables after test
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a FastAPI test client with test database session.

    Overrides the get_session dependency to use test database.

    Args:
        session: Test database session

    Yields:
        TestClient: FastAPI test client
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
