/**
 * Edit Task Page
 * View and edit existing task with delete functionality.
 *
 * Spec Reference:
 * - specs/features/task-crud.md (FR3: Get Task, FR4: Update Task, FR5: Delete Task)
 * - specs/features/plans/quickstart.md (Edit Task Page)
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getTask, updateTask, deleteTask } from "@/lib/task-api";
import { TaskForm } from "@/components/tasks/TaskForm";
import type { Task, TaskUpdateRequest } from "@/types/task";

export default function EditTaskPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    async function loadTask() {
      try {
        // Parse and validate task ID
        const taskId = parseInt(params.id, 10);

        if (isNaN(taskId) || taskId <= 0) {
          setError("Invalid task ID");
          setLoading(false);
          return;
        }

        setLoading(true);
        setError(null);
        const data = await getTask(taskId);
        setTask(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load task");
      } finally {
        setLoading(false);
      }
    }

    loadTask();
  }, [params.id]);

  const handleSubmit = async (data: TaskUpdateRequest) => {
    const taskId = parseInt(params.id, 10);
    await updateTask(taskId, data);
    router.push("/dashboard");
  };

  const handleCancel = () => {
    router.push("/dashboard");
  };

  const handleDelete = async () => {
    try {
      setIsDeleting(true);
      const taskId = parseInt(params.id, 10);
      await deleteTask(taskId);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete task");
      setShowDeleteConfirm(false);
      setIsDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen py-8" style={{ background: '#f5f0eb' }}>
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-16 rounded-3xl" style={{ background: '#e8e2dc' }}>
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-[#e08b3d] border-t-transparent"></div>
            <p className="mt-4 text-sm font-medium text-gray-600">Loading task...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !task) {
    return (
      <div className="min-h-screen py-8" style={{ background: '#f5f0eb' }}>
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="rounded-lg p-6" style={{ background: '#f8d7da' }}>
            <p className="text-sm font-medium text-red-800">{error || "Task not found"}</p>
            <button
              onClick={() => router.push("/dashboard")}
              className="mt-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8" style={{ background: '#f5f0eb' }}>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
          <p className="mt-2 text-sm text-gray-600">
            Update task details or delete the task
          </p>
        </div>

        {/* Task Form */}
        <div className="rounded-3xl p-8" style={{ background: '#e8e2dc' }}>
          <TaskForm
            initialData={{
              title: task.title,
              description: task.description,
              status: task.status,
            }}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            submitLabel="Save Changes"
          />
        </div>

        {/* Delete Section */}
        <div className="mt-6 rounded-3xl p-6 border-l-4 border-red-500" style={{ background: '#fee' }}>
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg
                className="h-6 w-6 text-red-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div className="ml-3 flex-1">
              <h3 className="text-sm font-semibold text-gray-900">Danger Zone</h3>
              <div className="mt-2 text-sm text-gray-600">
                <p>
                  Once you delete this task, there is no going back. This action
                  cannot be undone.
                </p>
              </div>
              <div className="mt-4">
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  disabled={isDeleting}
                  className="px-6 py-2.5 text-sm font-semibold text-white bg-red-600 rounded-xl hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Delete Task
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-gray-900 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
            <div className="relative bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 p-6">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className="h-6 w-6 text-red-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                </div>
                <div className="ml-3 flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Delete Task
                  </h3>
                  <div className="mt-3 text-sm text-gray-600">
                    <p>
                      Are you sure you want to delete this task? This action
                      cannot be undone.
                    </p>
                    <p className="mt-3 font-semibold text-gray-900">
                      "{task.title}"
                    </p>
                  </div>
                  <div className="mt-6 flex gap-3">
                    <button
                      onClick={() => setShowDeleteConfirm(false)}
                      disabled={isDeleting}
                      className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#e08b3d] disabled:opacity-50 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleDelete}
                      disabled={isDeleting}
                      className="flex-1 px-4 py-2.5 text-sm font-semibold text-white bg-red-600 rounded-xl hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 transition-colors"
                    >
                      {isDeleting ? "Deleting..." : "Delete"}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
