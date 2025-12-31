/**
 * TaskCard Component
 * Displays a single task with circular checkbox and delete button.
 *
 * Spec Reference: specs/features/task-crud.md (UI/UX Requirements - Dashboard View)
 */

"use client";

import { useState } from "react";
import type { Task } from "@/types/task";
import { updateTask, deleteTask } from "@/lib/task-api";

interface TaskCardProps {
  task: Task;
  onTaskUpdate?: () => void;
}

export function TaskCard({ task, onTaskUpdate }: TaskCardProps) {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleCheckboxClick = async () => {
    try {
      setIsUpdating(true);
      const newStatus = task.status === "completed" ? "pending" : "completed";
      await updateTask(task.id, { status: newStatus });
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error) {
      console.error("Failed to update task:", error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await deleteTask(task.id);
      if (onTaskUpdate) {
        onTaskUpdate();
      }
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  const isCompleted = task.status === "completed";

  return (
    <div className="flex items-center gap-4 py-4 border-b border-gray-300 group">
      {/* Custom Circular Checkbox */}
      <button
        onClick={handleCheckboxClick}
        disabled={isUpdating}
        className="flex-shrink-0 relative"
      >
        <div
          className={`w-7 h-7 rounded-full border-2 flex items-center justify-center transition-all ${
            isCompleted
              ? "bg-[#e08b3d] border-[#e08b3d]"
              : "border-gray-400 hover:border-[#e08b3d]"
          } ${isUpdating ? "opacity-50" : ""}`}
        >
          {isCompleted && (
            <svg
              className="w-5 h-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={3}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </div>
      </button>

      {/* Task Title */}
      <div className="flex-1 min-w-0">
        <p
          className={`text-lg ${
            isCompleted
              ? "text-gray-400 line-through"
              : "text-gray-900"
          }`}
        >
          {task.title}
        </p>
      </div>

      {/* Delete Button */}
      <button
        onClick={handleDelete}
        className="flex-shrink-0 text-red-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
          />
        </svg>
      </button>
    </div>
  );
}
