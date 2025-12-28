---
id: 003
title: CLI Todo App Implementation Plan
stage: plan
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 001-cli-todo-app
branch: master
user: DELL
command: /sp.plan
labels: ["planning", "architecture", "cli-todo-app", "blessed", "json-storage"]
links:
  spec: specs/001-cli-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo-app/plan.md
  - specs/001-cli-todo-app/data-model.md
  - specs/001-cli-todo-app/research.md
  - specs/001-cli-todo-app/quickstart.md
  - specs/001-cli-todo-app/contracts/task-schema.json
tests:
  - Manual testing checklist defined in plan.md
---

## Prompt

/sp.plan
Step-by-step plan:

1. Use Python for CLI app
2. Use a library for arrow-key navigation (e.g. curses or prompt-toolkit)
3. Create data files:
   - tasks.json (saved tasks)
   - drafts.json (draft tasks)
4. Define Task structure:
   - id
   - title
   - description
   - completed (true/false)
5. Build main menu loop with arrow navigation
6. Implement handlers:
   - add_task()
   - update_task()
   - delete_task()
   - show_all_tasks()
   - show_pending_tasks()
   - show_drafts()
7. Ensure smooth back navigation after every action
8. Handle empty states gracefully (no task found)
9. Keep code modular and readable

## Response snapshot

Created comprehensive implementation plan with Phase 0 (Research), Phase 1 (Design), Phase 2 (Architecture Decisions), and Phase 3 (Implementation Roadmap).

**Key Technical Decisions**:

1. **Keyboard Navigation Library**: Selected `blessed` over curses/prompt-toolkit
   - Cross-platform (Windows + Linux) without extra packages
   - Simple API (`term.inkey()`) - beginner-friendly
   - Lightweight and well-documented
   - Aligns with constitution: minimal dependencies, beginner-friendly code

2. **JSON File Structure**: Single file `todos.json` (not separate files as suggested)
   - Constitution Principle V: "MUST use a single data file"
   - Atomic writes prevent inconsistency
   - Simpler backup/recovery
   - Format: `{"saved": [...], "drafts": [...]}`

3. **Task ID Strategy**: UUID4 (not sequential integers or timestamps)
   - Zero collision risk
   - Standard library support
   - No state management needed
   - Future-proof for import/export

4. **Error Handling**: Layered approach with user-friendly messages
   - Storage layer: Low-level errors
   - Handler layer: Validation errors
   - UI layer: No stack traces, actionable messages

**Project Structure**:
```
src/
├── main.py              # Entry point, main loop
├── models/task.py       # Task dataclass, TaskList
├── storage/json_storage.py  # JSON I/O, validation
├── ui/                  # Menu, forms, display
└── handlers/            # Feature handlers
```

**Artifacts Created**:
- plan.md: Full implementation plan with phases, decisions, roadmap
- data-model.md: Task entity, TaskList operations, JSON schema
- research.md: Library evaluation, performance analysis
- quickstart.md: User guide for installation and usage
- contracts/task-schema.json: JSON Schema validation

**Constitution Compliance**: ✅ 7/7 principles validated
- CLI-only, keyboard-driven, Unicode icons, beginner-friendly code, JSON storage, draft/saved states, continuous loop

**Performance Goals**: <2s startup, <1s transitions, handles 1000+ tasks

## Outcome

- ✅ Impact: Complete architectural plan ready for `/sp.tasks` task generation
- 🧪 Tests: Manual testing checklist defined with 12 test cases + platform testing
- 📁 Files: Created plan.md, data-model.md, research.md, quickstart.md, task-schema.json
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Successfully balanced user suggestions (separate JSON files) with constitution requirements (single file), providing clear rationale. Architectural decisions documented with trade-offs and consequences.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (7/7 principles), Complexity tracking PASS (no violations)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): During `/sp.tasks`, validate that task breakdown follows user story prioritization (P1 MVP first)
