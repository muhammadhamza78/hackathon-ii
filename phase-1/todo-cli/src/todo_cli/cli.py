import click
from .storage import TaskStorage
from .utils import format_task_table
from .interactive import interactive as interactive_mode


# Global storage instance
_storage = None


def get_storage():
    """Get or create the global storage instance."""
    global _storage
    if _storage is None:
        _storage = TaskStorage()
    return _storage


@click.group()
@click.version_option(version='1.0.0')
def todo():
    """✨ Beautiful Todo CLI - Manage your tasks with style!"""
    pass


@todo.command()
@click.argument('description')
def add(description):
    """➕ Add a new task"""
    storage = get_storage()
    task = storage.add_task(description)
    click.secho(f"✓ Task created: [{task.id}] {task.description}", fg='green')


@todo.command()
@click.option('--completed', is_flag=True, help='Show only completed tasks')
@click.option('--pending', is_flag=True, help='Show only pending tasks')
def list(completed, pending):
    """📋 List all tasks"""
    storage = get_storage()
    tasks = storage.get_all_tasks()
    
    if completed:
        tasks = [t for t in tasks if t.completed]
    elif pending:
        tasks = [t for t in tasks if not t.completed]
    
    click.echo(format_task_table(tasks))


@todo.command()
@click.argument('task_id', type=int)
@click.argument('description')
def update(task_id, description):
    """✏️  Update a task"""
    storage = get_storage()
    if storage.update_task(task_id, description):
        click.secho(f"✓ Task updated: [{task_id}] {description}", fg='green')
    else:
        click.secho(f"✗ Task not found: ID {task_id}", fg='red')


@todo.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """🗑️  Delete a task"""
    storage = get_storage()
    if storage.delete_task(task_id):
        click.secho(f"✓ Task deleted: ID {task_id}", fg='green')
    else:
        click.secho(f"✗ Task not found: ID {task_id}", fg='red')


@todo.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """✅ Mark task as complete"""
    storage = get_storage()
    task = storage.get_task(task_id)
    if task:
        if task.completed:
            click.secho(f"ℹ Task already completed: [{task_id}] {task.description}", fg='blue')
        else:
            storage.complete_task(task_id)
            click.secho(f"✓ Task completed: [{task_id}] {task.description}", fg='green')
    else:
        click.secho(f"✗ Task not found: ID {task_id}", fg='red')


# Aliases
todo.add_command(list, name='ls')
todo.add_command(delete, name='rm')
todo.add_command(complete, name='done')
todo.add_command(interactive_mode, name='interactive')

if __name__ == '__main__':
    todo()





from .interactive import interactive as interactive_mode