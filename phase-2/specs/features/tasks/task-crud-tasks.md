---
description: "Atomic task breakdown for Task CRUD implementation (Feature F002)"
---

# Tasks: Task CRUD Operations

**Input**: Design documents from `/specs/features/plans/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Feature**: F002 - Task CRUD Operations
**Dependencies**: F001 (Authentication) - Complete ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` (models/, schemas/, api/v1/, tests/)
- **Frontend**: `frontend/` (app/, components/, lib/, types/)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify F001 prerequisites and prepare for Task CRUD implementation

**Note**: Most setup already complete from F001 (Authentication). This phase verifies readiness.

- [X] T001 Verify backend authentication dependency get_current_user_id() exists in backend/app/auth/dependencies.py
- [X] T002 Verify frontend API client with JWT auto-injection exists in frontend/lib/api.ts
- [X] T003 [P] Verify database session dependency get_session() exists in backend/app/db/session.py

**Checkpoint**: Prerequisites verified - ready for foundational work

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task models, schemas, and infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T004 [P] Create TaskStatus enum in backend/app/models/task.py (values: pending, in_progress, completed)
- [X] T005 Create Task SQLModel in backend/app/models/task.py with fields (id, title, description, status, user_id, created_at, updated_at)
- [X] T006 [P] Create TaskCreateRequest Pydantic schema in backend/app/schemas/task.py (title, description, status)
- [X] T007 [P] Create TaskUpdateRequest Pydantic schema in backend/app/schemas/task.py (all fields optional)
- [X] T008 [P] Create TaskResponse Pydantic schema in backend/app/schemas/task.py (all Task fields)
- [X] T009 Create TaskListResponse Pydantic schema in backend/app/schemas/task.py (tasks array)
- [X] T010 Create task router file backend/app/api/v1/tasks.py with FastAPI router setup and get_current_user_id dependency import
- [X] T011 Register task router in backend/app/main.py (app.include_router with prefix="/api/tasks")

### Database Migration

- [ ] T012 Create database migration for tasks table in database/migrations/ with schema (columns, foreign key to users, check constraint for status, indexes: user_id and composite user_id+created_at DESC)

### Frontend Foundation

- [X] T013 [P] Create TaskStatus type in frontend/types/task.ts (union type: "pending" | "in_progress" | "completed")
- [X] T014 [P] Create Task interface in frontend/types/task.ts (id, title, description, status, user_id, created_at, updated_at)
- [X] T015 [P] Create TaskCreateRequest interface in frontend/types/task.ts
- [X] T016 [P] Create TaskUpdateRequest interface in frontend/types/task.ts
- [X] T017 [P] Create TaskListResponse interface in frontend/types/task.ts
- [X] T018 Create task API client file frontend/lib/task-api.ts with imports (api client, Task types)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks and view a list of all their tasks

**Business Value**: Core functionality - users can capture tasks and see them in one place

**Independent Test**:
1. User logs in → navigates to dashboard → sees empty state
2. User clicks "New Task" → fills form (title, description) → submits
3. User redirected to dashboard → sees newly created task in list
4. User creates second task → list shows 2 tasks ordered by newest first
5. User logs out and logs in with different account → sees empty list (isolation verified)

### Backend: Create Task (FR1)

- [X] T019 [US1] Implement POST /api/tasks endpoint in backend/app/api/v1/tasks.py (extract user_id from JWT, validate request, auto-assign user_id, create task, return 201 with TaskResponse)
- [X] T020 [US1] Add input validation for create endpoint (title required, max 200 chars; description optional, max 2000 chars; status enum validation)
- [X] T021 [US1] Add error handling for create endpoint (401 for missing JWT, 422 for validation errors)

### Backend: List Tasks (FR2)

- [X] T022 [P] [US1] Implement GET /api/tasks endpoint in backend/app/api/v1/tasks.py (extract user_id from JWT, query WHERE user_id=user_id ORDER BY created_at DESC, return TaskListResponse)
- [X] T023 [P] [US1] Add error handling for list endpoint (401 for missing JWT, return empty array if no tasks)

### Frontend: API Client

- [X] T024 [P] [US1] Implement getTasks() function in frontend/lib/task-api.ts (GET /api/tasks, return TaskListResponse)
- [X] T025 [P] [US1] Implement createTask(data: TaskCreateRequest) function in frontend/lib/task-api.ts (POST /api/tasks, return Task)

### Frontend: Components

