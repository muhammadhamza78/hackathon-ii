# Research Findings: Task CRUD Implementation

**Feature**: F002 - Task CRUD Operations
**Date**: 2025-12-31
**Status**: Phase 0 Complete

## Overview

This document captures research findings and technical decisions for implementing Task CRUD operations with user data isolation. All unknowns from Technical Context have been resolved.

## Research Questions & Findings

### R1: How to implement TaskStatus enum across Python and TypeScript?

**Question**: What's the best practice for sharing enum values between FastAPI backend and Next.js frontend?

**Research**:
- Python: Use `str, Enum` pattern for string-based enums (Pydantic compatible)
- TypeScript: Use union types or const objects
- Sharing: Define source of truth in backend, document in API spec

**Decision**: Python Enum (str, Enum) + TypeScript union type

**Implementation**:
```python
# Backend: models/task.py
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
```

```typescript
// Frontend: types/task.ts
export type TaskStatus = "pending" | "in_progress" | "completed";
```

**Rationale**:
- Type-safe validation in both languages
- Auto-validation by Pydantic/FastAPI
- IDE autocomplete support
- String values make API responses human-readable
- OpenAPI spec auto-generates enum documentation

**Alternatives Considered**:
- Plain strings: Rejected - no compile-time validation, error-prone
- Integer flags (0, 1, 2): Rejected - not self-documenting in API responses
- Database enum type: Rejected - Neon PostgreSQL supports CHECK constraint instead

---

### R2: What's the best user isolation enforcement pattern for SQLModel?

**Question**: How to ensure every database query filters by user_id without repetition or errors?

**Research**:
- Option 1: Explicit WHERE clauses in every query
- Option 2: Row-Level Security (RLS) in PostgreSQL
- Option 3: Middleware/interceptor pattern
- Option 4: Repository pattern with base filtering

**Decision**: Explicit WHERE clause with user_id in every query

**Implementation**:
```python
# Pattern for all task queries
user_id = get_current_user_id()  # From JWT
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == user_id)
).first()
```

**Rationale**:
- **Visible**: Easy to audit in code review
- **Explicit**: No hidden magic, clear intent
- **Testable**: Can verify isolation in unit tests
- **Constitution Compliant**: Meets NON-NEGOTIABLE requirement III
- **No infrastructure dependency**: Works with any PostgreSQL version

**Alternatives Considered**:
1. **Row-Level Security (RLS)**:
   - Pros: Database-level enforcement, impossible to bypass
   - Cons: Neon Serverless may have limitations, harder to test, adds complexity
   - Rejected: Overengineering for MVP, testing complexity

2. **Middleware/Interceptor**:
   - Pros: Centralized logic, applied automatically
   - Cons: Implicit behavior, harder to debug, magic abstraction
   - Rejected: Violates Constitution preference for explicit patterns

3. **Repository Pattern**:
   - Pros: Encapsulates data access, reusable methods
   - Cons: Adds abstraction layer, more code to maintain
   - Rejected: Premature abstraction for 5 endpoints

**Testing Strategy**:
```python
# Multi-user isolation test
def test_user_cannot_access_other_user_task():
    # User A creates task
    task_a = create_task(user_id=1, title="Task A")

    # User B attempts to get Task A
    response = client.get(
        f"/api/tasks/{task_a.id}",
        headers={"Authorization": f"Bearer {token_user_b}"}
    )

    # Verify 404 (not 200, not 403)
    assert response.status_code == 404
```

---

### R3: Should we return 403 or 404 for cross-user access attempts?

**Question**: When User B tries to access User A's task, what HTTP status code should the API return?

**Research**:
- 403 Forbidden: Indicates "you don't have permission"
- 404 Not Found: Indicates "resource doesn't exist"
- Security consideration: Information leakage

**Decision**: 404 Not Found (not 403 Forbidden)

**Rationale**:
- **Prevents user enumeration**: User B cannot determine if Task ID 123 exists
- **Information hiding**: 403 reveals "task exists but you can't access it"
- **Security best practice**: Don't leak information about other users' data
- **Consistent UX**: Same response whether task doesn't exist or user doesn't own it

