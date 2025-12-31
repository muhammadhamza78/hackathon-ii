"""
Task CRUD API Endpoints
FastAPI router for task create, read, update, delete operations.

Spec Reference: specs/features/task-crud.md (FR1-FR6)
Plan Reference: specs/features/plans/task-crud-plan.md
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, UTC
from app.db.session import get_session
from app.auth.dependencies import get_current_user_id
from app.models.task import Task, TaskStatus
from app.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
    TaskListResponse
)

router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Spec: specs/features/task-crud.md (FR1: Create Task)
    Contract: specs/features/plans/contracts/task-create.json

    Args:
        request: Task creation data (title, description, status)
        user_id: Authenticated user ID (auto-extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Created task with auto-generated ID and timestamps

    Raises:
        HTTPException 401: Missing or invalid JWT token
        HTTPException 422: Validation error (title too long, invalid status, etc.)

    User Isolation: user_id is auto-assigned from JWT (never from request body)
    """
    # Create task with user_id from JWT
    task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        user_id=user_id,  # Auto-assign from JWT (Constitution III)
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.from_orm(task)


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    List all tasks for the authenticated user.

    Spec: specs/features/task-crud.md (FR2: List All Tasks)
    Contract: specs/features/plans/contracts/task-list.json

    Args:
        user_id: Authenticated user ID (auto-extracted from JWT)
        session: Database session

    Returns:
        TaskListResponse: Array of tasks owned by user, ordered by created_at DESC

    Raises:
        HTTPException 401: Missing or invalid JWT token

    User Isolation: Returns ONLY tasks where user_id matches authenticated user
    Research: specs/features/plans/research.md (R2: User Isolation Pattern)
    """
    # Query tasks with user isolation (Constitution III - NON-NEGOTIABLE)
    # Explicit WHERE clause for visibility and auditability
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )

    tasks = session.exec(statement).all()

    # Convert to response models
    task_responses = [TaskResponse.from_orm(task) for task in tasks]

    return TaskListResponse(tasks=task_responses)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a single task by ID (only if owned by authenticated user).

    Spec: specs/features/task-crud.md (FR3: Get Single Task)
    Contract: specs/features/plans/contracts/task-get.json

    Args:
        task_id: Task ID from path parameter
        user_id: Authenticated user ID (auto-extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Task details if found and owned by user

    Raises:
        HTTPException 401: Missing or invalid JWT token
        HTTPException 404: Task not found OR belongs to different user

    User Isolation: Returns 404 if task exists but belongs to different user
    Research: specs/features/plans/research.md (R3: 404 for Cross-User Access)
    """
    # Query with user isolation (Constitution III - NON-NEGOTIABLE)
    # Returns None if task doesn't exist OR belongs to different user
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Return 404 (not 403) to prevent user enumeration
        # Same response whether task doesn't exist or belongs to other user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.from_orm(task)


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update an existing task (only if owned by authenticated user).

    Partial updates supported - only provided fields will be updated.

    Spec: specs/features/task-crud.md (FR4: Update Task)
    Contract: specs/features/plans/contracts/task-update.json

    Args:
        task_id: Task ID from path parameter
        request: Task update data (all fields optional)
        user_id: Authenticated user ID (auto-extracted from JWT)
        session: Database session

    Returns:
        TaskResponse: Updated task with auto-updated updated_at

    Raises:
        HTTPException 401: Missing or invalid JWT token
        HTTPException 404: Task not found OR belongs to different user
        HTTPException 422: Validation error (title too long, invalid status, etc.)

    User Isolation: Returns 404 if task exists but belongs to different user
    Immutability: created_at and user_id cannot be changed
    """
    # Query with user isolation (Constitution III - NON-NEGOTIABLE)
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Return 404 (not 403) to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields (partial update)
    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status

    # Auto-update updated_at timestamp
    task.updated_at = datetime.now(UTC)

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.from_orm(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task (only if owned by authenticated user).

    Spec: specs/features/task-crud.md (FR5: Delete Task)
    Contract: specs/features/plans/contracts/task-delete.json

    Args:
        task_id: Task ID from path parameter
        user_id: Authenticated user ID (auto-extracted from JWT)
        session: Database session

    Returns:
        None: 204 No Content on successful deletion

    Raises:
        HTTPException 401: Missing or invalid JWT token
        HTTPException 404: Task not found OR belongs to different user

    User Isolation: Returns 404 if task exists but belongs to different user
    Idempotency: DELETE is idempotent - subsequent DELETE returns 404
    """
    # Query with user isolation (Constitution III - NON-NEGOTIABLE)
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Return 404 (not 403) to prevent user enumeration
        # Deletion is NOT applied if task doesn't exist or belongs to other user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task from database
    session.delete(task)
    session.commit()

    # Return 204 No Content (no response body)
