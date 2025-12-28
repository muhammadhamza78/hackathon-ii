# Implementation Plan: CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Build a Python-based CLI todo application with arrow-key navigation, task CRUD operations, completion tracking, and draft support. The application uses `blessed` library for terminal UI, stores data in JSON files (`todos.json`), and follows a modular architecture with separate concerns for UI, data persistence, and business logic.

**Core Technical Approach**:
- Python 3.10+ for modern type hints and features
- `blessed` library for cross-platform keyboard navigation and terminal control
- Single JSON file (`todos.json`) for persistence with separate saved/draft task arrays
- Modular design: UI layer, Storage layer, Models, Main controller
- Menu-driven continuous loop architecture with state management

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `blessed` (terminal UI), standard library only
**Storage**: Single JSON file (`todos.json`) in application directory
**Testing**: Manual testing checklist (unit tests optional for initial version)
**Target Platform**: Windows (CMD, PowerShell, Windows Terminal), Linux (bash, zsh)
**Project Type**: Single project (CLI application)
**Performance Goals**: <2s startup, <1s menu transitions, handles 1000+ tasks
**Constraints**: <200MB memory, keyboard-only input, Unicode support required
**Scale/Scope**: Single-user, local file storage, ~500 LOC total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. CLI-Only Interface (NON-NEGOTIABLE)
- Uses `blessed` for terminal UI (no GUI frameworks)
- No web servers or HTTP endpoints
- Terminal stdin/stdout only

### ✅ II. Keyboard-Driven Navigation (NON-NEGOTIABLE)
- Arrow keys (↑ ↓) for menu navigation via `blessed`
- Enter key for selection confirmation
- Escape/'q' for back navigation
- No mouse interaction

### ✅ III. Unicode Icons and Visual Clarity
- Unicode emoji in menu items (➕ 🔄 🗑️ 📋 ⏳ 📄 🔙)
- Checkboxes for tasks: [ ] and [✔]
- `blessed` handles terminal encoding
- ASCII fallback if needed (handled by library)

### ✅ IV. Code Quality: Clean and Beginner-Friendly
- Clear function/variable names
- Docstrings for all public functions
- PEP 8 compliance
- Max 50 lines per function
- Max 300 lines per file

### ✅ V. Local JSON Storage (NON-NEGOTIABLE)
- Single `todos.json` file
- Human-readable JSON format
- Auto-create if missing
- Graceful error handling for corruption

### ✅ VI. Draft and Saved Task States
- Tasks have `status` field: "saved" | "draft"
- Separate arrays in JSON for logical separation
- Explicit save/draft choice in UI

### ✅ VII. Continuous Loop Until Exit
- Main menu loop runs until Exit selected
- Returns to main menu after each action
- Ctrl+C handled gracefully

**Constitution Compliance**: PASS - All 7 principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── data-model.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── task-schema.json # JSON schema for Task entity
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Entry point, main loop, Ctrl+C handler
├── models/
│   └── task.py          # Task dataclass, TaskList operations
├── storage/
│   └── json_storage.py  # JSON file I/O, validation, backup
├── ui/
│   ├── menu.py          # Menu rendering, arrow navigation
│   ├── forms.py         # Input forms (title, description)
│   └── display.py       # Task list display, checkboxes
└── handlers/
    ├── add_task.py      # Add new task handler
    ├── update_task.py   # Update task handler
    ├── delete_task.py   # Delete task handler
    ├── show_tasks.py    # Show all/pending/draft handlers
    └── exit_handler.py  # Exit confirmation, cleanup

tests/
└── manual_test_checklist.md  # Manual testing steps

