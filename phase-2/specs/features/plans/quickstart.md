# Quickstart: Task CRUD Implementation Guide

**Feature**: F002 - Task CRUD Operations
**Date**: 2025-12-31
**Audience**: Developers implementing this feature

## Overview

This guide provides step-by-step instructions for implementing Task CRUD operations. Follow these steps in order for best results.

## Prerequisites

✅ **Required** (from F001):
- Backend: FastAPI project initialized with JWT authentication
- Frontend: Next.js 16+ project with Better Auth
- Database: PostgreSQL connection configured
- Auth: `get_current_user_id()` dependency available

## Implementation Sequence

### Phase 1: Backend Database Model (Estimated: 1 hour)

#### Step 1.1: Create Task Model

**File**: `backend/app/models/task.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    """Task status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    """Task model with user isolation."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
```

#### Step 1.2: Create Database Migration

**Option A: Alembic** (recommended for production):
```bash
cd backend
alembic revision -m "create tasks table"
# Edit migration file with SQL from data-model.md
alembic upgrade head
```

**Option B: SQLModel auto-create** (development only):
```python
# backend/app/main.py
from app.models.task import Task  # Import to register model

@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)
```

#### Step 1.3: Update models/__init__.py

```python
# backend/app/models/__init__.py
from .user import User
from .task import Task, TaskStatus

__all__ = ["User", "Task", "TaskStatus"]
```

**Test**: Run backend and verify `tasks` table exists in database.

---

### Phase 2: Backend Pydantic Schemas (Estimated: 30 min)

#### Step 2.1: Create Task Schemas

**File**: `backend/app/schemas/task.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus

class TaskCreateRequest(BaseModel):
    """Create task request."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)

class TaskUpdateRequest(BaseModel):
    """Update task request (partial)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    """Task response schema."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """Task list response."""
    tasks: list[TaskResponse]
```

#### Step 2.2: Update schemas/__init__.py

```python
# backend/app/schemas/__init__.py
from .auth import *
from .task import *
```

**Test**: Import schemas in Python REPL, verify no errors.

---

### Phase 3: Backend API Endpoints (Estimated: 2-3 hours)

#### Step 3.1: Create Task Router

**File**: `backend/app/api/v1/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.db.session import get_session
from app.auth.dependencies import get_current_user_id
from app.models.task import Task
from app.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# POST /api/tasks - Create task
@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    request: TaskCreateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Create new task for authenticated user."""
    task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        user_id=user_id  # Auto-assign from JWT
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskResponse.from_orm(task)

# GET /api/tasks - List tasks
@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """List all tasks for authenticated user."""
    tasks = session.exec(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()
    return TaskListResponse(tasks=[TaskResponse.from_orm(t) for t in tasks])

# GET /api/tasks/{task_id} - Get task
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Get task by ID (only if owned by user)."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse.from_orm(task)

# PUT /api/tasks/{task_id} - Update task
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Update task (only if owned by user)."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only provided fields
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

    return TaskResponse.from_orm(task)

# DELETE /api/tasks/{task_id} - Delete task
@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete task (only if owned by user)."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return None  # 204 No Content
```

#### Step 3.2: Register Router in Main App

```python
# backend/app/main.py
from app.api.v1 import tasks

app.include_router(tasks.router)
```

**Test**: Start backend, visit http://localhost:8000/docs, verify 5 task endpoints appear.

---

### Phase 4: Backend Testing (Estimated: 2 hours)

#### Step 4.1: Create Task Tests

**File**: `backend/tests/test_tasks.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.user import User
from app.models.task import Task, TaskStatus
from app.auth.password import hash_password

class TestTaskCRUD:
    """Test task CRUD operations."""

    def test_create_task_success(self, client: TestClient, session: Session):
        # Register and login
        user = User(email="test@example.com", hashed_password=hash_password("pass123"))
        session.add(user)
        session.commit()

        login_response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "pass123"})
        token = login_response.json()["access_token"]

        # Create task
        response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Test Task", "description": "Description", "status": "pending"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["user_id"] == user.id
        assert "id" in data

    def test_list_tasks_user_isolation(self, client: TestClient, session: Session):
        # Create two users
        user1 = User(email="user1@example.com", hashed_password=hash_password("pass1"))
        user2 = User(email="user2@example.com", hashed_password=hash_password("pass2"))
        session.add(user1)
        session.add(user2)
        session.commit()

        # User 1 creates tasks
        task1 = Task(title="Task 1", user_id=user1.id)
        task2 = Task(title="Task 2", user_id=user1.id)
        session.add(task1)
        session.add(task2)
        session.commit()

        # User 2 lists tasks
        login_response = client.post("/api/auth/login", json={"email": "user2@example.com", "password": "pass2"})
        token2 = login_response.json()["access_token"]

        response = client.get("/api/tasks", headers={"Authorization": f"Bearer {token2}"})

        assert response.status_code == 200
        data = response.json()
        # User 2 should see NO tasks (isolation)
        assert len(data["tasks"]) == 0

    def test_get_task_cross_user_returns_404(self, client: TestClient, session: Session):
        # Create two users
        user1 = User(email="user1@example.com", hashed_password=hash_password("pass1"))
        user2 = User(email="user2@example.com", hashed_password=hash_password("pass2"))
        session.add(user1)
        session.add(user2)
        session.commit()

        # User 1 creates task
        task = Task(title="User 1 Task", user_id=user1.id)
        session.add(task)
        session.commit()

        # User 2 attempts to get User 1's task
        login_response = client.post("/api/auth/login", json={"email": "user2@example.com", "password": "pass2"})
        token2 = login_response.json()["access_token"]

        response = client.get(f"/api/tasks/{task.id}", headers={"Authorization": f"Bearer {token2}"})

        # Should return 404 (not 200, not 403)
        assert response.status_code == 404

    # Add more tests for update, delete, validation...
```

