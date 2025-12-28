# Feature Specification: CLI-Based Todo Application

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Build a CLI-based Todo Application with arrow-key navigation, task management (add/update/delete), draft support, and completion tracking"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Task Creation and Viewing (Priority: P1)

As a user, I want to create tasks with titles and optional descriptions, and view all my saved tasks, so that I can track what I need to do.

**Why this priority**: This is the core functionality - without the ability to create and view tasks, the application has no purpose. This represents the minimum viable product (MVP).

**Independent Test**: User can launch app, add a task with title "Buy groceries", save it, navigate to "Show all task", and see the task listed. App can be restarted and task persists.

**Acceptance Scenarios**:

1. **Given** app is launched, **When** user navigates with arrow keys and selects "Add new task ➕", **Then** title input field appears
2. **Given** user is on title input, **When** user enters "Buy groceries" and proceeds, **Then** description input appears with option to skip
3. **Given** user has entered title, **When** user selects "Save Task", **Then** task is saved to main list and user returns to main menu
4. **Given** user has saved tasks, **When** user selects "Show all task 📋", **Then** all saved tasks are displayed with checkboxes [ ]
5. **Given** app has saved tasks, **When** user exits and restarts app, **Then** previously saved tasks are still present (persistence test)

---

### User Story 2 - Task Completion Tracking (Priority: P1)

As a user, I want to mark tasks as completed and view only pending tasks, so that I can focus on what still needs to be done.

**Why this priority**: Completion tracking is essential to the todo app concept. Without this, users cannot distinguish between done and pending work. Part of MVP alongside task creation.

**Independent Test**: User can create two tasks, mark one as completed in "Show all task", then navigate to "Show pending task" and see only the uncompleted task.

**Acceptance Scenarios**:

1. **Given** user is viewing all tasks, **When** user navigates with arrow keys to a task and presses Enter, **Then** checkbox changes from [ ] to [✔]
2. **Given** a task is marked completed [✔], **When** user presses Enter again, **Then** checkbox toggles back to [ ] (incomplete)
3. **Given** user has mix of completed and incomplete tasks, **When** user selects "Show pending task ⏳", **Then** only incomplete tasks are displayed
4. **Given** all tasks are completed, **When** user selects "Show pending task ⏳", **Then** message "No pending tasks" is displayed

---

### User Story 3 - Task Modification and Deletion (Priority: P2)

As a user, I want to update or delete existing tasks, so that I can correct mistakes or remove tasks that are no longer relevant.

**Why this priority**: Users need the ability to modify tasks, but the app is functional without this feature initially. Can be added after core create/view/complete functionality works.

**Independent Test**: User can create a task "Buy milk", update it to "Buy almond milk", verify the change persists, then delete it and confirm it's gone from the list.

**Acceptance Scenarios**:

1. **Given** user selects "Update previous task 🔄", **When** saved tasks list is displayed, **Then** user can navigate with arrow keys to select a task
2. **Given** user selects a task to update, **When** title/description edit fields appear, **Then** user can modify the text
3. **Given** user has modified a task, **When** user selects "Save Task", **Then** changes are persisted to main list
4. **Given** user selects "Delete previous task 🗑️", **When** user navigates to a task and presses Enter, **Then** task is removed from the list
5. **Given** user is about to delete a task, **When** confirmation prompt appears, **Then** user can confirm or cancel the deletion

---

### User Story 4 - Draft Task Management (Priority: P3)

As a user, I want to save incomplete tasks as drafts, so that I can return later to finish filling out details without committing to the main task list.

**Why this priority**: Draft functionality is a nice-to-have feature that improves workflow but is not essential for basic task management. Can be implemented last.

**Independent Test**: User can create a task with just a title, save as draft, exit app, restart, navigate to "Draft 📄", and see the draft task. User can then complete and save it to main list.

**Acceptance Scenarios**:

1. **Given** user is creating a new task, **When** user selects "Save as Draft", **Then** task is saved to draft list (not main list)
2. **Given** user selects "Draft 📄", **When** draft list appears, **Then** all draft tasks are displayed with arrow navigation
3. **Given** user selects "Update previous task 🔄", **When** editing a task, **Then** user can save as Draft instead of to main list
4. **Given** user has a draft task, **When** user edits and saves it as "Save Task", **Then** it moves from draft list to main saved list
5. **Given** draft list is empty, **When** user selects "Draft 📄", **Then** message "No draft tasks" is displayed

---

### User Story 5 - Navigation and Exit Flow (Priority: P1)

As a user, I want intuitive keyboard navigation throughout the app and the ability to safely exit, so that I can efficiently use the app without mouse dependency.

**Why this priority**: Keyboard navigation is a core constitutional requirement and is essential for the CLI experience. Must be implemented from the start.