- [X] T026 [P] [US1] Create StatusBadge component in frontend/components/tasks/StatusBadge.tsx (displays status with color-coded badge: gray=pending, blue=in_progress, green=completed)
- [X] T027 [P] [US1] Create TaskCard component in frontend/components/tasks/TaskCard.tsx (displays single task with title, StatusBadge, truncated description, click navigation to edit)
- [X] T028 [US1] Create TaskList component in frontend/components/tasks/TaskList.tsx (maps tasks array to TaskCard components, empty state message if no tasks)
- [X] T029 [US1] Create TaskForm component in frontend/components/tasks/TaskForm.tsx (controlled form with title input, description textarea, status dropdown, character count, validation errors display, submit/cancel buttons)

### Frontend: Pages

- [X] T030 [US1] Update dashboard page in frontend/app/dashboard/page.tsx (fetch tasks with getTasks on mount, display TaskList component, "New Task" button linking to /tasks/new, loading state)
- [X] T031 [US1] Create task creation page in frontend/app/tasks/new/page.tsx (TaskForm component, handle createTask submission, redirect to /dashboard on success, display validation errors from 422 responses)

### Testing User Story 1

- [ ] T032 [US1] Write backend test for create task happy path in backend/tests/test_tasks.py (authenticated POST, verify 201, verify user_id auto-assigned, verify timestamps set)
- [ ] T033 [US1] Write backend test for create task validation errors in backend/tests/test_tasks.py (empty title→422, title too long→422, invalid status→422)
- [ ] T034 [US1] Write backend test for create task without auth in backend/tests/test_tasks.py (no JWT→401)
- [ ] T035 [US1] Write backend test for list tasks happy path in backend/tests/test_tasks.py (authenticated GET, verify 200, verify only user's tasks returned, verify ordering by created_at DESC)
- [ ] T036 [US1] Write backend test for list tasks isolation in backend/tests/test_tasks.py (User A creates 2 tasks, User B creates 1 task, User A lists→2 tasks, User B lists→1 task)
- [ ] T037 [US1] Manual test: Create task from UI and verify it appears in dashboard list

**Checkpoint**: User Story 1 complete - Users can create tasks and see them listed. This is a functional MVP! 🎉

---

## Phase 4: User Story 2 - View and Update Tasks (Priority: P2)

**Goal**: Enable users to view task details and update task properties (title, description, status)

**Business Value**: Users can modify tasks as requirements change and mark progress

**Independent Test**:
1. User logs in → dashboard shows existing tasks (from US1)
2. User clicks on a task card → navigates to edit page → sees task details pre-populated
3. User updates title → saves → redirected to dashboard → sees updated title
4. User clicks task again → updates status to "in_progress" → saves → badge color changes to blue
5. User logs in with different account → attempts direct URL to first user's task edit page → receives 404

### Backend: Get Task (FR3)

- [X] T038 [P] [US2] Implement GET /api/tasks/{task_id} endpoint in backend/app/api/v1/tasks.py (extract user_id from JWT, query WHERE id=task_id AND user_id=user_id, return TaskResponse or 404)
- [X] T039 [P] [US2] Add error handling for get endpoint (401 for missing JWT, 404 for not found OR belongs to different user)

### Backend: Update Task (FR4)

- [X] T040 [P] [US2] Implement PUT /api/tasks/{task_id} endpoint in backend/app/api/v1/tasks.py (extract user_id from JWT, query task with isolation, partial update only provided fields, auto-update updated_at, return TaskResponse or 404)
- [X] T041 [P] [US2] Add input validation for update endpoint (title max 200 chars if provided, description max 2000 chars if provided, status enum validation if provided)
- [X] T042 [P] [US2] Add error handling for update endpoint (401 for missing JWT, 404 for not found OR cross-user, 422 for validation errors)

### Frontend: API Client

- [X] T043 [P] [US2] Implement getTask(id: number) function in frontend/lib/task-api.ts (GET /api/tasks/{id}, return Task, handle 404)
- [X] T044 [P] [US2] Implement updateTask(id: number, data: TaskUpdateRequest) function in frontend/lib/task-api.ts (PUT /api/tasks/{id}, return Task, handle 404 and 422)

### Frontend: Pages

- [X] T045 [US2] Create task edit page in frontend/app/tasks/[id]/page.tsx (fetch task with getTask, display TaskForm with pre-populated values, handle updateTask submission, redirect to /dashboard on success, handle 404 with error message, display validation errors from 422)

### Testing User Story 2

- [ ] T046 [US2] Write backend test for get task happy path in backend/tests/test_tasks.py (create task, authenticated GET with owner, verify 200 and task data)
- [ ] T047 [US2] Write backend test for get task cross-user isolation in backend/tests/test_tasks.py (User A creates task, User B attempts GET→404)
- [ ] T048 [US2] Write backend test for get task not found in backend/tests/test_tasks.py (GET non-existent id→404)
- [ ] T049 [US2] Write backend test for update task happy path in backend/tests/test_tasks.py (create task, authenticated PUT with partial data, verify 200, verify only provided fields updated, verify updated_at changed, verify created_at unchanged)
- [ ] T050 [US2] Write backend test for update task cross-user isolation in backend/tests/test_tasks.py (User A creates task, User B attempts PUT→404, verify User A's task unchanged)
- [ ] T051 [US2] Write backend test for update task validation errors in backend/tests/test_tasks.py (title too long→422, invalid status→422)
- [ ] T052 [US2] Manual test: Click task card, update title and status, verify changes persist

**Checkpoint**: User Story 2 complete - Users can view and update their tasks

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks they no longer need

**Business Value**: Users can remove completed or unwanted tasks to keep their list clean

**Independent Test**:
1. User logs in → dashboard shows existing tasks (from US1)
2. User clicks on a task → navigates to edit page
3. User clicks "Delete" button → confirmation dialog appears
4. User confirms deletion → task deleted → redirected to dashboard → task no longer in list
5. User attempts GET on deleted task ID → receives 404
6. User logs in with different account → attempts DELETE on first user's task → receives 404 (task still exists for original owner)

### Backend: Delete Task (FR5)

- [X] T053 [US3] Implement DELETE /api/tasks/{task_id} endpoint in backend/app/api/v1/tasks.py (extract user_id from JWT, query WHERE id=task_id AND user_id=user_id, delete if found, return 204 or 404)
- [X] T054 [US3] Add error handling for delete endpoint (401 for missing JWT, 404 for not found OR belongs to different user)

### Frontend: API Client

- [X] T055 [US3] Implement deleteTask(id: number) function in frontend/lib/task-api.ts (DELETE /api/tasks/{id}, return void on 204, handle 404)

### Frontend: Delete UI

- [X] T056 [US3] Add delete functionality to task edit page in frontend/app/tasks/[id]/page.tsx (delete button, confirmation dialog, handle deleteTask, redirect to /dashboard on success, handle 404)

### Testing User Story 3

- [ ] T057 [US3] Write backend test for delete task happy path in backend/tests/test_tasks.py (create task, authenticated DELETE, verify 204, verify subsequent GET returns 404)
- [ ] T058 [US3] Write backend test for delete task cross-user isolation in backend/tests/test_tasks.py (User A creates task, User B attempts DELETE→404, verify User A's task still exists)
- [ ] T059 [US3] Write backend test for delete task not found in backend/tests/test_tasks.py (DELETE non-existent id→404)
- [ ] T060 [US3] Write backend test for delete task idempotency in backend/tests/test_tasks.py (DELETE same task twice, both return 404 after first deletion)
- [ ] T061 [US3] Manual test: Delete task from UI and verify it's removed from list

**Checkpoint**: User Story 3 complete - Users can delete tasks

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

### User Data Isolation Verification (Cross-Cutting)

- [ ] T062 [P] Write comprehensive user isolation test suite in backend/tests/test_task_isolation.py (test all 5 endpoints with cross-user access attempts, verify all return 404, verify no data leakage)
- [ ] T063 [P] Add test for cascade delete in backend/tests/test_tasks.py (create user with tasks, delete user, verify all tasks deleted)

### Error Handling & Validation

- [ ] T064 [P] Add frontend error boundary in frontend/app/tasks/error.tsx (catch and display API errors gracefully)
- [ ] T065 [P] Improve validation error messages in frontend/components/tasks/TaskForm.tsx (map Pydantic error messages to user-friendly text)

### Performance & Optimization

- [ ] T066 [P] Verify database indexes exist in database/migrations/ (user_id index, composite user_id+created_at DESC index)
- [ ] T067 [P] Add loading states to all frontend pages (dashboard, create, edit) with skeleton UI or spinners

### Documentation

- [ ] T068 [P] Verify OpenAPI documentation auto-generated by FastAPI (access /docs endpoint, verify all 5 task endpoints documented with request/response schemas)
- [ ] T069 [P] Add JSDoc comments to frontend/lib/task-api.ts functions (describe parameters, return types, error handling)

### Final Validation

- [ ] T070 Run all backend tests in backend/tests/ and verify >80% coverage for task endpoints
- [ ] T071 Run quickstart.md validation (follow implementation guide steps, verify all code examples work)
- [ ] T072 Perform manual end-to-end testing (complete user flow: register→login→create task→list tasks→edit task→delete task→logout)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verify F001 readiness
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Can start immediately after Phase 2
- **User Story 2 (Phase 4)**: Depends on Foundational - Can run parallel with US1 (different files) but naturally builds on US1 functionality
- **User Story 3 (Phase 5)**: Depends on Foundational - Can run parallel with US1/US2 but naturally builds on their UI
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories - independently deliverable MVP
- **User Story 2 (P2)**: No hard dependencies on US1, but UI naturally extends edit page created in US1
- **User Story 3 (P3)**: No hard dependencies on US1/US2, but UI extends edit page

### Within Each User Story

**For US1 (Create and List)**:
1. Backend endpoints before frontend API client
2. API client before components
3. Components before pages
4. Core implementation before tests (write tests to verify, not TDD)

**For US2 (View and Update)**:
1. Backend endpoints before frontend API client
2. API client before pages
3. Core implementation before tests

**For US3 (Delete)**:
1. Backend endpoint before frontend API client
2. API client before UI changes
3. Core implementation before tests

### Parallel Opportunities

**Phase 2 (Foundational) - Parallelizable**:
- T004 (TaskStatus enum) ∥ T006-T009 (Pydantic schemas) ∥ T013-T017 (TypeScript types)
- T005 (Task model) must complete before T010 (router setup)
- Frontend types (T013-T017) can run fully parallel

**Within User Story 1**:
- T022-T023 (list endpoint) ∥ T019-T021 (create endpoint) - different operations
- T024-T025 (API client) ∥ T026-T027 (StatusBadge, TaskCard) - different files
- T032-T036 (all tests) can run parallel after implementation

**Across User Stories** (if team capacity allows):
- After Phase 2 completes: US1, US2, US3 can all start in parallel
- Backend tasks within each story can proceed independently
- Frontend tasks within each story can proceed independently

---

## Parallel Example: Foundational Phase

```bash
# Launch all parallelizable foundational tasks together:
Task T004: "Create TaskStatus enum in backend/app/models/task.py"
Task T006: "Create TaskCreateRequest Pydantic schema in backend/app/schemas/task.py"
Task T007: "Create TaskUpdateRequest Pydantic schema in backend/app/schemas/task.py"
Task T008: "Create TaskResponse Pydantic schema in backend/app/schemas/task.py"
Task T013: "Create TaskStatus type in frontend/types/task.ts"
Task T014: "Create Task interface in frontend/types/task.ts"
Task T015: "Create TaskCreateRequest interface in frontend/types/task.ts"
Task T016: "Create TaskUpdateRequest interface in frontend/types/task.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify F001) - 15 min
2. Complete Phase 2: Foundational (models, schemas, types) - 1.5 hours
3. Complete Phase 3: User Story 1 (create + list) - 3-4 hours
4. **STOP and VALIDATE**: Test US1 independently
5. Deploy/demo if ready → Users can create and list tasks! 🎉

**Total MVP Time**: ~6 hours

### Incremental Delivery

1. Foundation (Phase 1-2) → ~2 hours
2. Add US1 (create + list) → Test → Deploy (MVP!) → ~4 hours
3. Add US2 (view + update) → Test → Deploy → ~3 hours
4. Add US3 (delete) → Test → Deploy → ~2 hours
5. Polish (Phase 6) → Final validation → ~2 hours

**Total Complete Feature**: ~13 hours

### Parallel Team Strategy

With multiple developers after Phase 2:
- Developer A: US1 (create + list) - 4 hours
- Developer B: US2 (view + update) - 3 hours
- Developer C: US3 (delete) - 2 hours
- Integrate all: Polish phase together - 2 hours

**Total Parallel Time**: ~9 hours (with 3 developers)

---

## Task Statistics

- **Total Tasks**: 72
- **Setup Tasks**: 3 (Phase 1)
- **Foundational Tasks**: 15 (Phase 2)
- **User Story 1 Tasks**: 19 (Phase 3)
- **User Story 2 Tasks**: 15 (Phase 4)
- **User Story 3 Tasks**: 9 (Phase 5)
- **Polish Tasks**: 11 (Phase 6)

**Parallel Tasks**: 28 tasks marked [P] can run in parallel within their phase
**Independent Stories**: 3 user stories can be delivered independently

---

## Notes

- [P] = Parallelizable (different files, no sequential dependencies)
- [US1/US2/US3] = User story label for traceability
- Each user story is independently completable and testable
- Stop at any checkpoint to validate story independently
- Commit after each task or logical group
- User isolation testing is CRITICAL - must verify all endpoints return 404 for cross-user access
- All validation must be enforced on backend (frontend validation is UX only)
- Follow explicit WHERE clause pattern from research.md for all queries

---

**Tasks Status**: Complete - Ready for /sp.implement
**Total Estimated Time**: 13 hours (sequential) or 9 hours (parallel with 3 developers)
**MVP Delivery**: 6 hours for User Story 1 only
**Author**: Claude Sonnet 4.5
**Date**: 2025-12-31