**Run Tests**:
```bash
cd backend
pytest tests/test_tasks.py -v
```

---

### Phase 5: Frontend Types (Estimated: 15 min)

#### Step 5.1: Create Task Types

**File**: `frontend/types/task.ts`

```typescript
export type TaskStatus = "pending" | "in_progress" | "completed";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string | null;
  status?: TaskStatus;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string | null;
  status?: TaskStatus;
}

export interface TaskListResponse {
  tasks: Task[];
}
```

---

### Phase 6: Frontend API Client (Estimated: 30 min)

#### Step 6.1: Create Task API Functions

**File**: `frontend/lib/task-api.ts`

```typescript
import { apiGet, apiPost, apiPut, apiDelete } from "./api";
import type { Task, TaskCreateRequest, TaskUpdateRequest, TaskListResponse } from "@/types/task";

export async function getTasks(): Promise<Task[]> {
  const response = await apiGet("/api/tasks");
  const data: TaskListResponse = await response.json();
  return data.tasks;
}

export async function getTask(id: number): Promise<Task> {
  const response = await apiGet(`/api/tasks/${id}`);
  return await response.json();
}

export async function createTask(data: TaskCreateRequest): Promise<Task> {
  const response = await apiPost("/api/tasks", data);
  return await response.json();
}

export async function updateTask(id: number, data: TaskUpdateRequest): Promise<Task> {
  const response = await apiPut(`/api/tasks/${id}`, data);
  return await response.json();
}

export async function deleteTask(id: number): Promise<void> {
  await apiDelete(`/api/tasks/${id}`);
}
```

---

### Phase 7: Frontend Components (Estimated: 3-4 hours)

#### Step 7.1: Status Badge Component

**File**: `frontend/components/tasks/StatusBadge.tsx`

```typescript
import type { TaskStatus } from "@/types/task";

const statusStyles = {
  pending: "bg-gray-100 text-gray-800",
  in_progress: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
};

export function StatusBadge({ status }: { status: TaskStatus }) {
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[status]}`}>
      {status.replace("_", " ")}
    </span>
  );
}
```

#### Step 7.2: Task List Component

**File**: `frontend/components/tasks/TaskList.tsx`

```typescript
"use client";

import Link from "next/link";
import { StatusBadge } from "./StatusBadge";
import type { Task } from "@/types/task";

export function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Create your first task!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <Link key={task.id} href={`/tasks/${task.id}`}>
          <div className="bg-white p-4 rounded-lg shadow hover:shadow-md transition">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900">{task.title}</h3>
                {task.description && (
                  <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                )}
              </div>
              <StatusBadge status={task.status} />
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
```

#### Step 7.3: Update Dashboard Page

**File**: `frontend/app/dashboard/page.tsx`

```typescript
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { TaskList } from "@/components/tasks/TaskList";
import { getTasks } from "@/lib/task-api";
import type { Task } from "@/types/task";

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTasks() {
      try {
        const data = await getTasks();
        setTasks(data);
      } catch (error) {
        console.error("Failed to load tasks:", error);
      } finally {
        setLoading(false);
      }
    }
    loadTasks();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="px-4 py-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">My Tasks</h2>
        <Link
          href="/tasks/new"
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          New Task
        </Link>
      </div>
      <TaskList tasks={tasks} />
    </div>
  );
}
```

#### Step 7.4: Create Task Form Page

**File**: `frontend/app/tasks/new/page.tsx`

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createTask } from "@/lib/task-api";
import type { TaskCreateRequest, TaskStatus } from "@/types/task";

export default function NewTaskPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<TaskCreateRequest>({
    title: "",
    description: "",
    status: "pending",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await createTask(formData);
      router.push("/dashboard");
    } catch (err) {
      setError("Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Create New Task</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && <div className="bg-red-50 text-red-600 p-3 rounded">{error}</div>}

        <div>
          <label className="block text-sm font-medium text-gray-700">Title *</label>
          <input
            type="text"
            required
            maxLength={200}
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            rows={4}
            maxLength={2000}
            value={formData.description || ""}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Status</label>
          <select
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value as TaskStatus })}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? "Creating..." : "Create Task"}
          </button>
          <button
            type="button"
            onClick={() => router.push("/dashboard")}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
```

#### Step 7.5: Edit Task Form Page

**File**: `frontend/app/tasks/[id]/page.tsx`

Similar to new task page but with `getTask()` to load data and `updateTask()` + `deleteTask()` actions.

---

## Testing Checklist

### Backend Tests
- [ ] Create task returns 201 with task object
- [ ] List tasks filtered by user_id
- [ ] User isolation: User A cannot see User B's tasks
- [ ] Cross-user GET returns 404 (not 403)
- [ ] Cross-user UPDATE returns 404
- [ ] Cross-user DELETE returns 404
- [ ] Validation errors return 422
- [ ] Missing auth returns 401

### Frontend Tests
- [ ] Dashboard displays task list
- [ ] Create task form submits and redirects
- [ ] Edit task form loads data and updates
- [ ] Delete task removes from list
- [ ] Status badges display correctly
- [ ] Error messages display validation errors

---

## Deployment

1. **Backend**: Run migrations, restart server
2. **Frontend**: Build and deploy to Vercel
3. **Database**: Verify indexes created
4. **Monitoring**: Check for 404 errors (potential isolation issues)

---

**Quickstart Status**: Complete
**Estimated Total Time**: 10-12 hours
**Next**: Run `/sp.tasks` to create atomic task breakdown