todos.json               # Data file (auto-created at runtime)
requirements.txt         # Dependencies: blessed
README.md                # Installation, usage, keyboard shortcuts
```

**Structure Decision**: Single project structure chosen because this is a standalone CLI application with no frontend/backend separation needed. All code lives in `src/` with logical module separation (models, storage, ui, handlers).

## Complexity Tracking

No constitution violations - complexity budget not used.

## Phase 0: Research

### Objective
Validate technical decisions and explore implementation details for keyboard navigation and JSON persistence.

### Research Questions

1. **Keyboard Navigation Library Choice**
   - **Question**: Which library best supports cross-platform arrow key navigation with minimal complexity?
   - **Options Evaluated**:
     - `curses` (standard library): Complex, UNIX-only (Windows requires `windows-curses`)
     - `prompt-toolkit`: Powerful but heavy, async-based
     - `blessed`: Lightweight, cross-platform, beginner-friendly
     - `rich`: Modern but focused on rendering, not navigation
   - **Decision**: Use `blessed` for simplicity, cross-platform support, and constitution alignment (minimal dependencies, beginner-friendly)
   - **Rationale**: `blessed` provides simple API for keyboard input (`term.inkey()`), works on Windows/Linux without extra setup, and is well-documented for beginners

2. **JSON File Structure**
   - **Question**: Should we use one JSON file or separate files for tasks/drafts?
   - **Options Evaluated**:
     - Two files (`tasks.json`, `drafts.json`): User suggestion
     - One file with arrays (`todos.json` with `{saved: [], drafts: []}`): Simpler
   - **Decision**: Single file `todos.json` with two arrays
   - **Rationale**: Atomic writes, simpler backup/recovery, easier to maintain consistency, aligns with constitution (single data file)

3. **Task ID Generation**
   - **Question**: UUID vs timestamp vs sequential integer?
   - **Decision**: UUID (uuid4) for uniqueness without collision risk
   - **Rationale**: No need to track counter, safe for concurrent edits (future-proof), standard library support

4. **Terminal Encoding**
   - **Question**: How to handle Unicode emoji on different terminals?
   - **Decision**: UTF-8 encoding with `blessed` automatic handling
   - **Rationale**: `blessed` detects terminal capabilities and handles encoding; modern terminals support UTF-8

### Research Artifacts

**File**: `specs/001-cli-todo-app/research.md`

```markdown
# Research Notes: CLI Todo App

## Library Evaluation

### blessed vs curses vs prompt-toolkit
- **blessed**: ✅ Chosen - Cross-platform, simple API, beginner-friendly
- **curses**: ❌ Windows support requires extra package
- **prompt-toolkit**: ❌ Overly complex for our needs

## JSON Schema Design

Single file structure:
{
  "saved": [Task, Task, ...],
  "drafts": [Task, Task, ...]
}

Advantages:
- Atomic file writes
- Single backup point
- Easier consistency

## Terminal Compatibility Testing
- Windows Terminal: ✅ UTF-8 default
- PowerShell: ✅ UTF-8 with [Console]::OutputEncoding
- CMD: ⚠️ May need chcp 65001
- bash/zsh: ✅ UTF-8 default

## References
- blessed docs: https://blessed.readthedocs.io/
- Python UUID: https://docs.python.org/3/library/uuid.html
```

## Phase 1: Design

### Objective
Create detailed data model, API contracts, and quickstart guide.

### Data Model

**File**: `specs/001-cli-todo-app/data-model.md`

#### Task Entity

```python
@dataclass
class Task:
    """Represents a todo task with metadata."""
    id: str              # UUID4 string
    title: str           # Required, non-empty, max 200 chars
    description: str     # Optional, can be empty, max 1000 chars
    completed: bool      # True if marked done
    status: str          # "saved" | "draft"
    created_at: str      # ISO 8601 timestamp
    updated_at: str      # ISO 8601 timestamp
```

**Validation Rules**:
- `title`: Required, 1-200 characters, stripped whitespace
- `description`: Optional, 0-1000 characters
- `id`: Auto-generated UUID4, immutable
- `status`: Enum validated, must be "saved" or "draft"
- Timestamps: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm)

#### TaskList Operations

```python
class TaskList:
    """Manages collection of tasks with CRUD operations."""

    def add_task(task: Task, status: str) -> None:
        """Add task to saved or draft list."""

    def get_task(task_id: str) -> Optional[Task]:
        """Retrieve task by ID from any list."""

    def update_task(task_id: str, updates: dict) -> bool:
        """Update task fields and timestamp."""

    def delete_task(task_id: str) -> bool:
        """Remove task from any list."""

    def toggle_complete(task_id: str) -> bool:
        """Toggle completed status."""

    def get_saved_tasks() -> List[Task]:
        """Get all saved tasks."""

    def get_draft_tasks() -> List[Task]:
        """Get all draft tasks."""

    def get_pending_tasks() -> List[Task]:
        """Get saved tasks where completed=False."""

    def move_to_saved(task_id: str) -> bool:
        """Move draft task to saved list."""
