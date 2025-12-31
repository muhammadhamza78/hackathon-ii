/**
 * Task API Client
 * API functions for task CRUD operations.
 *
 * Spec Reference: specs/features/task-crud.md (FR1-FR5)
 * Plan Reference: specs/features/plans/quickstart.md (API Client section)
 */

import { apiGet, apiPost, apiPut, apiDelete } from "./api";
import type {
  Task,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskListResponse,
} from "@/types/task";

/**
 * Get all tasks for the authenticated user.
 *
 * Spec: specs/features/task-crud.md (FR2: List All Tasks)
 * Contract: specs/features/plans/contracts/task-list.json
 *
 * @returns Promise<TaskListResponse> - Array of tasks ordered by created_at DESC
 * @throws Error if request fails or user not authenticated
 */
export async function getTasks(): Promise<TaskListResponse> {
  const response = await apiGet("/api/tasks");

  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Create a new task for the authenticated user.
 *
 * Spec: specs/features/task-crud.md (FR1: Create Task)
 * Contract: specs/features/plans/contracts/task-create.json
 *
 * @param data - Task creation data (title, description, status)
 * @returns Promise<Task> - Created task with auto-generated ID
 * @throws Error if validation fails (422) or user not authenticated (401)
 */
export async function createTask(data: TaskCreateRequest): Promise<Task> {
  const response = await apiPost("/api/tasks", data);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to create task: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get a single task by ID.
 *
 * Spec: specs/features/task-crud.md (FR3: Get Single Task)
 * Contract: specs/features/plans/contracts/task-get.json
 *
 * @param id - Task ID
 * @returns Promise<Task> - Task details
 * @throws Error if task not found (404) or user not authenticated (401)
 */
export async function getTask(id: number): Promise<Task> {
  const response = await apiGet(`/api/tasks/${id}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Task not found");
    }
    throw new Error(`Failed to fetch task: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Update an existing task.
 *
 * Partial updates supported - only provided fields will be updated.
 *
 * Spec: specs/features/task-crud.md (FR4: Update Task)
 * Contract: specs/features/plans/contracts/task-update.json
 *
 * @param id - Task ID
 * @param data - Task update data (all fields optional)
 * @returns Promise<Task> - Updated task
 * @throws Error if validation fails (422), not found (404), or not authenticated (401)
 */
export async function updateTask(
  id: number,
  data: TaskUpdateRequest
): Promise<Task> {
  const response = await apiPut(`/api/tasks/${id}`, data);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Task not found");
    }
    const error = await response.json();
    throw new Error(error.detail || `Failed to update task: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete a task.
 *
 * Spec: specs/features/task-crud.md (FR5: Delete Task)
 * Contract: specs/features/plans/contracts/task-delete.json
 *
 * @param id - Task ID
 * @returns Promise<void> - No content on success (204)
 * @throws Error if not found (404) or not authenticated (401)
 */
export async function deleteTask(id: number): Promise<void> {
  const response = await apiDelete(`/api/tasks/${id}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Task not found");
    }
    throw new Error(`Failed to delete task: ${response.statusText}`);
  }

  // No response body for 204 No Content
}
