import click
from .storage import TaskStorage
from .utils import format_task_table


def clear_screen():
    """Clear the terminal screen."""
    click.clear()


def show_menu():
    """Display the main menu."""
    click.echo("\n" + "="*60)
    click.secho("✨ TODO CLI - Task Manager ✨", fg='cyan', bold=True)
    click.echo("="*60)
    click.echo("\n1. Add new task ➕")
    click.echo("2. Update previous task 🔄")
    click.echo("3. Delete previous task 🗑️")
    click.echo("4. Show all tasks 📋")
    click.echo("5. Show pending tasks ⏳")
    click.echo("6. Show completed tasks ✅")
    click.echo("7. Mark task as complete ✓")
    click.echo("8. Exit 🔙")
    click.echo("\n" + "="*60)


def add_task_interactive(storage):
    """Add a new task interactively."""
    description = click.prompt("\n📝 Enter task description")
    if description.strip():
        task = storage.add_task(description)
        click.secho(f"\n✓ Task created: [{task.id}] {task.description}", fg='green')
    else:
        click.secho("\n✗ Task description cannot be empty!", fg='red')
    click.pause("\nPress any key to continue...")


def update_task_interactive(storage):
    """Update a task interactively."""
    tasks = storage.get_all_tasks()
    if not tasks:
        click.secho("\n✗ No tasks available to update!", fg='red')
        click.pause("\nPress any key to continue...")
        return
    
    click.echo("\n" + format_task_table(tasks))
    
    try:
        task_id = click.prompt("\n🔄 Enter task ID to update", type=int)
        task = storage.get_task(task_id)
        
        if task:
            click.echo(f"\nCurrent description: {task.description}")
            new_description = click.prompt("Enter new description")
            
            if new_description.strip():
                storage.update_task(task_id, new_description)
                click.secho(f"\n✓ Task updated: [{task_id}] {new_description}", fg='green')
            else:
                click.secho("\n✗ Description cannot be empty!", fg='red')
        else:
            click.secho(f"\n✗ Task not found: ID {task_id}", fg='red')
    except:
        click.secho("\n✗ Invalid input!", fg='red')
    
    click.pause("\nPress any key to continue...")


def delete_task_interactive(storage):
    """Delete a task interactively."""
    tasks = storage.get_all_tasks()
    if not tasks:
        click.secho("\n✗ No tasks available to delete!", fg='red')
        click.pause("\nPress any key to continue...")
        return
    
    click.echo("\n" + format_task_table(tasks))
    
    try:
        task_id = click.prompt("\n🗑️  Enter task ID to delete", type=int)
        task = storage.get_task(task_id)
        
        if task:
            confirm = click.confirm(f"\nAre you sure you want to delete: '{task.description}'?")
            if confirm:
                storage.delete_task(task_id)
                click.secho(f"\n✓ Task deleted: ID {task_id}", fg='green')
            else:
                click.secho("\n✗ Deletion cancelled", fg='yellow')
        else:
            click.secho(f"\n✗ Task not found: ID {task_id}", fg='red')
    except:
        click.secho("\n✗ Invalid input!", fg='red')
    
    click.pause("\nPress any key to continue...")


def show_all_tasks(storage):
    """Show all tasks."""
    tasks = storage.get_all_tasks()
    click.echo("\n" + format_task_table(tasks))
    click.pause("\nPress any key to continue...")


def show_pending_tasks(storage):
    """Show pending tasks."""
    tasks = [t for t in storage.get_all_tasks() if not t.completed]
    click.echo("\n" + format_task_table(tasks))
    click.pause("\nPress any key to continue...")


def show_completed_tasks(storage):
    """Show completed tasks."""
    tasks = [t for t in storage.get_all_tasks() if t.completed]
    click.echo("\n" + format_task_table(tasks))
    click.pause("\nPress any key to continue...")


def complete_task_interactive(storage):
    """Mark a task as complete interactively."""
    tasks = [t for t in storage.get_all_tasks() if not t.completed]
    if not tasks:
        click.secho("\n✗ No pending tasks to complete!", fg='red')
        click.pause("\nPress any key to continue...")
        return
    
    click.echo("\n" + format_task_table(tasks))
    
    try:
        task_id = click.prompt("\n✓ Enter task ID to mark as complete", type=int)
        task = storage.get_task(task_id)
        
        if task:
            if task.completed:
                click.secho(f"\nℹ Task already completed: [{task_id}] {task.description}", fg='blue')
            else:
                storage.complete_task(task_id)
                click.secho(f"\n✓ Task completed: [{task_id}] {task.description}", fg='green')
        else:
            click.secho(f"\n✗ Task not found: ID {task_id}", fg='red')
    except:
        click.secho("\n✗ Invalid input!", fg='red')
    
    click.pause("\nPress any key to continue...")


@click.command()
def interactive():
    """Launch interactive todo manager."""
    storage = TaskStorage()
    
    while True:
        clear_screen()
        show_menu()
        
        choice = click.prompt("\n👉 Select an option", type=str, default="8")
        
        if choice == "1":
            add_task_interactive(storage)
        elif choice == "2":
            update_task_interactive(storage)
        elif choice == "3":
            delete_task_interactive(storage)
        elif choice == "4":
            show_all_tasks(storage)
        elif choice == "5":
            show_pending_tasks(storage)
        elif choice == "6":
            show_completed_tasks(storage)
        elif choice == "7":
            complete_task_interactive(storage)
        elif choice == "8":
            click.secho("\n👋 Thanks for using Todo CLI! Goodbye!", fg='cyan', bold=True)
            break
        else:
            click.secho("\n✗ Invalid option! Please select 1-8", fg='red')
            click.pause("\nPress any key to continue...")


if __name__ == '__main__':
    interactive()