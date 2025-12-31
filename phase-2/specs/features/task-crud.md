# Feature Specification: Task CRUD Operations

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Feature ID**: F002
**Status:** Specification
**Dependencies**: F001 (Authentication)

## Overview

Enable authenticated users to Create, Read, Update, and Delete (CRUD) their personal tasks with complete data isolation. All operations enforce user-level security through JWT authentication.

## Business Requirements

### BR1: Task Creation
Users must be able to create new tasks with a title, optional description, and status.

**Value**: Allows users to capture and organize their to-do items.

**User Story**:
> As an authenticated user, I want to create a new task with a title and description, so that I can track my work items.

### BR2: Task Listing
Users must be able to view a list of all their tasks.

**Value**: Provides overview of all user's tasks in one place.

**User Story**:
> As an authenticated user, I want to see a list of all my tasks, so that I can review what needs to be done.

### BR3: Task Detail View
Users must be able to view details of a single task.

**Value**: Allows users to see full information for a specific task.

**User Story**:
> As an authenticated user, I want to view the details of a specific task, so that I can see all its information.

### BR4: Task Update
Users must be able to update any property of their tasks (title, description, status).

**Value**: Allows users to modify tasks as requirements change.

**User Story**:
> As an authenticated user, I want to update my task's title, description, or status, so that I can keep my tasks current.

### BR5: Task Deletion
Users must be able to delete tasks they no longer need.

**Value**: Allows users to remove completed or unwanted tasks.

**User Story**:
> As an authenticated user, I want to delete a task, so that I can remove items I no longer need to track.

### BR6: User Data Isolation
Users must ONLY be able to access their own tasks, never tasks belonging to other users.

**Value**: Critical security requirement to protect user privacy.

**User Story**:
> As a user, I expect that my tasks are private and no other user can see or modify them.

## Functional Requirements

### Task Data Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique task identifier |
| title | String | Required, Max 200 chars | Task title |
| description | String | Optional, Max 2000 chars | Detailed task description |
| status | Enum | Required, One of: pending, in_progress, completed | Current task status |
| user_id | Integer | Required, Foreign Key to users.id | Task owner |
| created_at | DateTime | Auto-generated, Immutable | Task creation timestamp |
| updated_at | DateTime | Auto-updated | Last modification timestamp |

### Task Status Values

- **pending**: Task not yet started (default)
- **in_progress**: Task currently being worked on
- **completed**: Task finished

### FR1: Create Task

**Endpoint**: `POST /api/tasks`

**Authentication**: Required (JWT)

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

**Field Validation**:
- `title`: Required, non-empty string, max 200 chars
- `description`: Optional string, max 2000 chars, can be null or empty
- `status`: Optional, one of [pending, in_progress, completed], defaults to "pending"

**Response (201 Created)**:
```json
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "user_id": 456,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Business Logic**:
1. Extract user_id from JWT token
2. Validate request body
3. Auto-assign user_id from JWT (NEVER from request body)
4. Set created_at and updated_at to current timestamp
5. Insert into database
6. Return created task

**Error Cases**:
- 401 Unauthorized: Missing or invalid JWT token
- 422 Validation Error: Title missing or too long, description too long, invalid status

**Acceptance Criteria**:
- [ ] Task created with valid data returns 201 with task object
- [ ] Task auto-assigned to authenticated user
- [ ] Title is required (400 if missing)
- [ ] Title max length enforced (422 if exceeded)
- [ ] Description max length enforced (422 if exceeded)
- [ ] Invalid status value rejected (422)
- [ ] Default status is "pending" if not provided
- [ ] created_at and updated_at are set automatically
- [ ] Unauthenticated request returns 401

### FR2: List All Tasks

**Endpoint**: `GET /api/tasks`

**Authentication**: Required (JWT)

**Query Parameters**: None (filtering/pagination out of scope for MVP)

**Response (200 OK)**:
```json
{
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
      "description": null,
      "status": "in_progress",
      "user_id": 456,
      "created_at": "2025-12-30T11:00:00Z",
      "updated_at": "2025-12-30T11:30:00Z"
    }
  ]
}
```

**Business Logic**:
1. Extract user_id from JWT token
2. Query database for all tasks where user_id matches
3. Order by created_at DESC (newest first)
4. Return array of tasks

**Error Cases**:
- 401 Unauthorized: Missing or invalid JWT token

**Acceptance Criteria**:
- [ ] Returns only tasks owned by authenticated user
- [ ] Returns empty array if user has no tasks
- [ ] Tasks ordered by created_at descending
- [ ] All task fields included in response
- [ ] Unauthenticated request returns 401

**User Isolation Test**:
- [ ] User A creates task
- [ ] User B lists tasks
- [ ] User B does NOT see User A's task

### FR3: Get Single Task

**Endpoint**: `GET /api/tasks/{task_id}`

**Authentication**: Required (JWT)

**Path Parameters**:
- `task_id`: Integer (task ID)

**Response (200 OK)**:
```json
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "user_id": 456,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Business Logic**:
1. Extract user_id from JWT token
2. Query database for task with matching id AND user_id
3. If found, return task
4. If not found, return 404

