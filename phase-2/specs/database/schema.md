# Database Schema Specification

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Status:** Specification
**Database**: Neon Serverless PostgreSQL

## Overview

Complete database schema definition for the Task Management System. Uses PostgreSQL with SQLModel ORM for type-safe database operations.

## Database Configuration

**Provider**: Neon Serverless PostgreSQL
**Connection**: Pooled connection (max 10 connections)
**Timezone**: UTC (all timestamps in UTC)
**Character Set**: UTF-8

## Tables

### users

**Purpose**: Store user account information and credentials

**Table Definition**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| email | VARCHAR(255) | NOT NULL, UNIQUE | User email (login identifier) |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt/Argon2 hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `email` (case-insensitive via LOWER function)

**SQL Definition**:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_users_email_lower ON users (LOWER(email));
```

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Business Rules**:
- Email MUST be unique (case-insensitive)
- Email MUST be valid email format
- hashed_password MUST never contain plaintext password
- created_at is immutable (set once on insert)
- updated_at is auto-updated on every update

**Sample Data**:
```sql
INSERT INTO users (email, hashed_password, created_at, updated_at) VALUES
('user@example.com', '$2b$12$hashedpassword...', '2025-12-30 10:00:00', '2025-12-30 10:00:00');
```

---

### tasks

**Purpose**: Store user tasks with title, description, and status

**Table Definition**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULL | Task description (optional) |
| status | VARCHAR(20) | NOT NULL, CHECK IN (...) | Task status enum |
| user_id | INTEGER | NOT NULL, FOREIGN KEY | Owner of the task |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update time |

**Status Enum Values**:
- `pending`
- `in_progress`
- `completed`

**Foreign Keys**:
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Indexes**:
- PRIMARY KEY: `id`
- INDEX: `user_id` (for filtering tasks by user)
- INDEX: `(user_id, created_at DESC)` (for listing user's tasks ordered by creation)

**SQL Definition**:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed')),
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks (user_id);
CREATE INDEX idx_tasks_user_created ON tasks (user_id, created_at DESC);
```

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Business Rules**:
- title MUST NOT be empty
- status MUST be one of: pending, in_progress, completed
- user_id MUST reference valid user
- created_at is immutable (set once on insert)
- updated_at is auto-updated on every update
- When user is deleted, all their tasks are CASCADE deleted

**Sample Data**:
```sql
INSERT INTO tasks (title, description, status, user_id, created_at, updated_at) VALUES
('Buy groceries', 'Milk, eggs, bread', 'pending', 1, '2025-12-30 10:00:00', '2025-12-30 10:00:00'),
('Write report', NULL, 'in_progress', 1, '2025-12-30 11:00:00', '2025-12-30 11:30:00'),
('Submit assignment', 'Due Friday', 'completed', 2, '2025-12-30 09:00:00', '2025-12-30 14:00:00');
```

---

## Relationships

### users → tasks (One-to-Many)

**Relationship**: One user can have many tasks

**Foreign Key**: `tasks.user_id` → `users.id`

**Cascade Behavior**: ON DELETE CASCADE (when user deleted, all their tasks are deleted)

**SQLModel Relationship** (optional, for convenience):
```python
from sqlmodel import Relationship
from typing import List

class User(SQLModel, table=True):
    # ... other fields ...
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    # ... other fields ...
    user: "User" = Relationship(back_populates="tasks")
```

---

## Database Migrations

**Migration Tool**: Alembic (SQLModel integration)

**Migration Process**:
1. Modify SQLModel models in code
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review generated SQL
4. Apply migration: `alembic upgrade head`

**Migration Naming Convention**:
- Format: `YYYYMMDD_HHMM_description`
- Example: `20251230_1000_create_users_table`

**Initial Migration** (create tables):
```bash
alembic revision --autogenerate -m "create users and tasks tables"
alembic upgrade head
```

---

## Indexes

### Performance Optimization

**users.email (UNIQUE)**:
- Purpose: Fast lookup during login
- Type: B-tree index (case-insensitive via LOWER)
- Cardinality: High (unique per user)

**tasks.user_id**:
- Purpose: Fast filtering of tasks by user
- Type: B-tree index
- Cardinality: Medium (many tasks per user)
- Usage: `WHERE user_id = ?`

**tasks.(user_id, created_at DESC)**:
- Purpose: Fast listing of user's tasks ordered by creation
- Type: Composite B-tree index
- Usage: `WHERE user_id = ? ORDER BY created_at DESC`

**Index Sizing Estimate**:
- users table: ~1KB per 100 users
- tasks table: ~5KB per 1000 tasks
- Total: Negligible for MVP

---

## Data Integrity

### Constraints

**users.email UNIQUE**:
- Prevents duplicate accounts
- Case-insensitive enforcement via `LOWER(email)` index

**tasks.status CHECK**:
- Ensures status is always valid enum value
- Prevents invalid states

**tasks.user_id FOREIGN KEY**:
- Ensures referential integrity
- Prevents orphaned tasks
- CASCADE delete maintains consistency

### Triggers

**updated_at Auto-Update** (PostgreSQL trigger):
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Alternative** (Application-level in SQLModel):
```python
from sqlmodel import Session

def update_task(session: Session, task_id: int, updates: dict):
    task = session.get(Task, task_id)
    for key, value in updates.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()  # Explicitly update
    session.add(task)
    session.commit()
```

---

## Connection Management

### Connection Pooling

**Configuration**:
- Pool size: 10 connections (Neon free tier limit)
- Max overflow: 0 (no additional connections)
- Pool timeout: 30 seconds
- Pool recycle: 3600 seconds (1 hour)

