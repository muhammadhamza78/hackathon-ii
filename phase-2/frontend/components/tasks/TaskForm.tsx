/**
 * TaskForm Component
 * Form for creating and editing tasks with validation and error handling.
 *
 * Spec Reference: specs/features/task-crud.md (UI/UX Requirements - Task Creation Form)
 * Research: specs/features/plans/research.md (R6: Error Handling)
 */

"use client";

import { useState, FormEvent, ChangeEvent } from "react";
import type { TaskCreateRequest, TaskStatus } from "@/types/task";

interface TaskFormProps {
  initialData?: TaskCreateRequest;
  onSubmit: (data: TaskCreateRequest) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}

const MAX_TITLE_LENGTH = 200;
const MAX_DESCRIPTION_LENGTH = 2000;

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = "Create Task",
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreateRequest>({
    title: initialData?.title || "",
    description: initialData?.description || "",
    status: initialData?.status || "pending",
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    } else if (formData.title.length > MAX_TITLE_LENGTH) {
      newErrors.title = `Title must be ${MAX_TITLE_LENGTH} characters or less`;
    }

    if (
      formData.description &&
      formData.description.length > MAX_DESCRIPTION_LENGTH
    ) {
      newErrors.description = `Description must be ${MAX_DESCRIPTION_LENGTH} characters or less`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      await onSubmit(formData);
    } catch (error) {
      // Handle validation errors from backend
      if (error instanceof Error) {
        setErrors({ general: error.message });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const titleLength = formData.title.length;
  const descriptionLength = formData.description?.length || 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {errors.general && (
        <div className="rounded-lg p-4" style={{ background: '#f8d7da' }}>
          <p className="text-sm text-red-800">{errors.general}</p>
        </div>
      )}

      {/* Title Field */}
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <div>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`block w-full px-4 py-3 rounded-xl text-gray-700 focus:outline-none ${
              errors.title
                ? "border-2 border-red-500 focus:ring-2 focus:ring-red-500"
                : "focus:ring-2 focus:ring-[#e08b3d]"
            }`}
            style={{ background: errors.title ? '#fee' : '#f5f0eb' }}
            placeholder="e.g., Buy groceries"
            maxLength={MAX_TITLE_LENGTH}
          />
          <div className="mt-2 flex justify-between text-xs">
            {errors.title && <span className="text-red-600">{errors.title}</span>}
            <span className={`${errors.title ? '' : 'ml-auto'} text-gray-500`}>
              {titleLength}/{MAX_TITLE_LENGTH}
            </span>
          </div>
        </div>
      </div>

      {/* Description Field */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Description (Optional)
        </label>
        <div>
          <textarea
            id="description"
            name="description"
            rows={4}
            value={formData.description || ""}
            onChange={handleChange}
            className={`block w-full px-4 py-3 rounded-xl text-gray-700 focus:outline-none resize-none ${
              errors.description
                ? "border-2 border-red-500 focus:ring-2 focus:ring-red-500"
                : "focus:ring-2 focus:ring-[#e08b3d]"
            }`}
            style={{ background: errors.description ? '#fee' : '#f5f0eb' }}
            placeholder="e.g., Milk, eggs, bread, cheese"
            maxLength={MAX_DESCRIPTION_LENGTH}
          />
          <div className="mt-2 flex justify-between text-xs">
            {errors.description && (
              <span className="text-red-600">{errors.description}</span>
            )}
            <span className={`${errors.description ? '' : 'ml-auto'} text-gray-500`}>
              {descriptionLength}/{MAX_DESCRIPTION_LENGTH}
            </span>
          </div>
        </div>
      </div>

      {/* Status Field */}
      <div>
        <label
          htmlFor="status"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Status
        </label>
        <select
          id="status"
          name="status"
          value={formData.status}
          onChange={handleChange}
          className="block w-full px-4 py-3 rounded-xl text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#e08b3d]"
          style={{ background: '#f5f0eb' }}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end gap-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#e08b3d] transition-colors"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-6 py-3 text-sm font-semibold text-white rounded-xl hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-[#e08b3d] disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
          style={{ background: '#e08b3d' }}
        >
          {isSubmitting ? "Saving..." : submitLabel}
        </button>
      </div>
    </form>
  );
}
