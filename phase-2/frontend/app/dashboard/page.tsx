/**
 * Dashboard Page
 * Displays list of user's tasks with create button.
 *
 * Spec Reference:
 * - specs/features/task-crud.md (FR2: List All Tasks, UI/UX Requirements)
 * - specs/features/plans/quickstart.md (Dashboard Integration)
 */

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getTasks } from "@/lib/task-api";
import { TaskList } from "@/components/tasks/TaskList";
import type { Task } from "@/types/task";

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getTasks();
      setTasks(data.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  // Filter tasks by search query
  const filteredTasks = tasks.filter((task) =>
    task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.status === "completed").length;
  const pendingTasks = tasks.filter(t => t.status === "pending").length;
  const inProgressTasks = tasks.filter(t => t.status === "in_progress").length;

  // Clear completed tasks
  const handleClearCompleted = async () => {
    const completedTaskIds = tasks.filter(t => t.status === "completed").map(t => t.id);
    // TODO: Implement bulk delete
    loadTasks();
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Personal Tab */}
      <div className="flex mb-6 border-b-2 border-gray-300">
        <div className="px-6 py-3 text-lg font-semibold text-gray-900 border-b-4 border-[#e08b3d] -mb-0.5">
          Personal
        </div>
      </div>

      {/* Search Bar and Add Button */}
      <div className="mb-6">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <svg
              className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-6 py-4 rounded-2xl text-gray-700 text-lg focus:outline-none focus:ring-2 focus:ring-[#e08b3d]"
              style={{ background: '#e8e2dc' }}
            />
          </div>
          <Link
            href="/tasks/new"
            className="px-8 py-4 rounded-2xl text-white font-semibold text-lg hover:opacity-90 transition-opacity"
            style={{ background: '#6db9d4' }}
          >
            ADD
          </Link>
        </div>
      </div>

      {/* Task List Container */}
      <div className="rounded-3xl p-8" style={{ background: '#e8e2dc' }}>
        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-[#e08b3d] border-t-transparent"></div>
            <p className="mt-4 text-sm font-medium text-gray-600">Loading tasks...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-4">
            <p className="text-sm font-medium text-red-800">{error}</p>
          </div>
        )}

        {/* Task List */}
        {!loading && !error && (
          <>
            <TaskList tasks={filteredTasks} onTaskUpdate={loadTasks} />

            {/* Clear Completed Button */}
            {completedTasks > 0 && (
              <div className="flex justify-end mt-6">
                <button
                  onClick={handleClearCompleted}
                  className="flex items-center gap-2 text-[#e08b3d] hover:text-[#d17a2f] font-medium transition-colors"
                >
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Clear Completed
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