```

#### JSON File Schema

**File**: `specs/001-cli-todo-app/contracts/task-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "saved": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "format": "uuid"},
          "title": {"type": "string", "minLength": 1, "maxLength": 200},
          "description": {"type": "string", "maxLength": 1000},
          "completed": {"type": "boolean"},
          "status": {"type": "string", "enum": ["saved"]},
          "created_at": {"type": "string", "format": "date-time"},
          "updated_at": {"type": "string", "format": "date-time"}
        },
        "required": ["id", "title", "description", "completed", "status", "created_at", "updated_at"]
      }
    },
    "drafts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "format": "uuid"},
          "title": {"type": "string", "minLength": 1, "maxLength": 200},
          "description": {"type": "string", "maxLength": 1000},
          "completed": {"type": "boolean"},
          "status": {"type": "string", "enum": ["draft"]},
          "created_at": {"type": "string", "format": "date-time"},
          "updated_at": {"type": "string", "format": "date-time"}
        },
        "required": ["id", "title", "description", "completed", "status", "created_at", "updated_at"]
      }
    }
  },
  "required": ["saved", "drafts"]
}
```

### API Contracts

**File**: `specs/001-cli-todo-app/contracts/module-interfaces.md`

#### Storage Layer Contract

```python
# storage/json_storage.py

def load_data() -> dict:
    """
    Load data from todos.json.

    Returns:
        dict: {"saved": [...], "drafts": [...]}

    Raises:
        FileNotFoundError: If file doesn't exist (caller creates default)
        JSONDecodeError: If file is corrupted (caller handles recovery)
    """

def save_data(data: dict) -> bool:
    """
    Atomically save data to todos.json.

    Args:
        data: {"saved": [...], "drafts": [...]}

    Returns:
        bool: True if successful, False otherwise

    Side Effects:
        - Creates backup (.bak) before writing
        - Writes to temp file then renames (atomic)
    """

def validate_schema(data: dict) -> bool:
    """
    Validate data against JSON schema.

    Returns:
        bool: True if valid, False otherwise
    """

def create_backup() -> str:
    """
    Create timestamped backup of todos.json.

    Returns:
        str: Path to backup file
    """
```

#### UI Layer Contract

```python
# ui/menu.py

def show_menu(options: List[str], current: int, term) -> None:
    """
    Render menu with arrow navigation.

    Args:
        options: List of menu items with icons
        current: Currently selected index (0-based)
        term: blessed Terminal instance
    """

def get_menu_selection(options: List[str], term) -> int:
    """
    Display menu and wait for user selection.

    Returns:
        int: Selected index (0-based), -1 if escape/q pressed
    """

# ui/forms.py

def get_text_input(prompt: str, required: bool, max_length: int, term) -> Optional[str]:
    """
    Get single-line text input from user.

    Args:
        prompt: Input prompt to display
        required: If True, validates non-empty
        max_length: Maximum character limit

    Returns:
        str: User input (stripped), None if cancelled
    """

def get_save_option(term) -> str:
    """
    Show "Save Task" / "Save as Draft" menu.

    Returns:
        str: "saved" | "draft" | "cancel"
    """

# ui/display.py

def show_task_list(tasks: List[Task], term, allow_toggle: bool = False) -> Optional[str]:
    """
    Display task list with arrow navigation.

    Args:
        tasks: List of Task objects to display
        allow_toggle: If True, Enter toggles checkbox

    Returns:
        str: Selected task ID, None if escape/q pressed
    """

def show_message(message: str, term, wait: bool = True) -> None:
    """
    Display message and optionally wait for keypress.
    """
```

### Quickstart Guide

**File**: `specs/001-cli-todo-app/quickstart.md`

```markdown
# Quickstart: CLI Todo App

## Installation

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

```bash
python src/main.py
```

## First Time Usage

1. App starts with main menu
2. Press ↓ to navigate, Enter to select
3. Select "Add new task ➕"
4. Enter title (required)
5. Enter description (or skip)
6. Select "Save Task"
7. Task appears in "Show all task 📋"

## Keyboard Shortcuts

- **↑ / ↓**: Navigate menu
- **Enter**: Select / Toggle checkbox
- **Escape / q**: Back to main menu
- **Ctrl+C**: Exit app (saves automatically)

