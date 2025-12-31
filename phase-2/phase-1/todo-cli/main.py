from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog, message_dialog
from prompt_toolkit.styles import Style
import json
import os
import uuid

TASK_FILE = "tasks.json"
DRAFT_FILE = "drafts.json"

# ---------- Style ----------
style = Style.from_dict({
    "dialog": "bg:#000000",
    "dialog frame.label": "fg:#ffaf00 bold",
    "radiolist": "fg:#ffffff",
    "checkbox": "fg:#00ff00",
})

# ---------- Utils ----------
def load_data(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Core ----------
def add_task():
    title = prompt("Title: ").strip()
    if not title:
        message_dialog(title="Error", text="Title required!", style=style).run()
        return
    description = prompt("Description (optional): ").strip()
    choice = radiolist_dialog(
        title="Save Option",
        text="Choose action",
        values=[("save", "💾 Save Task"), ("draft", "📄 Save as Draft")],
        style=style
    ).run()
    if choice is None:
        return
    task = {"id": str(uuid.uuid4()), "title": title, "description": description, "completed": False}
    if choice == "save":
        tasks = load_data(TASK_FILE)
        tasks.append(task)
        save_data(TASK_FILE, tasks)
    elif choice == "draft":
        drafts = load_data(DRAFT_FILE)
        drafts.append(task)
        save_data(DRAFT_FILE, drafts)

def update_task():
    tasks = load_data(TASK_FILE)
    if not tasks:
        message_dialog(title="Info", text="No tasks found", style=style).run()
        return
    selected = radiolist_dialog(
        title="Update Task",
        text="Select task",
        values=[(t["id"], t["title"]) for t in tasks],
        style=style
    ).run()
    if selected is None:
        return
    task = next((t for t in tasks if t["id"] == selected), None)
    if not task:
        message_dialog(title="Error", text="Task not found!", style=style).run()
        return
    new_title = prompt(f"New title [{task['title']}]: ").strip()
    new_desc = prompt(f"New description [{task['description']}]: ").strip()
    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc
    save_data(TASK_FILE, tasks)

def delete_task():
    tasks = load_data(TASK_FILE)
    if not tasks:
        message_dialog(title="Info", text="No tasks to delete", style=style).run()
        return
    selected = radiolist_dialog(
        title="Delete Task",
        text="Select task",
        values=[(t["id"], t["title"]) for t in tasks],
        style=style
    ).run()
    if selected:
        tasks = [t for t in tasks if t["id"] != selected]
        save_data(TASK_FILE, tasks)

def show_all_tasks():
    tasks = load_data(TASK_FILE)
    if not tasks:
        message_dialog(title="Info", text="No tasks", style=style).run()
        return
    values = [(t["id"], f"{'[x]' if t.get('completed') else '[ ]'} {t['title']}") for t in tasks]
    selected = checkboxlist_dialog(
        title="All Tasks",
        text="✔ Mark completed/uncompleted",
        values=values,
        style=style
    ).run()
    if selected is None:
        return
    for t in tasks:
        t["completed"] = t["id"] in selected
    save_data(TASK_FILE, tasks)

def show_pending():
    tasks = load_data(TASK_FILE)
    pending = [t for t in tasks if not t.get("completed")]
    if not pending:
        message_dialog(title="Pending", text="No pending tasks", style=style).run()
        return
    message_dialog(title="Pending Tasks", text="\n".join(f"⏳ {t['title']}" for t in pending), style=style).run()

def show_drafts():
    drafts = load_data(DRAFT_FILE)
    if not drafts:
        message_dialog(title="Drafts", text="No drafts", style=style).run()
        return
    selected = radiolist_dialog(
        title="Drafts",
        text="Select draft",
        values=[(d["id"], d["title"]) for d in drafts],
        style=style
    ).run()
    if not selected:
        return
    draft = next((d for d in drafts if d["id"] == selected), None)
    if not draft:
        message_dialog(title="Error", text="Draft not found!", style=style).run()
        return
    action = radiolist_dialog(
        title="Draft Action",
        text="What to do?",
        values=[("save", "💾 Save to Tasks"), ("delete", "🗑️ Delete Draft")],
        style=style
    ).run()
    if action == "save":
        tasks = load_data(TASK_FILE)
        tasks.append(draft)
        save_data(TASK_FILE, tasks)
    drafts = [d for d in drafts if d["id"] != selected]
    save_data(DRAFT_FILE, drafts)

# ---------- Main Menu ----------
def main_menu():
    while True:
        choice = radiolist_dialog(
            title="Select Option",
            text="Use ↑ ↓ keys and Enter",
            values=[
                ("add", "➕ Add new task"),
                ("update", "🔄 Update previous task"),
                ("delete", "🗑️ Delete previous task"),
                ("all", "📋 Show all tasks"),
                ("pending", "⏳ Show pending tasks"),
                ("draft", "📄 Drafts"),
                ("exit", "🔙 Exit"),
            ],
            style=style
        ).run()
        if choice == "add":
            add_task()
        elif choice == "update":
            update_task()
        elif choice == "delete":
            delete_task()
        elif choice == "all":
            show_all_tasks()
        elif choice == "pending":
            show_pending()
        elif choice == "draft":
            show_drafts()
        elif choice == "exit" or choice is None:
            break

if __name__ == "__main__":
    main_menu()
