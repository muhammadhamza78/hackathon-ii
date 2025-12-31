/**
 * StatusBadge Component
 * Displays task status with color-coded badge.
 *
 * Spec Reference: specs/features/task-crud.md (UI/UX Requirements - Status Display)
 * Research: specs/features/plans/research.md (R7: Status Badge Colors)
 */

import type { TaskStatus } from "@/types/task";
import type { ReactElement } from "react";

interface StatusBadgeProps {
  status: TaskStatus;
}

const statusConfig: Record<TaskStatus, { bg: string; text: string; icon: ReactElement; label: string }> = {
  pending: {
    bg: "bg-gray-100",
    text: "text-gray-700",
    label: "Pending",
    icon: (
      <svg className="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
      </svg>
    ),
  },
  in_progress: {
    bg: "bg-blue-100",
    text: "text-blue-700",
    label: "In Progress",
    icon: (
      <svg className="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
      </svg>
    ),
  },
  completed: {
    bg: "bg-green-100",
    text: "text-green-700",
    label: "Completed",
    icon: (
      <svg className="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
      </svg>
    ),
  },
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.icon}
      {config.label}
    </span>
  );
}