## Data Location

Tasks stored in: `todos.json` (auto-created)

## Troubleshooting

- **Icons not showing**: Ensure terminal uses UTF-8 encoding
- **File permission error**: Check write permissions in app directory
- **Corrupted JSON**: App creates backup and resets to empty state
```

## Phase 2: Architecture Decisions

### Decision 1: Keyboard Navigation Library

**Context**: Need cross-platform arrow key input with minimal complexity for beginner-friendly codebase.

**Options**:
1. `curses` (standard library)
2. `blessed` (third-party)
3. `prompt-toolkit` (third-party)

**Decision**: Use `blessed`

**Rationale**:
- Cross-platform without extra packages (works on Windows/Linux)
- Simple API: `term.inkey()` for keyboard input, easy to understand
- Beginner-friendly documentation
- Lightweight (aligns with constitution: minimal dependencies)
- Active maintenance and good community support

**Trade-offs**:
- Adds one external dependency (acceptable per constitution)
- Slightly less control than `curses` (not needed for our use case)

**Consequences**:
- Developers must `pip install blessed`
- Code examples easily understood by Python beginners
- Windows support works out-of-the-box

---

### Decision 2: Single vs Multiple JSON Files

**Context**: User suggested separate `tasks.json` and `drafts.json` files, but constitution emphasizes single data file.

**Options**:
1. Two files: `tasks.json`, `drafts.json`
2. One file: `todos.json` with `{saved: [], drafts: []}`

**Decision**: Single file `todos.json`

**Rationale**:
- Constitution Principle V states: "MUST use a single data file: `todos.json`"
- Atomic writes prevent inconsistency between files
- Simpler backup/recovery (one file to manage)
- Easier to maintain referential integrity
- Simpler code (one load/save function)

**Trade-offs**:
- Slightly larger file size (negligible for typical use)
- Must separate saved/drafts in memory (trivial with dict structure)

**Consequences**:
- Load/save operations handle both lists together
- Backup is comprehensive (no partial state)
- Moving task from draft to saved is simple status change

---

### Decision 3: Task ID Strategy

**Context**: Need unique identifiers for tasks to support update/delete operations.

**Options**:
1. Sequential integers (1, 2, 3, ...)
2. Timestamps (epoch milliseconds)
3. UUID4 (random UUIDs)

**Decision**: UUID4

**Rationale**:
- No collision risk (critical for data integrity)
- No need to track counter state
- Standard library support (`uuid.uuid4()`)
- Future-proof (e.g., if we later support import/export)
- Immutable and globally unique

**Trade-offs**:
- Less human-readable than integers (acceptable - users don't see IDs)
- Larger storage (36 chars vs int) - negligible impact

**Consequences**:
- Task creation generates new UUID
- IDs are strings in JSON schema
- No counter management needed in storage layer

---

### Decision 4: Error Handling Strategy

**Context**: Must handle file I/O errors, JSON corruption, and invalid input per constitution.

**Decision**: Layered error handling with user-friendly messages

**Approach**:
1. **Storage layer**: Catches low-level errors (FileNotFoundError, JSONDecodeError)
2. **Handler layer**: Validates input, provides actionable errors
3. **UI layer**: Displays formatted messages (no stack traces)

**Error Categories**:
- **Validation errors**: "Title cannot be empty. Press any key to retry."
- **File errors**: "Cannot write to todos.json. Check permissions."
- **Corruption**: "Data file corrupted. Created backup at todos.json.bak. Starting fresh."

**Consequences**:
- Users never see Python exceptions
- Errors include recovery instructions
- Backup created before any destructive operation

---

## Phase 3: Implementation Roadmap

### Module Dependencies

```
main.py
  ├─> handlers/* (add, update, delete, show, exit)
  │     ├─> ui/* (menu, forms, display)
  │     ├─> models/task.py
  │     └─> storage/json_storage.py
  │
  ├─> ui/menu.py (for main menu)
  └─> storage/json_storage.py (for init/cleanup)
```

**Build Order**:
1. `models/task.py` (no dependencies)
2. `storage/json_storage.py` (depends on models)
3. `ui/menu.py`, `ui/forms.py`, `ui/display.py` (depends on models)
4. `handlers/*` (depends on all above)
5. `main.py` (orchestrates everything)

### File Scaffolding

Each file includes:
- Module docstring
- Imports (grouped: standard library, third-party, local)
- Constants (if needed)
- Functions/classes with docstrings
- Main guard if executable

**Example**: `src/models/task.py`

```python
"""Task data model and TaskList operations.

This module defines the Task dataclass and TaskList class for managing
todo tasks with CRUD operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
    """Represents a todo task with metadata.

    Attributes:
        id: Unique UUID4 identifier
        title: Task title (required, 1-200 chars)
        description: Task description (optional, max 1000 chars)
        completed: Completion status (True if done)
        status: "saved" or "draft"
        created_at: ISO 8601 creation timestamp
        updated_at: ISO 8601 last update timestamp
    """
    id: str
    title: str
    description: str
    completed: bool
    status: str
    created_at: str
    updated_at: str

    @staticmethod
    def create(title: str, description: str, status: str) -> "Task":
        """Create new Task with auto-generated ID and timestamps."""
        # Implementation here

    def to_dict(self) -> dict:
        """Convert Task to dictionary for JSON serialization."""
        # Implementation here


class TaskList:
    """Manages collections of tasks with CRUD operations."""
    # Implementation here
```

### Cross-Cutting Concerns

#### Logging
- Use `print()` for user messages (no logging library needed)
- Debug mode can be added later if needed (constitution: YAGNI)

#### Configuration
- No config file (constitution: simplicity)
- Hardcoded constants in modules (file paths, limits)

#### Unicode Fallback
- `blessed` handles terminal capabilities
- If emoji fails, ASCII alternatives: [x], +, -, ?

#### Ctrl+C Handling
- Signal handler in `main.py`
- Calls `storage.save_data()` before exit
- Displays "Saving and exiting..." message

## Testing Strategy

### Manual Testing Checklist

**File**: `tests/manual_test_checklist.md`

```markdown
# Manual Testing Checklist

## Prerequisites
- [ ] Python 3.10+ installed
- [ ] blessed installed (`pip install blessed`)
- [ ] Fresh terminal (UTF-8 encoding)

## Test Cases

### TC001: First Launch
- [ ] Run `python src/main.py`
- [ ] Main menu appears with 7 options and icons
- [ ] No errors or warnings

### TC002: Add Task (Saved)
- [ ] Select "Add new task ➕"
- [ ] Enter title: "Test Task"
- [ ] Enter description: "Test Description"
- [ ] Select "Save Task"
- [ ] Returns to main menu

### TC003: View All Tasks
- [ ] Select "Show all task 📋"
- [ ] See "Test Task" with [ ] checkbox
- [ ] Press q to return to menu

### TC004: Mark Complete
- [ ] Select "Show all task 📋"
- [ ] Navigate to task, press Enter
- [ ] Checkbox changes to [✔]
- [ ] Press q to return to menu

### TC005: View Pending
- [ ] Select "Show pending task ⏳"
- [ ] Task not shown (completed)
- [ ] See "No pending tasks" message

### TC006: Persistence
- [ ] Exit app (select "Exit 🔙")
- [ ] Restart app
- [ ] Select "Show all task 📋"
- [ ] Task still present with [✔]

### TC007: Update Task
- [ ] Select "Update previous task 🔄"
- [ ] Select task
- [ ] Change title to "Updated Task"
- [ ] Select "Save Task"
- [ ] Verify change in "Show all task"

### TC008: Delete Task
- [ ] Select "Delete previous task 🗑️"
- [ ] Select task
- [ ] Confirm deletion
- [ ] Task removed from list

### TC009: Draft Task
- [ ] Select "Add new task ➕"
- [ ] Enter title: "Draft Task"
- [ ] Skip description
- [ ] Select "Save as Draft"
- [ ] Select "Draft 📄"
- [ ] See "Draft Task" in list

### TC010: Error Handling
- [ ] Select "Add new task ➕"
- [ ] Leave title empty, press Enter
- [ ] See validation error message
- [ ] Can retry or cancel

### TC011: Ctrl+C Handling
- [ ] Add a task
- [ ] Press Ctrl+C
- [ ] See "Saving and exiting..." message
- [ ] Restart app
- [ ] Task persists

### TC012: Empty States
- [ ] Delete all tasks
- [ ] Select "Show all task 📋"
- [ ] See "No tasks found" message
- [ ] Select "Draft 📄"
- [ ] See "No draft tasks" message

## Platform Testing
- [ ] Test on Windows Terminal
- [ ] Test on PowerShell
- [ ] Test on CMD (with chcp 65001)
- [ ] Test on Linux bash
- [ ] Test on Linux zsh

## Edge Cases
- [ ] Title with 200 characters (max length)
- [ ] Description with 1000 characters
- [ ] Unicode characters in title/description
- [ ] 100+ tasks (performance check)
- [ ] Manually corrupt todos.json (recovery check)
```

### Unit Tests (Optional)

If time permits, add tests for:
- `Task.create()` - validates ID generation and timestamps
- `TaskList` operations - add, update, delete, filter
- `json_storage` - load/save/validate
- Input validation functions

**Framework**: `pytest` (if implemented)

## Deployment and Packaging

### Requirements File

**File**: `requirements.txt`

```
blessed==1.20.0
```

### README Template

**File**: `README.md`

```markdown
# CLI Todo Application

A simple, keyboard-driven todo app for the command line.

## Features
- ➕ Add tasks with title and description
- 🔄 Update existing tasks
- 🗑️ Delete tasks
- 📋 View all tasks with completion checkboxes
- ⏳ Filter pending tasks
- 📄 Save drafts
- ⌨️ Full keyboard navigation (no mouse needed)

## Installation

1. Requires Python 3.10 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app:
```bash
python src/main.py
```

## Keyboard Shortcuts
- **↑ / ↓**: Navigate menus
- **Enter**: Select option / Toggle checkbox
- **Escape / q**: Back to main menu
- **Ctrl+C**: Exit (saves automatically)

## Data Storage
Tasks are saved in `todos.json` in the application directory.

## Troubleshooting

**Icons not displaying?**
- Ensure your terminal uses UTF-8 encoding
- Windows CMD: Run `chcp 65001` before starting app

**Permission errors?**
- Check write permissions in app directory
- Try running from user home directory

**Data corrupted?**
- App automatically creates backup (`.bak` file)
- Restart app to create fresh data file

## License
MIT
```

## Risks and Mitigations

### Risk 1: Terminal Compatibility
**Risk**: Unicode emoji may not render on older terminals
**Likelihood**: Low (modern terminals support UTF-8)
**Mitigation**: `blessed` handles encoding; document encoding requirements in README
**Contingency**: Add ASCII fallback if reports come in

### Risk 2: File Permissions
**Risk**: User may not have write permissions in app directory
**Likelihood**: Medium (especially on restricted systems)
**Mitigation**: Check permissions on startup, display clear error message
**Contingency**: Allow user to specify alternate data file location

### Risk 3: Large Task Lists
**Risk**: Performance degradation with 1000+ tasks
**Likelihood**: Low (typical usage <100 tasks)
**Mitigation**: No pagination needed initially (YAGNI)
**Contingency**: Add pagination if issue reported

### Risk 4: JSON Corruption
**Risk**: Power loss or crash during write corrupts data
**Likelihood**: Low
**Mitigation**: Atomic write (write to temp, rename), create backup before write
**Contingency**: Restore from `.bak` file or start fresh

## Success Metrics

- [ ] All 5 user stories testable independently
- [ ] Constitution compliance: 7/7 principles satisfied
- [ ] Startup time <2 seconds
- [ ] All 18 acceptance criteria pass
- [ ] Code follows PEP 8
- [ ] All functions <50 lines
- [ ] All files <300 lines
- [ ] README complete with keyboard shortcuts
- [ ] Manual test checklist passes on Windows and Linux
- [ ] No external dependencies except `blessed`

## Next Steps

1. Run `/sp.tasks` to generate task breakdown
2. Implement Phase 1 (Setup): Project structure, requirements.txt
3. Implement Phase 2 (Foundation): models, storage, basic UI
4. Implement Phase 3 (User Story 1): Add + view tasks
5. Implement Phase 4 (User Story 2): Completion tracking
6. Implement Phase 5 (User Story 5): Navigation polish
7. Implement Phase 6 (User Story 3): Update + delete
8. Implement Phase 7 (User Story 4): Draft support
9. Run manual test checklist
10. Write README and quickstart guide
