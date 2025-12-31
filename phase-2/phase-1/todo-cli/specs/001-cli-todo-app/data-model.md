# Data Model: CLI Todo Application

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28

## Entities

### Task

Represents a single todo task with all metadata.

```python
@dataclass
class Task:
    """Represents a todo task with metadata."""
    id: str              # UUID4 string (e.g., "f47ac10b-58cc-4372-a567-0e02b2c3d479")
    title: str           # Required, 1-200 characters
    description: str     # Optional, 0-1000 characters (empty string if not provided)
    completed: bool      # True if task is marked done, False otherwise
    status: str          # "saved" | "draft"
    created_at: str      # ISO 8601 timestamp (e.g., "2025-12-28T10:30:45.123456")
    updated_at: str      # ISO 8601 timestamp
```

**Validation Rules**:
- `id`: Auto-generated UUID4, immutable, must be unique
- `title`: Required, cannot be empty after stripping, max 200 characters
- `description`: Optional, can be empty string, max 1000 characters
- `completed`: Boolean, defaults to False on creation
- `status`: Must be exactly "saved" or "draft"
- `created_at`: ISO 8601 format, set on Task.create(), immutable
- `updated_at`: ISO 8601 format, updated on any modification

**Business Rules**:
- Only saved tasks can be marked completed (drafts cannot be completed)
- Moving from draft to saved preserves all fields except status
- Deleting a task is permanent (no soft delete)
- Title is always stripped of leading/trailing whitespace

### TaskList

Manages the collection of tasks with CRUD operations.

```python
class TaskList:
    """Manages collections of tasks with CRUD operations."""

    def __init__(self, saved: List[Task], drafts: List[Task]):
        """Initialize with saved and draft task lists."""
        self.saved = saved
        self.drafts = drafts

    def add_task(self, task: Task, status: str) -> None:
        """Add task to appropriate list based on status."""

    def get_task(self, task_id: str) -> Optional[Task]:
        """Find and return task by ID from any list."""

    def update_task(self, task_id: str, updates: dict) -> bool:
        """Update task fields and refresh updated_at timestamp."""

    def delete_task(self, task_id: str) -> bool:
        """Remove task from its list. Returns True if found and deleted."""

    def toggle_complete(self, task_id: str) -> bool:
        """Toggle completed status for saved tasks only."""

    def get_saved_tasks(self) -> List[Task]:
        """Return all saved tasks (completed and incomplete)."""

    def get_draft_tasks(self) -> List[Task]:
        """Return all draft tasks."""

    def get_pending_tasks(self) -> List[Task]:
        """Return saved tasks where completed=False."""

    def move_to_saved(self, task_id: str) -> bool:
        """Move task from drafts to saved, update status field."""

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict: {saved: [...], drafts: [...]}"""
```

## JSON Storage Format

### File Structure

**File**: `todos.json` (created in application directory)

```json
{
  "saved": [
    {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "status": "saved",
      "created_at": "2025-12-28T10:30:45.123456",
      "updated_at": "2025-12-28T10:30:45.123456"
    },
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Finish project report",
      "description": "",
      "completed": true,
      "status": "saved",
      "created_at": "2025-12-27T14:20:10.987654",
      "updated_at": "2025-12-28T09:15:30.456789"
    }
  ],
  "drafts": [
    {
      "id": "12345678-90ab-cdef-1234-567890abcdef",
      "title": "Call dentist",
      "description": "",
      "completed": false,
      "status": "draft",
      "created_at": "2025-12-28T11:00:00.000000",
      "updated_at": "2025-12-28T11:00:00.000000"
    }
  ]
}
```

### Schema Constraints

- Root object must have exactly two keys: `saved` and `drafts`
- Both `saved` and `drafts` must be arrays (can be empty)
- Each task object must have all 7 required fields
- Tasks in `saved` array must have `status: "saved"`
- Tasks in `drafts` array must have `status: "draft"`
- All `id` values must be unique across both arrays
- Timestamps must be valid ISO 8601 format

### File Operations

#### Initialization
- If `todos.json` doesn't exist, create with empty arrays: `{"saved": [], "drafts": []}`
- Perform on first app launch

#### Loading
- Read `todos.json`
- Validate JSON syntax
- Validate schema (all fields present, correct types)
- If validation fails: create backup `.bak`, reset to empty state
- Convert dict to TaskList object

#### Saving
- Convert TaskList to dict
- Write to temporary file `todos.json.tmp`
- Rename `todos.json` to `todos.json.bak` (atomic backup)
- Rename `todos.json.tmp` to `todos.json` (atomic write)
- If any step fails, rollback and report error

## State Transitions

### Task Lifecycle

```
[Created] --> status="draft" --> [Draft List]
                    |
                    v
         User: "Save as Draft"
                    |
                    v
              [Draft List] <--> [Update] --> [Draft List]
                    |
                    v
         User: "Save Task"
                    |
                    v
            status="saved" --> [Saved List]
                    |
                    v
              [Saved List] <--> [Update/Complete] --> [Saved List]
                    |
                    v
            User: "Delete"
                    |
                    v
               [Deleted]
```

### Status Changes

- **Draft to Saved**: `move_to_saved()` updates status field, moves task from drafts to saved
- **Saved to Draft**: Not allowed (one-way transition)
- **Completion Toggle**: Only allowed for saved tasks
- **Delete**: Allowed from any state

## Data Integrity Rules

1. **Uniqueness**: No two tasks can have the same `id`
2. **Referential Integrity**: Task status must match its array location
3. **Timestamp Consistency**: `updated_at` >= `created_at`
4. **Completion Constraint**: Draft tasks always have `completed=False`
5. **Title Required**: Title cannot be empty string after strip

## Performance Considerations

- **In-Memory**: All tasks loaded into memory (acceptable for <10,000 tasks)
- **Linear Search**: Finding task by ID is O(n), acceptable for typical usage
- **Full File Write**: Every change rewrites entire file (simple, atomic)
- **No Indexing**: Not needed for small datasets

## Migration Strategy

**Version 1.0** (initial): Schema as defined above

**Future Versions** (if needed):
- Add `version` field to root object
- Implement migration functions for schema changes
- Preserve backward compatibility or provide migration tool

## Example Operations

### Create New Task

```python
task = Task.create(
    title="Buy groceries",
    description="Milk, eggs, bread",
    status="saved"
)
# Result: Task with auto-generated id, timestamps, completed=False
```

### Load from JSON

```python
data = load_data()  # {"saved": [...], "drafts": [...]}
task_list = TaskList(
    saved=[Task(**t) for t in data["saved"]],
    drafts=[Task(**t) for t in data["drafts"]]
)
```

### Move Draft to Saved

```python
success = task_list.move_to_saved(task_id)
# Changes task.status from "draft" to "saved"
# Moves from drafts array to saved array
# Updates task.updated_at
```

### Toggle Completion

```python
success = task_list.toggle_complete(task_id)
# Toggles task.completed: False -> True or True -> False
# Updates task.updated_at
# Only works for saved tasks (not drafts)
```

### Filter Pending Tasks

```python
pending = task_list.get_pending_tasks()
# Returns tasks where status="saved" AND completed=False
```
