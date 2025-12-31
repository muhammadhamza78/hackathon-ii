/**
 * Create Task Page
 * Form page for creating new tasks.
 *
 * Spec Reference:
 * - specs/features/task-crud.md (FR1: Create Task, UI/UX Requirements)
 * - specs/features/plans/quickstart.md (Create Task Page)
 */

"use client";

import { useRouter } from "next/navigation";
import { createTask } from "@/lib/task-api";
import { TaskForm } from "@/components/tasks/TaskForm";
import type { TaskCreateRequest } from "@/types/task";

export default function NewTaskPage() {
  const router = useRouter();

  const handleSubmit = async (data: TaskCreateRequest) => {
    await createTask(data);
    router.push("/dashboard");
  };

  const handleCancel = () => {
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen py-8" style={{ background: '#f5f0eb' }}>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
          <p className="mt-2 text-sm text-gray-600">
            Add a new task to your list
          </p>
        </div>

        {/* Task Form */}
        <div className="rounded-3xl p-8" style={{ background: '#e8e2dc' }}>
          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            submitLabel="Create Task"
          />
        </div>
      </div>
    </div>
  );
}
