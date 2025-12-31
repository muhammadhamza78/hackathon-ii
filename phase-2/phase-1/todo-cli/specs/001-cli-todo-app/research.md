# Research Notes: CLI Todo Application

**Feature**: 001-cli-todo-app
**Date**: 2025-12-28
**Researcher**: Planning Agent

## Library Evaluation

### Keyboard Navigation Libraries

**Requirement**: Cross-platform arrow key navigation with minimal complexity for beginner-friendly codebase.

#### Option 1: curses (Standard Library)

**Pros**:
- Standard library (no external dependency)
- Mature and well-documented
- Full terminal control

**Cons**:
- Windows support requires `windows-curses` package (defeats "standard library" benefit)
- Complex API for simple use cases
- Steep learning curve for beginners
- Overkill for menu navigation

**Verdict**: ❌ Rejected - Windows dependency issue

---

#### Option 2: blessed

**Pros**:
- Cross-platform (Windows + Linux) out of box
- Simple, beginner-friendly API
- `term.inkey()` for keyboard input is intuitive
- Good documentation with examples
- Lightweight (~50KB)
- Active maintenance (last release: 2023)

**Cons**:
- Requires external package (acceptable per constitution)
- Less control than curses (not needed for our use case)

**Verdict**: ✅ **SELECTED** - Best fit for requirements

**Example Code**:
```python
from blessed import Terminal

term = Terminal()

with term.fullscreen(), term.cbreak():
    key = term.inkey()
    if key.name == 'KEY_UP':
        # Handle up arrow
    elif key.name == 'KEY_DOWN':
        # Handle down arrow
    elif key.name == 'KEY_ENTER':
        # Handle enter
```

---

#### Option 3: prompt-toolkit

**Pros**:
- Powerful features (auto-completion, syntax highlighting)
- Cross-platform
- Well-maintained

**Cons**:
- Heavy (~1MB)
- Async-based architecture (complex for beginners)
- Overkill for simple menu navigation
- Steeper learning curve

**Verdict**: ❌ Rejected - Too complex

---

#### Option 4: rich

**Pros**:
- Beautiful terminal rendering
- Modern API
- Good for displaying formatted output

**Cons**:
- Focused on rendering, not input handling
- Would need to combine with another library for keyboard input
- Heavier than blessed

**Verdict**: ❌ Rejected - Not designed for keyboard navigation

---

### Decision: blessed

**Rationale**:
- Simplest API for arrow key input
- Cross-platform without extra packages
- Beginner-friendly (aligns with constitution)
- Minimal dependency footprint
- Active community support

**Installation**: `pip install blessed`

---

## JSON File Structure

### Single File vs Multiple Files

**User Suggestion**: Separate `tasks.json` and `drafts.json`

**Constitution Requirement**: "MUST use a single data file: `todos.json`"

#### Option 1: Two Files

```
tasks.json:   [{"id": "...", ...}, ...]
drafts.json:  [{"id": "...", ...}, ...]
```

**Pros**:
- Logical separation
- Smaller individual files

**Cons**:
- Violates constitution (single file requirement)
- Atomic write complexity (must update both or neither)
- Risk of inconsistency (one file corrupted, other fine)
- Two backup files to manage

---

#### Option 2: Single File with Two Arrays

```json
{
  "saved": [{"id": "...", ...}, ...],
  "drafts": [{"id": "...", ...}, ...]
}
```

**Pros**:
- Adheres to constitution
- Atomic writes (one file = consistent state)
- Single backup point
- Simpler code (one load/save function)

**Cons**:
- Slightly larger file (negligible)

---

### Decision: Single File (todos.json)

**Rationale**:
- Constitution compliance (Principle V)
- Atomic write operations ensure consistency
- Simpler backup and recovery
- Easier to maintain referential integrity
- Moving task from draft to saved is status change (not file operation)

---

## Task ID Generation

### Options Evaluated

#### Option 1: Sequential Integers (1, 2, 3, ...)

**Pros**:
- Human-readable
- Compact storage

**Cons**:
- Need to track counter
- Counter state must persist
- Collision risk if counter resets
- Not future-proof (import/export scenarios)

---

#### Option 2: Timestamps (Epoch Milliseconds)

**Pros**:
- Auto-generated
- Sortable
- No counter needed

**Cons**:
- Collision risk (two tasks created in same millisecond)
- Not truly unique

---

#### Option 3: UUID4 (Random UUIDs)