**Independent Test**: User can navigate entire app using only arrow keys, Enter, and Escape/q. Exit option safely closes app and preserves all data.

**Acceptance Scenarios**:

1. **Given** app starts, **When** main menu displays, **Then** user sees arrow-navigable menu with all 7 options and icons
2. **Given** user is in main menu, **When** user presses ↓ arrow, **Then** selection moves to next menu item
3. **Given** user is in main menu, **When** user presses ↑ arrow, **Then** selection moves to previous menu item (wraps around)
4. **Given** user is in any submenu, **When** user presses Escape or 'q', **Then** user returns to main menu
5. **Given** user selects "Exit 🔙", **When** user confirms exit, **Then** app closes gracefully and all data is saved
6. **Given** user is in the app, **When** user presses Ctrl+C, **Then** app handles interrupt gracefully, saves state, and exits

---

### Edge Cases

- What happens when user tries to view tasks but no tasks exist? → Display "No tasks found" message
- What happens when user enters empty title for a task? → Validation error: "Title is required"
- What happens when JSON file is corrupted? → Display error, create backup, initialize fresh file
- What happens when user tries to update/delete but no saved tasks exist? → Display "No saved tasks available"
- What happens when terminal doesn't support Unicode? → Fallback to ASCII characters (e.g., [x] instead of [✔])
- What happens when user navigates past last menu item? → Selection wraps around to first item
- What happens when todos.json is read-only? → Display permission error, offer to save to alternate location
- What happens when user enters extremely long title (>500 chars)? → Truncate or warn about length limit
- What happens when description contains special characters or newlines? → JSON escaping handles correctly, display preserves formatting

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display main menu with 7 options on startup: Add new task, Update previous task, Delete previous task, Show all task, Show pending task, Draft, Exit
- **FR-002**: System MUST support arrow key (↑ ↓) navigation for all menus and lists
- **FR-003**: System MUST confirm selection with Enter key
- **FR-004**: System MUST allow Escape or 'q' to return to previous menu/main menu
- **FR-005**: System MUST display Unicode icons for each menu option (➕ 🔄 🗑️ 📋 ⏳ 📄 🔙)
- **FR-006**: System MUST require title input for all tasks (cannot be empty)
- **FR-007**: System MUST allow optional description input for tasks (can be skipped/empty)
- **FR-008**: System MUST provide two save options when creating/editing tasks: "Save Task" and "Save as Draft"
- **FR-009**: System MUST persist saved tasks to `todos.json` file in JSON format
- **FR-010**: System MUST persist draft tasks separately from saved tasks
- **FR-011**: System MUST display checkboxes [ ] for all tasks in "Show all task" view
- **FR-012**: System MUST toggle checkbox to [✔] when task is marked complete
- **FR-013**: System MUST display only incomplete tasks in "Show pending task" view
- **FR-014**: System MUST display only draft tasks in "Draft" view
- **FR-015**: System MUST allow updating title and description of existing saved tasks
- **FR-016**: System MUST allow deletion of saved tasks with confirmation
- **FR-017**: System MUST create `todos.json` automatically if it doesn't exist
- **FR-018**: System MUST return to main menu after completing any action
- **FR-019**: System MUST run in continuous loop until user selects Exit
- **FR-020**: System MUST handle Ctrl+C gracefully (save state and exit)
- **FR-021**: System MUST validate JSON file structure on load and recover from corruption
- **FR-022**: System MUST display clear error messages for invalid input (no stack traces)
- **FR-023**: System MUST display visual indicator for currently selected menu item
- **FR-024**: System MUST clear screen appropriately between menu transitions for readability

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item with the following attributes:
  - `id`: Unique identifier (auto-generated, UUID or timestamp-based)
  - `title`: Required text field, user-entered task name
  - `description`: Optional text field, additional task details
  - `completed`: Boolean flag, true if task is marked done
  - `created_at`: Timestamp of task creation
  - `updated_at`: Timestamp of last modification
  - `status`: Enum (saved | draft) - distinguishes main tasks from drafts

- **TaskList**: Collection of tasks with operations:
  - Add task (to saved or draft)
  - Update task (modify title/description, change status)
  - Delete task (remove from list)
  - Mark complete/incomplete (toggle completed flag)
  - Filter by status (saved vs draft)
  - Filter by completion (completed vs pending)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can create a task with title only in under 10 seconds (3 keystrokes: arrow to Add, Enter, type, Enter)
