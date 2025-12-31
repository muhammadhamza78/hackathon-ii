<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0 (Initial ratification)
Modified principles: All principles newly defined
Added sections: Core Principles (7), User Experience Standards, Development Standards, Governance
Removed sections: None (initial version)
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section aligns with principles
  ✅ spec-template.md - User scenarios align with UX principles
  ✅ tasks-template.md - Task structure supports incremental delivery
Follow-up TODOs: None
-->

# CLI Todo Application Constitution

## Core Principles

### I. CLI-Only Interface (NON-NEGOTIABLE)

The application MUST be 100% command-line interface based with zero graphical or web components.

**Rules**:
- No GUI frameworks (no Tkinter, PyQt, web browsers, etc.)
- No web servers or HTTP endpoints
- Terminal-based interaction only using stdin/stdout
- MUST support standard terminal emulators (Windows Terminal, CMD, PowerShell, bash, zsh)

**Rationale**: Ensures simplicity, portability, and focused scope. CLI applications are lightweight, scriptable, and universally accessible across platforms without dependencies on display servers or browsers.

### II. Keyboard-Driven Navigation (NON-NEGOTIABLE)

All user interaction MUST use keyboard controls; mouse interaction is forbidden.

**Rules**:
- Arrow keys (↑ ↓) MUST provide menu navigation
- Enter key MUST confirm selection
- Escape or 'q' MUST provide back/cancel functionality
- Tab key MAY be used for field navigation in forms
- No mouse clicks, hover events, or pointer-based interaction

**Rationale**: Keyboard-only navigation ensures accessibility, speed, and consistency with CLI conventions. Power users can navigate efficiently without context switching to mouse.

### III. Unicode Icons and Visual Clarity

CLI menus MUST render properly with Unicode icons (emoji) for visual appeal and usability.

**Rules**:
- Use Unicode emoji for visual categorization (e.g., ✅ for completed, 📝 for draft, ➕ for add)
- MUST test rendering in target terminal environments (Windows Terminal, bash)
- Icons MUST be optional fallback if terminal doesn't support Unicode
- Text MUST remain readable even if icons fail to render
- Use box-drawing characters (─ ┌ └ │) for borders and structure where appropriate

**Rationale**: Modern terminals support Unicode. Visual icons improve scannability and user experience in text-based interfaces without requiring graphics.

### IV. Code Quality: Clean and Beginner-Friendly

Code MUST be readable, well-structured, and accessible to beginner Python developers.

**Rules**:
- Use clear variable names (no cryptic abbreviations)
- Functions MUST be single-purpose with clear names
- MUST include docstrings for all public functions and classes
- MUST follow PEP 8 style guidelines
- Avoid over-engineering: no unnecessary abstractions, design patterns, or frameworks
- Maximum function length: 50 lines (refactor if longer)
- Maximum file length: 300 lines (split into modules if longer)

**Rationale**: Beginner-friendly code enables learning, maintenance, and contributions. Simplicity reduces bugs and cognitive load.

### V. Local JSON Storage (NON-NEGOTIABLE)

All application data MUST persist to local JSON files; no databases or external services.

**Rules**:
- Data MUST be stored in human-readable JSON format
- MUST use a single data file: `todos.json` in application directory or user home
- File MUST be created automatically if it doesn't exist
- MUST handle file I/O errors gracefully (inform user, don't crash)
- MUST validate JSON structure on load (recover or reset if corrupted)
- No SQLite, PostgreSQL, MongoDB, or any database system

**Rationale**: JSON is human-readable, debuggable, portable, and requires no external dependencies. Users can inspect, backup, and edit data directly if needed.

### VI. Draft and Saved Task States

Tasks MUST maintain two distinct states: Draft and Saved.

**Rules**:
- Draft tasks: In-progress, editable, not yet committed
- Saved tasks: Confirmed, persistent, displayed in main list
- Users MUST explicitly save drafts to transition to saved state
- Optional field: Description (can be empty/skipped)
- MUST distinguish draft from saved in UI (visual indicator or separate view)
- Saved tasks MUST persist across application restarts
- Draft tasks MAY be discarded without saving

**Rationale**: Draft state enables incremental task creation without committing incomplete or incorrect entries. Separates work-in-progress from confirmed tasks.

### VII. Continuous Loop Until Exit

Application MUST run in a persistent loop until user explicitly exits.

**Rules**:
- MUST display main menu after each action completes
- MUST provide clear "Exit" option in main menu
- Application MUST NOT terminate automatically after single action
- MUST handle Ctrl+C gracefully (save state and exit cleanly)
- Exit MUST be user-initiated only

**Rationale**: Continuous operation matches user expectations for interactive CLI applications. Avoids need to repeatedly launch app for multiple operations.

## User Experience Standards

### Navigation Flow
- Main menu → Action → Result/Confirmation → Main menu (loop)
- Clear visual hierarchy: menus, selections, confirmations
- Consistent key bindings across all screens

### Error Handling
- MUST validate all user input before processing
- MUST display clear error messages (not stack traces to end users)
- MUST offer retry or return to menu on error
- MUST never crash on invalid input

### Feedback and Confirmation
- MUST confirm destructive actions (delete, clear all)
- MUST show success messages after operations
- MUST indicate current state clearly (e.g., "Draft mode", "Viewing saved tasks")

## Development Standards

### Python Version
- Minimum: Python 3.8
- Target: Python 3.10+
- MUST specify version in README and requirements

### Dependencies
- Prefer standard library over external packages
- Allowed: `click` or `typer` for CLI framework (optional), `rich` or `blessed` for advanced terminal UI (optional)
- MUST minimize dependency count (ideal: zero external deps)
- MUST document all dependencies in requirements.txt

### Testing
- Unit tests encouraged but NOT mandatory for initial version
- Manual testing checklist MUST be provided in README
- MUST test on Windows and Linux terminals before release

### Documentation
- README MUST include: Installation, Usage, Features, Keyboard shortcuts
- Code comments for non-obvious logic
- No external documentation files unless necessary

## Governance

### Amendment Process
1. Propose change with rationale and impact assessment
2. Update constitution version (semantic versioning)
3. Propagate changes to templates and dependent artifacts
4. Document decision in ADR if architecturally significant

### Versioning Policy
- MAJOR: Breaking changes to core principles (e.g., removing CLI-only requirement)
- MINOR: New principles or standards added
- PATCH: Clarifications, wording improvements, typo fixes

### Compliance
- All code MUST adhere to these principles
- PRs MUST verify compliance before merge
- Complexity MUST be justified explicitly if principles are violated

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
