---
description: "Task list for CLI Todo Application implementation"
---

# Tasks: CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (required), research.md (optional)

**Tests**: Not required for initial version (manual testing only)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure: `src/`, `src/models/`, `src/storage/`, `src/ui/`, `src/handlers/`, `tests/`
- [X] T002 Create `requirements.txt` with `blessed==1.20.0`
- [X] T003 [P] Create `.gitignore` with entries: `__pycache__/`, `*.pyc`, `todos.json`, `todos.json.bak`, `.venv/`, `venv/`
- [X] T004 [P] Create empty `__init__.py` files in: `src/`, `src/models/`, `src/storage/`, `src/ui/`, `src/handlers/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Task Model and Data Layer

- [X] T005 Implement `Task` dataclass in `src/models/task.py` with fields: id, title, description, completed, status, created_at, updated_at
- [X] T006 Implement `Task.create()` static method in `src/models/task.py` for creating new tasks with auto-generated UUID and timestamps
- [X] T007 Implement `Task.to_dict()` method in `src/models/task.py` for JSON serialization
- [X] T008 Implement `Task.from_dict()` static method in `src/models/task.py` for JSON deserialization
- [X] T009 Implement `TaskList` class in `src/models/task.py` with __init__ accepting saved and drafts lists
- [X] T010 Implement `TaskList.to_dict()` method in `src/models/task.py` returning `{"saved": [...], "drafts": [...]}`

### Storage Layer

- [X] T011 Implement `load_data()` function in `src/storage/json_storage.py` to read todos.json, handle FileNotFoundError (return empty dict), handle JSONDecodeError (raise for caller)
- [X] T012 Implement `save_data(data: dict)` function in `src/storage/json_storage.py` with atomic write: write to .tmp, backup original to .bak, rename .tmp to todos.json
- [X] T013 Implement `validate_schema(data: dict)` function in `src/storage/json_storage.py` to check structure: has "saved" and "drafts" keys, both are lists
- [X] T014 Implement `create_backup()` function in `src/storage/json_storage.py` to copy todos.json to todos.json.bak with timestamp

### UI Foundation (blessed)

- [X] T015 Implement `show_menu(options, current, term)` function in `src/ui/menu.py` to render menu with highlighted current selection using blessed
- [X] T016 Implement `get_menu_selection(options, term)` function in `src/ui/menu.py` to handle arrow key navigation (↑ ↓), Enter to select, Escape/q to cancel (return -1)
- [X] T017 Implement `get_text_input(prompt, required, max_length, term)` function in `src/ui/forms.py` for single-line text input with validation
- [X] T018 Implement `show_message(message, term, wait)` function in `src/ui/display.py` to display message and optionally wait for keypress

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Creation and Viewing (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks and view them, with persistence across restarts

**Independent Test**: User can add task "Buy groceries", view it in "Show all task", restart app, and task persists

### Implementation for User Story 1

- [X] T019 [P] [US1] Implement `TaskList.add_task(task, status)` method in `src/models/task.py` to append task to saved or drafts list
- [X] T020 [P] [US1] Implement `TaskList.get_saved_tasks()` method in `src/models/task.py` to return saved list
- [X] T021 [US1] Implement `get_save_option(term)` function in `src/ui/forms.py` to show menu: "Save Task" / "Save as Draft" / "Cancel", return "saved" | "draft" | "cancel"
- [X] T022 [US1] Implement `add_task_handler(task_list, term)` function in `src/handlers/add_task.py`: get title input (required), get description input (optional), get save option, create Task, add to TaskList
- [X] T023 [US1] Implement `show_task_list(tasks, term, allow_toggle)` function in `src/ui/display.py` to display tasks with arrow navigation, show checkboxes `[ ]` or `[✔]` based on completed field
- [X] T024 [US1] Implement `show_all_handler(task_list, term)` function in `src/handlers/show_tasks.py` to get saved tasks and call show_task_list with allow_toggle=False (view only for now)
- [X] T025 [US1] Create `src/main.py` with main() function: initialize blessed Terminal, load data (or create empty), create TaskList, show main menu loop with 7 options
- [X] T026 [US1] In `src/main.py`, implement main menu dispatcher: handle "Add new task ➕" calling add_task_handler, handle "Show all task 📋" calling show_all_handler
- [X] T027 [US1] In `src/main.py`, implement Ctrl+C signal handler to save data before exit with message "Saving and exiting..."
- [X] T028 [US1] In `src/main.py`, add save_data() call after each handler returns to persist changes

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (add task, view task, persistence)

---

## Phase 4: User Story 2 - Task Completion Tracking (Priority: P1)

**Goal**: Enable users to mark tasks complete/incomplete and view only pending tasks

**Independent Test**: User creates two tasks, marks one complete, views pending tasks and sees only the incomplete one

### Implementation for User Story 2

- [X] T029 [P] [US2] Implement `TaskList.toggle_complete(task_id)` method in `src/models/task.py` to flip completed boolean and update updated_at timestamp
- [X] T030 [P] [US2] Implement `TaskList.get_task(task_id)` method in `src/models/task.py` to find and return task by id from saved or drafts list
- [X] T031 [P] [US2] Implement `TaskList.get_pending_tasks()` method in `src/models/task.py` to return tasks where status="saved" AND completed=False
- [X] T032 [US2] Update `show_task_list()` in `src/ui/display.py` to support allow_toggle=True: when Enter pressed on task, return task_id for toggling
- [X] T033 [US2] Update `show_all_handler()` in `src/handlers/show_tasks.py` to enable allow_toggle=True, handle returned task_id by calling toggle_complete()
- [X] T034 [US2] Implement `show_pending_handler(task_list, term)` function in `src/handlers/show_tasks.py` to get pending tasks and display with message "No pending tasks" if empty
- [X] T035 [US2] In `src/main.py`, add main menu handler for "Show pending task ⏳" calling show_pending_handler

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (create, view, complete, filter pending)

---

## Phase 5: User Story 5 - Navigation and Exit Flow (Priority: P1)

**Goal**: Ensure smooth keyboard navigation and safe exit

**Independent Test**: User can navigate entire app with arrow keys and Escape, exit safely with data preserved

### Implementation for User Story 5

- [X] T036 [US5] Update `get_menu_selection()` in `src/ui/menu.py` to support wraparound: when at last item and press ↓, go to first item; when at first item and press ↑, go to last item
- [X] T037 [US5] Add screen clearing in `src/ui/menu.py` and `src/ui/display.py` using `term.clear()` before rendering menus for clean transitions
- [X] T038 [US5] Implement `exit_handler(term)` function in `src/handlers/exit_handler.py` to show confirmation: "Exit application? (Y/N)", return True if confirmed
- [X] T039 [US5] In `src/main.py`, add main menu handler for "Exit 🔙" calling exit_handler, break loop if confirmed
- [X] T040 [US5] Test and verify Ctrl+C handler in `src/main.py` saves data correctly before exiting

**Checkpoint**: At this point, core MVP (US1, US2, US5) is complete and fully navigable

---

## Phase 6: User Story 3 - Task Modification and Deletion (Priority: P2)

**Goal**: Enable users to update or delete existing tasks

**Independent Test**: User creates task "Buy milk", updates to "Buy almond milk", verifies change, then deletes and confirms removal

### Implementation for User Story 3

- [X] T041 [P] [US3] Implement `TaskList.update_task(task_id, updates)` method in `src/models/task.py` to update title/description fields and refresh updated_at timestamp
- [X] T042 [P] [US3] Implement `TaskList.delete_task(task_id)` method in `src/models/task.py` to remove task from saved or drafts list, return True if found and deleted
- [X] T043 [US3] Update `show_task_list()` in `src/ui/display.py` to support selection_mode="select": when Enter pressed, return selected task_id (not toggle)
- [X] T044 [US3] Implement `update_task_handler(task_list, term)` function in `src/handlers/update_task.py`: show task list for selection, get title input (pre-filled with current), get description input (pre-filled), get save option, call update_task()
- [X] T045 [US3] Implement `show_confirmation(message, term)` function in `src/ui/display.py` to show Yes/No confirmation, return True if Yes
- [X] T046 [US3] Implement `delete_task_handler(task_list, term)` function in `src/handlers/delete_task.py`: show task list for selection, show confirmation "Delete this task? (Y/N)", call delete_task() if confirmed
- [X] T047 [US3] In `src/main.py`, add main menu handler for "Update previous task 🔄" calling update_task_handler
- [X] T048 [US3] In `src/main.py`, add main menu handler for "Delete previous task 🗑️" calling delete_task_handler

**Checkpoint**: At this point, User Stories 1, 2, 3, and 5 should all work independently (full CRUD + navigation)

---

## Phase 7: User Story 4 - Draft Task Management (Priority: P3)

**Goal**: Enable users to save tasks as drafts and convert drafts to saved tasks

**Independent Test**: User creates draft task, views it in "Draft 📄", updates and saves it, verifies it moved to saved list

### Implementation for User Story 4

- [X] T049 [P] [US4] Implement `TaskList.get_draft_tasks()` method in `src/models/task.py` to return drafts list
- [X] T050 [P] [US4] Implement `TaskList.move_to_saved(task_id)` method in `src/models/task.py` to move task from drafts to saved, update status field to "saved", update updated_at
- [X] T051 [US4] Implement `show_drafts_handler(task_list, term)` function in `src/handlers/show_tasks.py` to get draft tasks and display with message "No draft tasks" if empty
- [X] T052 [US4] Update `update_task_handler()` in `src/handlers/update_task.py` to show both saved AND draft tasks for selection (combined list)
- [X] T053 [US4] Update `update_task_handler()` in `src/handlers/update_task.py` to handle save option: if task was draft and "Save Task" selected, call move_to_saved()
- [X] T054 [US4] In `src/main.py`, add main menu handler for "Draft 📄" calling show_drafts_handler

**Checkpoint**: All user stories (US1, US2, US3, US4, US5) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Add input validation in `src/ui/forms.py`: get_text_input() should enforce max_length, strip whitespace, show error if required and empty
- [ ] T056 [P] Add error handling in `src/storage/json_storage.py`: if load_data() gets JSONDecodeError, call create_backup(), return empty dict `{"saved": [], "drafts": []}`
- [ ] T057 Add empty state messages in all handlers: "No tasks found", "No saved tasks available", "No draft tasks", "No pending tasks"
- [ ] T058 [P] Add visual indicator in `src/ui/menu.py`: highlight current selection with `term.reverse()` or arrow symbol "→"
- [ ] T059 Add Unicode icons to main menu options in `src/main.py`: "Add new task ➕", "Update previous task 🔄", "Delete previous task 🗑️", "Show all task 📋", "Show pending task ⏳", "Draft 📄", "Exit 🔙"
- [ ] T060 [P] Create `README.md` with: Installation, Usage, Keyboard shortcuts, Troubleshooting (from quickstart.md)
- [ ] T061 [P] Create `tests/manual_test_checklist.md` from plan.md testing section with all 12 test cases
- [ ] T062 Verify PEP 8 compliance across all Python files using `flake8` or manual review
- [ ] T063 Add docstrings to all public functions and classes following Google or NumPy style
- [ ] T064 Test on Windows Terminal and PowerShell to verify Unicode rendering
- [ ] T065 Test on Linux bash/zsh to verify cross-platform compatibility

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Depends on US1 (needs task display functionality)
  - User Story 5 (Phase 5): Depends on US1 (needs basic menu structure)
  - User Story 3 (Phase 6): Depends on US1 (needs task selection)
  - User Story 4 (Phase 7): Depends on US1 and US3 (needs add and update handlers)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 completion (T019-T028) - needs show_task_list() and TaskList methods
- **User Story 5 (P1)**: Depends on US1 completion (T019-T028) - needs main menu structure
- **User Story 3 (P2)**: Depends on US1 completion (T019-T028) - needs task selection UI
- **User Story 4 (P3)**: Depends on US1 (T019-T028) and US3 (T041-T048) - needs add and update handlers

### Within Each Phase

**Phase 2 (Foundational)**:
- T005-T010 (Task model): Can run in parallel [P]
- T011-T014 (Storage): Can run in parallel [P], but after T005-T010 (needs Task class)
- T015-T018 (UI Foundation): Can run in parallel [P], no dependencies on Task model

**Phase 3 (User Story 1)**:
- T019-T020: Can run in parallel [P]
- T021-T024: Can run in parallel [P], depend on T005-T018
- T025-T028: Sequential, depend on all above tasks

**Phase 4 (User Story 2)**:
- T029-T031: Can run in parallel [P]
- T032-T034: Sequential, depend on T029-T031
- T035: Depends on T034

**Phase 5 (User Story 5)**:
- T036-T038: Can run in parallel [P]
- T039-T040: Sequential, depend on T036-T038

**Phase 6 (User Story 3)**:
- T041-T042: Can run in parallel [P]
- T043-T046: Can run in parallel [P], depend on T041-T042
- T047-T048: Sequential, depend on T043-T046

**Phase 7 (User Story 4)**:
- T049-T050: Can run in parallel [P]
- T051-T053: Sequential, depend on T049-T050
- T054: Depends on T051-T053

**Phase 8 (Polish)**:
- T055-T056, T058-T061, T064-T065: Can run in parallel [P]
- T057, T059, T062-T063: Sequential (affect multiple files)

### Parallel Opportunities

**Phase 2 - Foundational**:
```bash
# Can run in parallel:
Task: "Implement Task dataclass" (T005)
Task: "Implement Task.create() static method" (T006)
Task: "Implement Task.to_dict() method" (T007)
Task: "Implement Task.from_dict() static method" (T008)
```

**Phase 3 - User Story 1**:
```bash
# Can run in parallel:
Task: "Implement TaskList.add_task()" (T019)
Task: "Implement TaskList.get_saved_tasks()" (T020)
```

**Phase 8 - Polish**:
```bash
# Can run in parallel:
Task: "Add input validation in forms.py" (T055)
Task: "Add error handling in json_storage.py" (T056)
Task: "Add visual indicator in menu.py" (T058)
Task: "Create README.md" (T060)
Task: "Create manual_test_checklist.md" (T061)
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 + 5 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T018) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T019-T028)
4. Complete Phase 4: User Story 2 (T029-T035)
5. Complete Phase 5: User Story 5 (T036-T040)
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational (T001-T018) → Foundation ready
2. Add User Story 1 (T019-T028) → Test independently → Basic add/view works
3. Add User Story 2 (T029-T035) → Test independently → Completion tracking works
4. Add User Story 5 (T036-T040) → Test independently → Navigation polished (MVP complete!)
5. Add User Story 3 (T041-T048) → Test independently → Update/delete works
6. Add User Story 4 (T049-T054) → Test independently → Draft support works
7. Complete Polish (T055-T065) → Final validation → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T018)
2. Once Foundational is done:
   - Developer A: User Story 1 (T019-T028)
   - Developer B: User Story 2 - BLOCKED until A finishes T023-T024
   - Developer C: UI Foundation polish (can work on T036-T037 in parallel)
3. After US1 complete:
   - Developer A: User Story 3 (T041-T048)
   - Developer B: User Story 2 (T029-T035)
   - Developer C: User Story 5 (T036-T040)
4. Final polish (T055-T065) - all developers contribute

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Task Count Summary

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 14 tasks (CRITICAL PATH)
- **Phase 3 (User Story 1 - P1)**: 10 tasks
- **Phase 4 (User Story 2 - P1)**: 7 tasks
- **Phase 5 (User Story 5 - P1)**: 5 tasks
- **Phase 6 (User Story 3 - P2)**: 8 tasks
- **Phase 7 (User Story 4 - P3)**: 6 tasks
- **Phase 8 (Polish)**: 11 tasks

**Total**: 65 tasks

**MVP Tasks** (US1 + US2 + US5): T001-T040 = 40 tasks
**Full Feature**: T001-T065 = 65 tasks