- **SC-002**: User can create a task with title and description in under 20 seconds
- **SC-003**: User can mark a task as completed in under 5 seconds (arrow to Show all, Enter, arrow to task, Enter)
- **SC-004**: User can navigate entire menu using only keyboard (no mouse required for any operation)
- **SC-005**: Application starts and displays main menu in under 2 seconds
- **SC-006**: All tasks persist correctly across application restarts (100% data retention)
- **SC-007**: Application handles 1000+ tasks without performance degradation
- **SC-008**: Unicode icons render correctly in Windows Terminal, PowerShell, bash, and zsh
- **SC-009**: Application never crashes on invalid input (graceful error handling for all edge cases)
- **SC-010**: User can complete primary task workflow (add → view → complete → view pending) on first attempt without documentation
- **SC-011**: JSON file remains human-readable and can be manually edited if needed
- **SC-012**: Application returns to main menu within 1 second after any action

### User Experience Goals

- **UX-001**: Menu navigation feels intuitive and responsive
- **UX-002**: Visual feedback clearly indicates current selection
- **UX-003**: Error messages are helpful and actionable (e.g., "Title cannot be empty. Press any key to retry.")
- **UX-004**: Unicode icons enhance readability without being distracting
- **UX-005**: Screen transitions are smooth (clear screen appropriately, avoid flicker)
- **UX-006**: Confirmation prompts prevent accidental deletions
- **UX-007**: Empty states provide helpful guidance (e.g., "No tasks yet. Press 'a' or select Add new task to get started.")

## Technical Constraints

- **TC-001**: MUST be implemented in Python 3.8 or higher
- **TC-002**: MUST use only standard library OR minimal dependencies (`blessed`, `rich`, or `click` allowed)
- **TC-003**: MUST store all data in single `todos.json` file (no database)
- **TC-004**: MUST support Windows (CMD, PowerShell, Windows Terminal) and Linux (bash, zsh) terminals
- **TC-005**: MUST handle terminal resize gracefully (or document minimum terminal size requirements)
- **TC-006**: MUST follow PEP 8 style guidelines
- **TC-007**: MUST include docstrings for all functions and classes
- **TC-008**: Code MUST be beginner-friendly (clear naming, no complex patterns)
- **TC-009**: Maximum function length: 50 lines
- **TC-010**: MUST NOT use GUI libraries (Tkinter, PyQt, etc.)
- **TC-011**: MUST NOT use web frameworks or create web servers

## Out of Scope

The following are explicitly NOT included in this feature:

- Multi-user support or user authentication
- Cloud sync or remote storage
- Task categories, tags, or labels
- Task priorities or due dates
- Subtasks or task dependencies
- Search or filter by keywords
- Task sorting (custom order, alphabetical, by date)
- Export to other formats (CSV, PDF, etc.)
- Undo/redo functionality
- Task recurrence or reminders
- Color customization or themes
- Command-line arguments (app must be interactive menu-driven)
- Configuration file support
- Integration with other todo systems
- Task statistics or analytics

## Acceptance Checklist

Before considering this feature complete, verify:

- [ ] All 7 menu options are functional and navigable with arrow keys
- [ ] Tasks can be created with title (required) and description (optional)
- [ ] Tasks persist to `todos.json` and reload correctly on app restart
- [ ] Tasks can be marked complete/incomplete with checkbox toggle
- [ ] "Show pending task" displays only incomplete tasks
- [ ] Draft tasks are saved separately and accessible via "Draft" menu
- [ ] Tasks can be updated (title and description modification)
- [ ] Tasks can be deleted with confirmation prompt
- [ ] App runs in continuous loop until Exit is selected
- [ ] Ctrl+C exits gracefully without data loss
- [ ] Unicode icons render correctly in target terminals
- [ ] Error messages are clear and helpful (no stack traces)
- [ ] Empty states display appropriate messages
- [ ] JSON file is created automatically if missing
- [ ] Corrupted JSON is detected and handled (backup + fresh start)
- [ ] All edge cases are handled gracefully
- [ ] Code follows constitution guidelines (PEP 8, docstrings, beginner-friendly)
- [ ] README includes installation, usage, and keyboard shortcuts
- [ ] Manual testing checklist completed on Windows and Linux

## Dependencies and Assumptions

### Dependencies
- Python 3.8+ installed
- Terminal with Unicode support (recommended: Windows Terminal, modern bash/zsh)
- File system write permissions for `todos.json`

### Assumptions
- User has basic terminal/command-line familiarity
- User's terminal supports arrow key input
- User's terminal uses UTF-8 encoding for Unicode support
- Single user per `todos.json` file (no concurrent access handling needed)
- Tasks are text-based (no images, attachments, or rich media)
- Reasonable task count (< 10,000 tasks for optimal performance)

## Related Artifacts

- Constitution: `.specify/memory/constitution.md`
- Plan: `specs/001-cli-todo-app/plan.md` (to be created by `/sp.plan`)
- Tasks: `specs/001-cli-todo-app/tasks.md` (to be created by `/sp.tasks`)
- Implementation: `src/` (to be determined in plan)
