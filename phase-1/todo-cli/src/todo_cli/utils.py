from typing import List
from .task import Task


def format_task_table(tasks: List[Task]) -> str:
    """Format tasks as a beautiful table."""
    if not tasks:
        return "No tasks found."
    
    lines = []
    lines.append("")
    lines.append("ID │ STATUS │ TASK")
    lines.append("───┼────────┼" + "─" * 50)
    
    for task in tasks:
        status = "✓" if task.completed else "○"
        lines.append(f"{task.id:<2} │ {status:^6} │ {task.description}")
    
    lines.append("")
    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed
    lines.append(f"{completed}/{len(tasks)} completed")
    
    return "\n".join(lines)