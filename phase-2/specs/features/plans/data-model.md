# Data Model: Task CRUD

**Feature**: F002 - Task CRUD Operations
**Date**: 2025-12-31
**Status**: Phase 1 - Database Design

## Overview

This document defines the database schema, SQLModel definitions, and data relationships for the Task CRUD feature. All models follow Constitution principles for type safety and user data isolation.

## Entities

### Task

**Purpose**: Represents a user's task with title, description, status, and ownership.

**Attributes**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| title | String(200) | NOT NULL | Task title (required) |
| description | Text | NULL | Task description (optional) |
| status | Enum | NOT NULL, CHECK | Task status (pending/in_progress/completed) |
| user_id | Integer | NOT NULL, FOREIGN KEY | Owner of the task |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Task creation timestamp |
| updated_at | DateTime | NOT NULL, DEFAULT NOW | Last modification timestamp |

**Relationships**:
- **Belongs To**: User (many-to-one)
  - Foreign Key: `task.user_id` → `user.id`
  - Cascade: ON DELETE CASCADE (when user deleted, all their tasks deleted)

**Indexes**:
1. PRIMARY KEY: `id`
2. INDEX: `user_id` (for filtering tasks by user)
3. COMPOSITE INDEX: `(user_id, created_at DESC)` (for listing user's tasks sorted by date)

**Validation Rules**:
- `title`: Required, non-empty, max 200 characters
- `description`: Optional, max 2000 characters, can be NULL
- `status`: Must be one of: "pending", "in_progress", "completed"
- `user_id`: Must reference existing user.id
- `created_at`: Immutable after creation
- `updated_at`: Auto-updated on every modification

**State Transitions**:
```
pending → in_progress → completed
   ↓         ↓              ↓
   └─────────┴──────────────┘
   (Any status can transition to any other status)
```

---

## Database Schema

### PostgreSQL Definition

```sql
-- Task table
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

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks (user_id);
CREATE INDEX idx_tasks_user_created ON tasks (user_id, created_at DESC);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

### SQLModel Definition (Python)

```python
# backend/app/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enum with string values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    """
    Task model representing a user's todo item.

    User Isolation: All queries MUST filter by user_id.
    Constitution: Principle III (NON-NEGOTIABLE)
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True  # Store enum as string in database
```

---

## Pydantic Schemas (Request/Response)

### Request Schemas

```python
# backend/app/schemas/task.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus

class TaskCreateRequest(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "pending"
            }
        }

class TaskUpdateRequest(BaseModel):
    """Request schema for updating an existing task (partial updates)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "status": "in_progress"
            }
        }
```

### Response Schemas

```python
class TaskResponse(BaseModel):
    """Response schema for a single task."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM mode
        json_schema_extra = {
            "example": {
                "id": 123,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "pending",
                "user_id": 456,
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }

class TaskListResponse(BaseModel):
    """Response schema for task list."""
    tasks: list[TaskResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 123,
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "status": "pending",
                        "user_id": 456,
                        "created_at": "2025-12-30T10:00:00Z",
                        "updated_at": "2025-12-30T10:00:00Z"
                    },
                    {
                        "id": 124,
                        "title": "Write report",
                        "description": None,
                        "status": "in_progress",
                        "user_id": 456,
                        "created_at": "2025-12-30T11:00:00Z",
                        "updated_at": "2025-12-30T11:30:00Z"
                    }
                ]
            }
        }
```

---

## TypeScript Types (Frontend)

```typescript
// frontend/types/task.ts

/**
 * Task status enum matching backend TaskStatus.
 */
export type TaskStatus = "pending" | "in_progress" | "completed";

/**
 * Task model representing a user's todo item.
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  user_id: number;
  created_at: string;  // ISO 8601 datetime string
  updated_at: string;  // ISO 8601 datetime string
}

/**
 * Request payload for creating a new task.
 */
export interface TaskCreateRequest {
  title: string;
  description?: string | null;
  status?: TaskStatus;
}

/**
 * Request payload for updating an existing task.
 * All fields are optional (partial update).
 */
export interface TaskUpdateRequest {
  title?: string;
  description?: string | null;
  status?: TaskStatus;
}

/**
 * Response payload for task list endpoint.
 */
export interface TaskListResponse {
  tasks: Task[];
}

/**
 * Error response from API.
 */
export interface TaskErrorResponse {
  detail: string | ValidationError[];
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}
```

---

## Data Relationships

### User → Tasks (One-to-Many)

**Relationship**: One user can have many tasks (0..*)

```
users (1) ─────< tasks (many)
  │                 │
  └─ id             └─ user_id (FK)