**Implementation**:
```python
# Get task endpoint
task = session.exec(
    select(Task).where(Task.id == task_id, Task.user_id == user_id)
).first()

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
    # Same response whether:
    # 1. Task ID doesn't exist at all
    # 2. Task exists but belongs to different user
```

**Alternatives Considered**:
- 403 Forbidden: Rejected - reveals task existence, security information leakage
- 401 Unauthorized: Rejected - misleading (user IS authenticated, just not authorized)
- 200 with empty response: Rejected - incorrect HTTP semantics

**Reference**: OWASP recommends 404 for authorization failures to prevent enumeration attacks.

---

### R4: How should tasks be ordered in the list endpoint?

**Question**: What's the default sort order for GET /api/tasks?

**Research**:
- Common patterns: created_at DESC (newest first), alphabetical, status-based
- User behavior: Most users care about recent tasks
- Performance: Indexed sorting vs application-level sorting

**Decision**: created_at DESC (newest first)

**Implementation**:
```python
# List tasks endpoint
tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
).all()
```

**Database Index**:
```sql
CREATE INDEX idx_tasks_user_created ON tasks (user_id, created_at DESC);
```

**Rationale**:
- **User expectation**: Recent activity is most relevant
- **Performance**: Composite index (user_id, created_at DESC) enables fast queries
- **Consistent**: Matches common pattern in todo apps
- **Simple**: No need for complex sorting logic

**Alternatives Considered**:
- Alphabetical (title): Rejected - less useful for temporal tasks
- Status-based (pending first): Rejected - adds complexity, user can filter manually
- updated_at DESC: Rejected - created_at is more stable, updates don't change order

**Future Enhancement**: Allow client-side sorting (out of scope for MVP)

---

### R5: What frontend state management approach for task list?

**Question**: Should we use global state (Redux/Zustand) or local state for managing tasks?

**Research**:
- MVP scope: Simple task list, create, edit, delete
- Complexity: 3 pages (list, create, edit)
- Data flow: API-driven, no complex client-side mutations

**Decision**: React useState + API client (no global state)

**Implementation**:
```typescript
// Dashboard page
const [tasks, setTasks] = useState<Task[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  async function loadTasks() {
    const response = await apiGet("/api/tasks");
    const data = await response.json();
    setTasks(data.tasks);
    setLoading(false);
  }
  loadTasks();
}, []);
```

**Rationale**:
- **Simplicity**: Avoid unnecessary complexity for MVP
- **Sufficient**: State only needed on dashboard page
- **Performance**: Task list is small (< 100 items per user)
- **Maintainability**: Less code, easier to understand
- **API-driven**: Refresh from server after mutations (simple, reliable)

**Alternatives Considered**:
1. **Redux Toolkit**:
   - Pros: Predictable state, DevTools, middleware
   - Cons: Boilerplate, overkill for 3 pages, learning curve
   - Rejected: Overengineering for MVP scope

2. **Zustand**:
   - Pros: Lightweight, simple API, global state
   - Cons: Still adds dependency, unnecessary for single-page state
   - Rejected: Local state sufficient for MVP

3. **React Query / SWR**:
   - Pros: Cache management, automatic refetching
   - Cons: Another dependency, complexity for simple CRUD
   - Rejected: Could consider for future if caching becomes important

**Mutation Flow**:
```typescript
// Create task
async function createTask(data) {
  await apiPost("/api/tasks", data);
  router.push("/dashboard");  // Dashboard will reload tasks
}

// Update task
async function updateTask(id, data) {
  await apiPut(`/api/tasks/${id}`, data);
  router.push("/dashboard");  // Dashboard will reload tasks
}

// Delete task
async function deleteTask(id) {
  await apiDelete(`/api/tasks/${id}`);
  // Optimistic update or page reload
  setTasks(tasks.filter(t => t.id !== id));
}
```

---

### R6: How to handle validation errors from FastAPI in the frontend?

**Question**: What's the best way to display Pydantic validation errors in React forms?

**Research**:
- FastAPI returns 422 with structured error details
- Error format: `{detail: [{loc: [...], msg: "...", type: "..."}]}`
- UI patterns: Field-level errors, toast notifications, alert banners

