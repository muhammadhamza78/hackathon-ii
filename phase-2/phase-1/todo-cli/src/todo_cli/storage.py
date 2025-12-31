import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from .task import Task


class TaskStorage:
    """File-based storage for tasks."""
    
    def __init__(self, storage_file: str = None):
        if storage_file is None:
            # Default storage location in user's home directory
            home = Path.home()
            self.storage_file = home / ".todo-cli" / "tasks.json"
        else:
            self.storage_file = Path(storage_file)
        
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from file."""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._next_id = data.get('next_id', 1)
                    
                    for task_data in data.get('tasks', []):
                        task = Task(
                            id=task_data['id'],
                            description=task_data['description'],
                            completed=task_data['completed'],
                            created_at=datetime.fromisoformat(task_data['created_at']),
                            completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data.get('completed_at') else None
                        )
                        self._tasks[task.id] = task
            except Exception as e:
                print(f"Warning: Could not load tasks: {e}")
    
    def _save_tasks(self):
        """Save tasks to file."""
        # Ensure directory exists
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'next_id': self._next_id,
            'tasks': [
                {
                    'id': task.id,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat(),
                    'completed_at': task.completed_at.isoformat() if task.completed_at else None
                }
                for task in self._tasks.values()
            ]
        }
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_task(self, description: str) -> Task:
        """Add a new task."""
        task = Task(
            id=self._next_id,
            description=description,
            created_at=datetime.now()
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        self._save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self._tasks.values())
    
    def update_task(self, task_id: int, description: str) -> bool:
        """Update task description."""
        task = self._tasks.get(task_id)
        if task:
            task.description = description
            self._save_tasks()
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save_tasks()
            return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed."""
        task = self._tasks.get(task_id)
        if task:
            task.completed = True
            task.completed_at = datetime.now()
            self._save_tasks()
            return True
        return False