```

**Cascade Behavior**:
- ON DELETE CASCADE: When user is deleted, all their tasks are automatically deleted
- ON UPDATE CASCADE: Not needed (user.id should never change)

**Querying**:
```python
# Get all tasks for a user
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# Get task count for a user
count = session.exec(
    select(func.count(Task.id)).where(Task.user_id == user_id)
).one()
```

---

## Sample Data

```sql
-- Sample users (from F001)
INSERT INTO users (id, email, hashed_password, created_at, updated_at) VALUES
(1, 'alice@example.com', '$2b$12$...', '2025-12-30 09:00:00', '2025-12-30 09:00:00'),
(2, 'bob@example.com', '$2b$12$...', '2025-12-30 09:30:00', '2025-12-30 09:30:00');

-- Sample tasks
INSERT INTO tasks (id, title, description, status, user_id, created_at, updated_at) VALUES
(1, 'Buy groceries', 'Milk, eggs, bread', 'pending', 1, '2025-12-30 10:00:00', '2025-12-30 10:00:00'),
(2, 'Write report', NULL, 'in_progress', 1, '2025-12-30 11:00:00', '2025-12-30 11:30:00'),
(3, 'Submit assignment', 'Due Friday', 'completed', 2, '2025-12-30 09:00:00', '2025-12-30 14:00:00'),
(4, 'Call dentist', 'Schedule checkup', 'pending', 1, '2025-12-30 12:00:00', '2025-12-30 12:00:00');
```

**Expected Queries**:
- Alice (user_id=1) lists tasks → Returns tasks 1, 2, 4 (3 tasks)
- Bob (user_id=2) lists tasks → Returns task 3 (1 task)
- Alice attempts to get task 3 → Returns 404 (belongs to Bob)

---

## Migration Plan

### Creating the Task Table

**Option 1: Alembic Migration (Recommended)**
```python
# migrations/versions/002_create_tasks_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed')", name='check_task_status')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_user_created', 'tasks', ['user_id', 'created_at DESC'])

def downgrade():
    op.drop_table('tasks')
```

**Option 2: SQLModel auto-creation (Development Only)**
```python
# backend/app/main.py
from sqlmodel import SQLModel, create_engine

# Create tables on startup (development only)
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

---

## Data Integrity Rules

1. **Title is Required**: Cannot be NULL or empty string
2. **Status Must Be Valid**: One of "pending", "in_progress", or "completed"
3. **User Must Exist**: user_id must reference valid users.id (enforced by FK)
4. **created_at is Immutable**: Never update this field
5. **updated_at is Auto-Updated**: Trigger updates on every UPDATE
6. **Cascade Delete**: When user deleted, all their tasks deleted

---

## Performance Considerations

### Indexes

1. **Primary Key (id)**: Clustered index, fast single-task lookups
2. **user_id Index**: Fast filtering by user (covers WHERE user_id = ?)
3. **Composite Index (user_id, created_at DESC)**: Optimizes task list queries

### Query Performance

**Fast Query** (uses composite index):
```sql
SELECT * FROM tasks
WHERE user_id = 1
ORDER BY created_at DESC;
```

**Slow Query** (full table scan):
```sql
SELECT * FROM tasks
WHERE title LIKE '%grocery%';  -- Not indexed, avoid in MVP
```

### Expected Load

- Users: 100-1000
- Tasks per user: 10-100
- Total tasks: ~10,000
- List query frequency: High (every dashboard load)
- Create/Update/Delete: Medium (user actions)

**Optimization**: Composite index handles expected load. Pagination not needed for MVP.

---

## Security Considerations

### User Isolation Enforcement

**CRITICAL**: Every task query MUST include `WHERE user_id = {authenticated_user_id}`

```python
# ✅ CORRECT - Always filter by user_id
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == user_id)
).first()

# ❌ WRONG - Security vulnerability!
task = session.exec(
    select(Task).where(Task.id == task_id)
).first()
```

### Preventing User Enumeration

**Return 404 for cross-user access** (not 403):
```python
# User B attempts to access User A's task
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
    # Same response whether task doesn't exist or belongs to different user
```

---

## Testing Strategy

### Unit Tests

```python
def test_task_model_validation():
    # Valid task
    task = Task(title="Test", user_id=1)
    assert task.status == TaskStatus.PENDING  # Default status

    # Invalid title (too long)
    with pytest.raises(ValidationError):
        Task(title="x" * 201, user_id=1)

    # Invalid status
    with pytest.raises(ValidationError):
        Task(title="Test", status="invalid", user_id=1)
```

### User Isolation Tests

```python
def test_user_cannot_see_other_user_tasks():
    # User 1 creates task
    task1 = create_task(user_id=1, title="Task 1")

    # User 2 lists tasks
    tasks = list_tasks(user_id=2)

    # User 1's task should NOT appear in User 2's list
    assert task1.id not in [t.id for t in tasks]
```

---

**Data Model Status**: Complete
**Author**: Claude Sonnet 4.5
**Date**: 2025-12-31