**Decision**: Parse 422 errors and display field-level validation messages

**Implementation**:
```typescript
// Error type
interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

interface ErrorResponse {
  detail: string | ValidationError[];
}

// Form submission
async function handleSubmit(e) {
  try {
    await apiPost("/api/tasks", formData);
    router.push("/dashboard");
  } catch (err) {
    const errorData: ErrorResponse = await err.json();

    if (Array.isArray(errorData.detail)) {
      // Pydantic validation errors
      const fieldErrors = {};
      errorData.detail.forEach(error => {
        const field = error.loc[error.loc.length - 1];
        fieldErrors[field] = error.msg;
      });
      setErrors(fieldErrors);
    } else {
      // Generic error
      setError(errorData.detail);
    }
  }
}
```

**UI Display**:
```tsx
<input
  name="title"
  value={formData.title}
  onChange={handleChange}
  className={errors.title ? "border-red-500" : "border-gray-300"}
/>
{errors.title && (
  <p className="text-red-600 text-sm">{errors.title}</p>
)}
```

**Rationale**:
- **User-friendly**: Shows errors next to relevant fields
- **FastAPI compatible**: Matches Pydantic error structure
- **Accessible**: Screen readers can announce field errors
- **Clear**: User knows exactly what to fix

---

### R7: How to implement status badge colors consistently?

**Question**: What's the visual design pattern for task status indicators?

**Research**:
- Common patterns: Badges, pills, colored dots
- Accessibility: Color + text label (not color alone)
- TailwindCSS utilities: bg-* and text-* classes

**Decision**: Colored badge with status text

**Implementation**:
```typescript
// StatusBadge component
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

**Rationale**:
- **Accessible**: Text + color (not color alone)
- **Consistent**: Uses theme colors (gray, blue, green)
- **Scalable**: Easy to add new statuses
- **Readable**: Text label makes status clear

**Alternatives Considered**:
- Colored dots only: Rejected - not accessible
- Icon-based: Rejected - adds complexity, icon library needed
- Full background color: Rejected - too prominent, distracting

---

## Technology Decisions Summary

| Technology | Purpose | Justification |
|-----------|---------|---------------|
| Python Enum | Status values | Type safety, Pydantic validation |
| Explicit WHERE clauses | User isolation | Visible, auditable, testable |
| 404 (not 403) | Cross-user access | Prevents enumeration attacks |
| created_at DESC | Task ordering | User expectation, indexed |
| React useState | State management | Simple, sufficient for MVP |
| Field-level errors | Validation display | User-friendly, accessible |
| Colored badges | Status display | Clear, accessible, consistent |

## Best Practices Applied

1. **Security First**: User enumeration prevention, explicit isolation
2. **Type Safety**: Enums in Python and TypeScript
3. **Performance**: Database indexing for common queries
4. **Simplicity**: Avoid premature abstraction and complexity
5. **Accessibility**: Color + text for status indicators
6. **API-Driven**: Frontend refreshes from backend after mutations

## Implementation Guidelines

1. **Always filter by user_id**: No exceptions for task queries
2. **Return 404 for isolation failures**: Never 403
3. **Validate on backend**: Frontend validation is UX, backend is security
4. **Use composite indexes**: (user_id, created_at DESC) for list queries
5. **Test isolation**: Multi-user scenarios for every endpoint
6. **Handle errors gracefully**: Parse and display validation errors

## Risks Identified

| Risk | Mitigation |
|------|-----------|
| User isolation bug | Mandatory isolation tests, explicit WHERE clauses, code review |
| N+1 queries | Use single queries, composite index |
| Validation inconsistency | Backend is source of truth, share types |
| Cross-user data leakage | 404 responses, isolation tests |

## Next Steps

1. ✅ Research complete - All unknowns resolved
2. → Phase 1: Generate data-model.md (database schema)
3. → Phase 1: Generate contracts/ (API schemas)
4. → Phase 1: Generate quickstart.md (implementation guide)
5. → Phase 2: Run `/sp.tasks` to create atomic task breakdown

---

**Research Status**: Complete
**Author**: Claude Sonnet 4.5
**Date**: 2025-12-31
