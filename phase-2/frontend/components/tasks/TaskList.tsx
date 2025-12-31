/**
 * TaskList Component
 * Displays a list of tasks or empty state message.
 *
 * Spec Reference: specs/features/task-crud.md (UI/UX Requirements - Dashboard View, Empty State)
 */

import type { Task } from "@/types/task";
import { TaskCard } from "./TaskCard";

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate?: () => void;
}

export function TaskList({ tasks, onTaskUpdate }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-200 rounded-full mb-4">
          <svg
            className="h-8 w-8 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-700 mb-2">No tasks yet</h3>
        <p className="text-sm text-gray-500">
          Click the ADD button above to create your first task
        </p>
      </div>
    );
  }

  return (
    <div>
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onTaskUpdate={onTaskUpdate} />
      ))}
    </div>
  );
}