**Error Cases**:
- 401 Unauthorized: Missing or invalid JWT token
- 404 Not Found: Task doesn't exist OR task exists but belongs to different user

**Acceptance Criteria**:
- [ ] Returns task if owned by authenticated user
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 404 if task exists but belongs to different user (isolation)
- [ ] All task fields included in response
- [ ] Unauthenticated request returns 401

**User Isolation Test**:
- [ ] User A creates task with ID 123
- [ ] User B attempts GET /api/tasks/123
- [ ] User B receives 404 (NOT the task data)

### FR4: Update Task

**Endpoint**: `PUT /api/tasks/{task_id}`

**Authentication**: Required (JWT)

**Path Parameters**:
- `task_id`: Integer (task ID)

**Request Body** (all fields optional):
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": "in_progress"
}
```

**Field Validation**:
- `title`: Optional, if provided must be non-empty and max 200 chars
- `description`: Optional, if provided max 2000 chars, can be null to clear
- `status`: Optional, if provided must be one of [pending, in_progress, completed]

**Response (200 OK)**:
```json
{
  "id": 123,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": "in_progress",
  "user_id": 456,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Business Logic**:
1. Extract user_id from JWT token
2. Validate request body
3. Query database for task with matching id AND user_id
4. If not found, return 404
5. Update only provided fields
6. Set updated_at to current timestamp
7. Save to database
8. Return updated task

**Error Cases**:
- 401 Unauthorized: Missing or invalid JWT token
- 404 Not Found: Task doesn't exist OR task exists but belongs to different user
- 422 Validation Error: Title too long, description too long, invalid status

**Acceptance Criteria**:
- [ ] Updates task if owned by authenticated user
- [ ] Only provided fields are updated
- [ ] updated_at is automatically updated
- [ ] created_at is NOT changed
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 404 if task exists but belongs to different user (isolation)
- [ ] Validation errors return 422
- [ ] Unauthenticated request returns 401

**User Isolation Test**:
- [ ] User A creates task with ID 123
- [ ] User B attempts PUT /api/tasks/123 with new title
- [ ] User B receives 404 (update is NOT applied)
- [ ] User A's task remains unchanged

### FR5: Delete Task

**Endpoint**: `DELETE /api/tasks/{task_id}`

**Authentication**: Required (JWT)

**Path Parameters**:
- `task_id`: Integer (task ID)

**Response (204 No Content)**:
No response body.

**Business Logic**:
1. Extract user_id from JWT token
2. Query database for task with matching id AND user_id
3. If not found, return 404
4. Delete task from database
5. Return 204

**Error Cases**:
- 401 Unauthorized: Missing or invalid JWT token
- 404 Not Found: Task doesn't exist OR task exists but belongs to different user

**Acceptance Criteria**:
- [ ] Deletes task if owned by authenticated user
- [ ] Returns 204 on successful deletion
- [ ] Returns 404 if task doesn't exist
- [ ] Returns 404 if task exists but belongs to different user (isolation)
- [ ] Subsequent GET for same task returns 404
- [ ] Unauthenticated request returns 401

**User Isolation Test**:
- [ ] User A creates task with ID 123
- [ ] User B attempts DELETE /api/tasks/123
- [ ] User B receives 404 (deletion is NOT applied)
- [ ] User A's task still exists

### FR6: User Data Isolation

**Requirement**: Every task operation MUST filter by user_id extracted from JWT token.

**Implementation**:
- user_id extracted from JWT token in authentication middleware/dependency
- All database queries include `WHERE user_id = {user_id_from_jwt}`
- user_id NEVER accepted from request body or query parameters
- Failed isolation check returns 404 (not 403, to avoid enumeration)

**Testing**:
- Multi-user integration tests for every endpoint
- Attempt to access/modify other user's tasks
- Verify 404 responses (not 403 or success)

**Acceptance Criteria**:
- [ ] All task queries filter by user_id from JWT
- [ ] user_id from request body/params is ignored
- [ ] Cross-user access attempts return 404
- [ ] Tests verify isolation for all CRUD operations

## Non-Functional Requirements

### Performance

- **Response Time**: Task CRUD operations < 200ms (p95)
- **Database Queries**: Single query per operation (no N+1)
- **Indexing**: Index on (user_id, created_at) for list queries

### Security

- **Authentication**: JWT required for all endpoints
- **Isolation**: User data isolation MUST be enforced (NON-NEGOTIABLE)
- **Validation**: All input validated with Pydantic
- **SQL Injection**: Prevented by ORM (SQLModel)

### Data Integrity

- **Foreign Key**: task.user_id references users.id
- **Cascade Delete**: When user deleted, all their tasks deleted
- **Timestamps**: created_at immutable, updated_at auto-updated

### Scalability

- **Pagination**: Not in MVP, but design should allow future addition
- **Filtering**: Not in MVP, but database schema supports adding indexes

## UI/UX Requirements

### Dashboard View (Task List)

**Layout**:
- Display tasks in a list/card format
- Show title, status badge, and truncated description
- Sort by created_at descending (newest first)
- "New Task" button prominently displayed

**Empty State**:
- If no tasks, show message: "No tasks yet. Create your first task!"

### Task Creation Form

**Fields**:
- Title (text input, required, max 200 chars)
- Description (textarea, optional, max 2000 chars)
- Status (dropdown, defaults to "pending")
- Submit button: "Create Task"
- Cancel button: Return to task list

**Validation Feedback**:
- Show character count for title and description
- Highlight errors (e.g., "Title is required")
- Disable submit if validation fails

### Task Edit Form

**Fields**: Same as creation form, pre-populated with existing values

**Actions**:
- Update button: "Save Changes"
- Cancel button: Return to task list
- Delete button: "Delete Task" (with confirmation)

**Confirmation**:
- On delete, show confirmation dialog: "Are you sure you want to delete this task? This action cannot be undone."

### Status Display

**Visual Indicators**:
- `pending`: Gray badge
- `in_progress`: Blue badge
- `completed`: Green badge

## Test Scenarios

### TS1: Create Task - Happy Path
1. User authenticates and receives JWT
2. User submits POST /api/tasks with valid data
3. System creates task and returns 201 with task object
4. user_id auto-assigned from JWT
5. created_at and updated_at are set

**Expected**: Task created successfully

### TS2: Create Task - Validation Errors
1. User submits task with empty title → 422 error
2. User submits task with 250-char title → 422 error
3. User submits task with invalid status → 422 error

**Expected**: Validation errors returned with field details

### TS3: List Tasks - User Isolation
1. User A creates 3 tasks
2. User B creates 2 tasks
3. User A lists tasks → receives 3 tasks
4. User B lists tasks → receives 2 tasks

**Expected**: Each user sees only their own tasks

### TS4: Get Task - Cross-User Access
1. User A creates task with ID 123
2. User B attempts GET /api/tasks/123
3. System returns 404

**Expected**: User B cannot access User A's task

### TS5: Update Task - Happy Path
1. User A creates task
2. User A updates task title and status
3. System returns updated task
4. updated_at is newer than created_at

**Expected**: Task updated successfully

### TS6: Update Task - Cross-User Modification
1. User A creates task with ID 123
2. User B attempts PUT /api/tasks/123
3. System returns 404
4. User A's task remains unchanged

**Expected**: User B cannot modify User A's task

### TS7: Delete Task - Happy Path
1. User creates task
2. User deletes task
3. System returns 204
4. Subsequent GET returns 404

**Expected**: Task deleted successfully

### TS8: Delete Task - Cross-User Deletion
1. User A creates task with ID 123
2. User B attempts DELETE /api/tasks/123
3. System returns 404
4. User A's task still exists

**Expected**: User B cannot delete User A's task

### TS9: Unauthenticated Access
1. Request without JWT token to any task endpoint
2. System returns 401

**Expected**: All endpoints require authentication

## Edge Cases

### EC1: Invalid Task ID
- GET/PUT/DELETE with non-existent task_id → 404
- GET/PUT/DELETE with non-integer task_id → 422

### EC2: Null Description
- Create task with description: null → Accepted, stored as null
- Update task with description: null → Clears description

### EC3: Empty String vs Null
- Title as empty string → Validation error (required)
- Description as empty string → Accepted, stored as empty string

### EC4: Concurrent Updates
- Two clients update same task simultaneously
- Last write wins (no optimistic locking in MVP)

### EC5: Large Task List
- User with 1000+ tasks
- List endpoint returns all (pagination in future)
- Performance may degrade (acceptable for MVP)

## Dependencies

**Depends On**:
- F001 (Authentication): Requires JWT authentication to be implemented
- Database schema: Users table and Tasks table must exist

**Blocks**:
- None (this is core feature)

## Out of Scope

The following are explicitly OUT OF SCOPE for this feature:

- Task search or filtering
- Task sorting (beyond default created_at DESC)
- Pagination
- Task sharing or collaboration
- Task categories or tags
- Task priority levels
- Task due dates or reminders
- Task attachments
- Bulk operations (delete multiple, update multiple)
- Task templates
- Task versioning or history

## Acceptance Criteria Summary

**Feature is DONE when**:
- [ ] All 5 CRUD endpoints implemented and tested
- [ ] User isolation verified with multi-user tests (TS3, TS4, TS6, TS8)
- [ ] All validation rules enforced
- [ ] All error cases return correct status codes
- [ ] UI allows creating, viewing, updating, and deleting tasks
- [ ] API documentation (OpenAPI) generated and accurate
- [ ] Integration tests pass with >80% coverage
- [ ] Manual testing completed for all user flows

## References

- See: `specs/architecture.md` (API contracts section)
- See: `specs/database/schema.md` (Task table definition)
- See: `specs/api/rest-endpoints.md` (Detailed endpoint specs)
- See: `.specify/memory/constitution.md` (User Data Isolation principle)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