**SQLModel/SQLAlchemy Engine**:
```python
from sqlmodel import create_engine

DATABASE_URL = "postgresql://user:password@neon-host/dbname"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False  # Set to True for SQL logging in dev
)
```

### Session Management

**Session Pattern** (FastAPI dependency):
```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

**Usage in Endpoints**:
```python
from fastapi import Depends

@app.get("/api/tasks")
async def list_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"tasks": tasks}
```

---

## Security

### User Isolation Enforcement

**Query Pattern** (MUST be followed):
```python
# CORRECT: Filter by user_id from JWT
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# INCORRECT: No user_id filter (security vulnerability!)
tasks = session.exec(select(Task)).all()  # ❌ DO NOT DO THIS
```

**Acceptance Criteria**:
- ALL queries on tasks table MUST include `WHERE user_id = ?`
- user_id MUST come from validated JWT token
- user_id from request body/params MUST be ignored

### SQL Injection Prevention

**Protection**: SQLModel/SQLAlchemy uses parameterized queries automatically.

**Safe**:
```python
# Parameterized query (safe)
session.exec(select(Task).where(Task.title == user_input))
```

**Unsafe** (NEVER do this):
```python
# String concatenation (SQL injection vulnerability!)
session.exec(f"SELECT * FROM tasks WHERE title = '{user_input}'")  # ❌ NEVER
```

---

## Backup and Recovery

### Backup Strategy

**Neon Automatic Backups**:
- Point-in-time recovery (PITR) available
- 7-day retention on free tier
- Daily snapshots

**Manual Backup** (pg_dump):
```bash
pg_dump -h neon-host -U user -d dbname > backup.sql
```

**Restore**:
```bash
psql -h neon-host -U user -d dbname < backup.sql
```

### Disaster Recovery

**Recovery Time Objective (RTO)**: < 1 hour
**Recovery Point Objective (RPO)**: < 24 hours (daily backups)

**Steps**:
1. Restore from Neon snapshot or manual backup
2. Apply any recent migrations
3. Verify data integrity
4. Resume service

---

## Data Retention

### Active Data

**users**: Retained indefinitely while account is active

**tasks**: Retained indefinitely (no auto-deletion)

### Deleted Data

**Soft Delete** (future enhancement):
- Add `deleted_at` timestamp column
- Modify queries to exclude deleted records
- Retention: 30 days (users), 7 days (tasks)

**Hard Delete** (current):
- Immediate permanent deletion
- Cascade: User deletion → all tasks deleted

---

## Performance Benchmarks

### Query Performance Targets

| Query | Target (p95) | Notes |
|-------|--------------|-------|
| Get user by email | < 5ms | Indexed lookup |
| Create task | < 20ms | Single INSERT |
| List tasks (per user) | < 50ms | Indexed query, 100 tasks |
| Get task by ID | < 5ms | Primary key lookup |
| Update task | < 20ms | Single UPDATE |
| Delete task | < 10ms | Single DELETE |

### Scaling Considerations

**Vertical Scaling** (Neon):
- Increase vCPU and RAM for database
- Neon auto-scales within tier limits

**Query Optimization**:
- Use `EXPLAIN ANALYZE` to identify slow queries
- Add indexes for frequently queried columns
- Avoid N+1 queries (use eager loading if needed)

**Future Optimizations**:
- Read replicas for scaling read operations
- Caching layer (Redis) for frequently accessed data
- Pagination for large task lists

---

## Environment Configuration

### Database Connection

**Environment Variables**:
```env
DATABASE_URL=postgresql://user:password@neon-host/dbname
DATABASE_POOL_SIZE=10
DATABASE_ECHO=false  # Set to true for SQL logging
```

**Connection String Format**:
```
postgresql://[user]:[password]@[host]:[port]/[database]?[options]
```

**Neon Connection String Example**:
```
postgresql://user:pass@ep-cool-name-123456.us-east-2.aws.neon.tech/dbname?sslmode=require
```

---

## Testing

### Test Database

**Separate Database**: Use different database for testing

**Setup**:
```python
from sqlmodel import create_engine, SQLModel

TEST_DATABASE_URL = "postgresql://user:pass@localhost/test_db"
test_engine = create_engine(TEST_DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(test_engine)

# Run tests

# Drop all tables
SQLModel.metadata.drop_all(test_engine)
```

### Fixtures

**pytest fixture for database session**:
```python
import pytest
from sqlmodel import Session, create_engine, SQLModel

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")  # In-memory for speed
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
```

### Test Data

**Factory pattern for test data**:
```python
def create_test_user(session: Session, email: str = "test@example.com"):
    user = User(email=email, hashed_password="hashed...")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_test_task(session: Session, user_id: int, title: str = "Test Task"):
    task = Task(title=title, user_id=user_id, status=TaskStatus.PENDING)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

## Acceptance Criteria

**Database schema is DONE when**:
- [ ] All tables created with correct columns and types
- [ ] All constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK) defined
- [ ] All indexes created for performance
- [ ] Migrations working (create, upgrade, downgrade)
- [ ] Connection pooling configured
- [ ] updated_at triggers or application logic implemented
- [ ] User isolation queries tested and verified
- [ ] Sample data inserted successfully
- [ ] Database documentation complete

---

## References

- See: `specs/features/authentication.md` (User model requirements)
- See: `specs/features/task-crud.md` (Task model requirements)
- See: `specs/architecture.md` (Data management section)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Neon Documentation](https://neon.tech/docs)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
