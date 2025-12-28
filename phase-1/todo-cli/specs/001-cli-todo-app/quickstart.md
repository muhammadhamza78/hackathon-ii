# Quickstart Guide: CLI Todo Application

**Version**: 1.0.0
**Last Updated**: 2025-12-28

## Prerequisites

- Python 3.10 or higher installed
- Terminal with UTF-8 encoding support
- Write permissions in application directory

## Installation

### Step 1: Clone or Download

```bash
cd /path/to/todo-app
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `blessed` - Terminal UI library for keyboard navigation

### Step 3: Verify Installation

```bash
python --version  # Should show 3.10 or higher
pip show blessed   # Should show blessed 1.20.0 or similar
```

## Running the Application

### Launch

```bash
python src/main.py
```

### First Launch

On first run, the app will:
1. Create `todos.json` file in the application directory
2. Display the main menu with 7 options

## Basic Usage

### Creating Your First Task

1. **Launch app**: `python src/main.py`
2. **Navigate**: Press **↓** arrow to highlight "Add new task ➕"
3. **Select**: Press **Enter**
4. **Enter title**: Type task title (e.g., "Buy groceries"), press **Enter**
5. **Enter description**: Type description or press **Enter** to skip
6. **Save**: Navigate to "Save Task" and press **Enter**
7. **Done**: You're back at the main menu

### Viewing Tasks

1. From main menu, navigate to "Show all task 📋"
2. Press **Enter**
3. See your tasks with checkboxes: `[ ] Buy groceries`
4. Press **q** or **Escape** to return to main menu

### Marking Tasks Complete

1. Navigate to "Show all task 📋" and press **Enter**
2. Use **↑** / **↓** to select a task
3. Press **Enter** to toggle checkbox: `[ ]` → `[✔]`
4. Press **Enter** again to unmark: `[✔]` → `[ ]`
5. Press **q** to return to main menu

### Viewing Only Pending Tasks

1. Navigate to "Show pending task ⏳" and press **Enter**
2. See only incomplete tasks (unchecked)
3. Press **q** to return to main menu

### Updating a Task

1. Navigate to "Update previous task 🔄" and press **Enter**
2. Select task with **↑** / **↓**, press **Enter**
3. Edit title (or keep existing), press **Enter**
4. Edit description (or keep existing), press **Enter**
5. Navigate to "Save Task" and press **Enter**

### Deleting a Task

1. Navigate to "Delete previous task 🗑️" and press **Enter**
2. Select task with **↑** / **↓**, press **Enter**
3. Confirm deletion when prompted
4. Task is permanently removed

### Using Drafts

**Saving as Draft**:
1. When creating/editing a task, select "Save as Draft" instead of "Save Task"
2. Task is saved but not added to main list

**Viewing Drafts**:
1. Navigate to "Draft 📄" and press **Enter**
2. See all draft tasks

**Converting Draft to Saved**:
1. Select "Update previous task 🔄"
2. Select a draft task
3. Edit if needed
4. Choose "Save Task" (moves from draft to saved)

### Exiting the Application

1. Navigate to "Exit 🔙" and press **Enter**
2. Or press **Ctrl+C** anytime (app saves automatically before exiting)

## Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| **↑** | Move selection up |
| **↓** | Move selection down |
| **Enter** | Confirm selection / Toggle checkbox |
| **Escape** or **q** | Go back to main menu |
| **Ctrl+C** | Exit application (saves data) |

## Menu Structure

```
Main Menu
├── 1. Add new task ➕
│   ├── Enter title (required)
│   ├── Enter description (optional)
│   └── Choose: Save Task | Save as Draft
│
├── 2. Update previous task 🔄
│   ├── Select task
│   ├── Edit title
│   ├── Edit description
│   └── Choose: Save Task | Save as Draft
│
├── 3. Delete previous task 🗑️
│   ├── Select task
│   └── Confirm deletion
│
├── 4. Show all task 📋
│   └── View tasks with checkboxes (Enter to toggle)
│
├── 5. Show pending task ⏳
│   └── View only incomplete tasks
│
├── 6. Draft 📄
│   └── View draft tasks
│
└── 7. Exit 🔙
    └── Save and quit
```

## Data Storage

### Location
- **File**: `todos.json` (in application directory)
- **Format**: Human-readable JSON

### Structure
```json
{
  "saved": [
    {
      "id": "uuid-here",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "status": "saved",
      "created_at": "2025-12-28T10:30:45.123456",
      "updated_at": "2025-12-28T10:30:45.123456"
    }
  ],
  "drafts": []
}
```

### Backup
- Automatic backup created on each save: `todos.json.bak`
- If `todos.json` is corrupted, app restores from `.bak` or creates fresh file

## Troubleshooting

### Icons Not Displaying

**Problem**: Menu shows boxes or question marks instead of emoji

**Solution**:
- **Windows CMD**: Run `chcp 65001` before launching app
- **PowerShell**: Add to profile: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- **Windows Terminal**: UTF-8 by default, should work out of box
- **Linux**: Ensure `$LANG` is set to UTF-8 (e.g., `en_US.UTF-8`)

### Permission Errors

**Problem**: "Cannot write to todos.json"

**Solution**:
- Check folder permissions: `ls -la` (Linux) or folder properties (Windows)
- Run from home directory where you have write access
- Or run with elevated permissions (not recommended)

### Corrupted Data File

**Problem**: "Data file corrupted" message on startup

**Solution**:
- App automatically creates backup: `todos.json.bak`
- Check backup file manually
- If backup is good, rename it to `todos.json`
- If backup is also corrupted, app creates fresh file (data lost)

### App Freezes or Unresponsive

**Solution**:
- Press **Ctrl+C** to force exit (data is saved before exit)
- Restart app
- If problem persists, check terminal compatibility

### Missing Dependencies

**Problem**: `ModuleNotFoundError: No module named 'blessed'`

**Solution**:
```bash
pip install blessed
# Or reinstall from requirements:
pip install -r requirements.txt
```

## Tips and Best Practices

1. **Save Often**: App saves to disk on every operation, but use Exit properly
2. **Use Drafts**: Start tasks as drafts if you're not sure about details
3. **Regular Backups**: Copy `todos.json` to another location periodically
4. **Empty Title Validation**: Title is required - app will prevent empty titles
5. **Unicode Support**: Works best in modern terminals (Windows Terminal, iTerm2, etc.)

## Example Workflow

### Daily Task Management

```
Morning:
1. Launch app
2. Add new tasks for the day (use drafts for uncertain ones)
3. Review "Show pending task" to see what's left from yesterday

During Day:
1. Complete tasks: "Show all task" → select → Enter (mark complete)
2. Add tasks as they come up
3. Update tasks if requirements change

Evening:
1. "Show pending task" - review what's left
2. Move unfinished tasks to tomorrow (or delete if no longer relevant)
3. Exit app
```

## Next Steps

- Explore all menu options
- Try creating, updating, and deleting tasks
- Experiment with drafts
- Review "Show pending task" to filter incomplete items

## Getting Help

- Check this quickstart guide
- Review `README.md` for detailed documentation
- Check constitution at `.specify/memory/constitution.md` for design principles
- Check spec at `specs/001-cli-todo-app/spec.md` for feature details

## Version History

- **1.0.0** (2025-12-28): Initial release
  - Basic CRUD operations
  - Completion tracking
  - Draft support
  - Keyboard navigation