**Pros**:
- Globally unique (no collision risk)
- Standard library support (`uuid.uuid4()`)
- No counter management
- Future-proof

**Cons**:
- Less human-readable (acceptable - users don't see IDs)
- Larger storage (36 chars) - negligible impact

---

### Decision: UUID4

**Rationale**:
- Zero collision risk (critical for data integrity)
- Standard library (`import uuid`)
- No state to manage
- Future-proof for import/export features
- IDs are internal (users don't interact with them)

**Implementation**:
```python
import uuid

task_id = str(uuid.uuid4())
# Example: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

---

## Terminal Encoding and Unicode Support

### Unicode Emoji in Different Terminals

**Requirement**: Icons must render properly: ➕ 🔄 🗑️ 📋 ⏳ 📄 🔙 ✔

#### Windows Terminal
- ✅ UTF-8 by default
- ✅ Full emoji support
- **Status**: Fully supported

#### PowerShell (5.x)
- ⚠️ Default encoding may be UTF-16
- ✅ Can set UTF-8: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- **Status**: Supported with encoding config

#### CMD (Command Prompt)
- ⚠️ Default code page may be CP437 or CP850
- ✅ Switch to UTF-8: `chcp 65001`
- **Status**: Supported with chcp command

#### bash / zsh (Linux)
- ✅ UTF-8 default on modern distros
- ✅ Full emoji support
- **Status**: Fully supported

---

### blessed Encoding Handling

`blessed` automatically detects terminal capabilities and handles encoding:
- Queries terminal for Unicode support
- Falls back to ASCII if needed
- Handles different encoding schemes transparently

**Recommendation**: Trust `blessed` automatic handling, document encoding requirements in README.

---

## Atomic File Write Strategy

### Problem
Risk of data corruption if app crashes during write.

### Solution: Atomic Write with Backup

```python
def save_data(data: dict) -> bool:
    """Atomically save data with backup."""
    # Step 1: Write to temporary file
    with open('todos.json.tmp', 'w') as f:
        json.dump(data, f, indent=2)

    # Step 2: Create backup of current file
    if os.path.exists('todos.json'):
        os.replace('todos.json', 'todos.json.bak')

    # Step 3: Rename temp to actual (atomic on POSIX, near-atomic on Windows)
    os.replace('todos.json.tmp', 'todos.json')

    return True
```

**Benefits**:
- If crash during step 1: `todos.json` untouched
- If crash during step 2: `todos.json.bak` available
- `os.replace()` is atomic on POSIX, near-atomic on Windows
- Always have recoverable state

---

## Error Handling Strategy

### Layered Error Approach

**Layer 1: Storage** (Low-level errors)
- `FileNotFoundError`: Create default file
- `JSONDecodeError`: Backup corrupted file, start fresh
- `PermissionError`: Display clear message to user

**Layer 2: Handlers** (Business logic errors)
- Validation errors (empty title, etc.)
- Not found errors (task doesn't exist)

**Layer 3: UI** (User-facing messages)
- Never show stack traces
- Actionable error messages
- "Press any key to retry" options

### Example Error Messages

| Error Type | User Message |
|------------|--------------|
| Empty title | "Title cannot be empty. Press Enter to retry or Escape to cancel." |
| File write fail | "Cannot save to todos.json. Check folder permissions." |
| Corrupted JSON | "Data file corrupted. Backup saved to todos.json.bak. Starting fresh." |
| No tasks found | "No tasks yet. Select 'Add new task ➕' to create one." |

---

## Performance Considerations

### Expected Load
- Typical user: 10-100 tasks
- Power user: 100-1000 tasks
- Stress test: 10,000 tasks

### Performance Analysis

**JSON Load/Save**:
- 1000 tasks ≈ 100KB file
- Load time: <50ms
- Save time: <100ms
- **Acceptable**: Well under 2s startup goal

**Linear Search** (finding task by ID):
- O(n) where n = number of tasks
- For 1000 tasks: ~1000 comparisons
- Python string comparison: ~1µs each
- Total: ~1ms
- **Acceptable**: No indexing needed

**Memory**:
- 1000 tasks in memory: ~200KB
- **Acceptable**: Well under 200MB constraint

**Conclusion**: No optimization needed for initial version. Add pagination only if users report issues with >1000 tasks.

---

## References

- blessed documentation: https://blessed.readthedocs.io/
- Python UUID module: https://docs.python.org/3/library/uuid.html
- JSON Schema: https://json-schema.org/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- os.replace() documentation: https://docs.python.org/3/library/os.html#os.replace
