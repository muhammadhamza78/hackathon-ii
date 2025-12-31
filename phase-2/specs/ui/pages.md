# UI Pages Specification

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Status:** Specification
**Framework**: Next.js 16+ (App Router)

## Overview

Complete specification of all pages in the Task Management System frontend. Uses Next.js App Router for routing and server components for optimal performance.

## Page Structure (App Router)

```
app/
├── layout.tsx           # Root layout (auth provider, global styles)
├── page.tsx             # Landing/Login page (/)
├── register/
│   └── page.tsx         # Registration page (/register)
└── dashboard/
    ├── layout.tsx       # Dashboard layout (auth check)
    ├── page.tsx         # Task list page (/dashboard)
    ├── new/
    │   └── page.tsx     # New task page (/dashboard/new)
    └── [id]/
        ├── page.tsx     # Task detail/edit page (/dashboard/[id])
        └── edit/
            └── page.tsx # Alternative edit page (/dashboard/[id]/edit)
```

---

## Page: Landing / Login

**Route**: `/`

**File**: `app/page.tsx`

**Access**: Public (unauthenticated users)

**Purpose**: Landing page with login form for returning users

### Layout

**Header**:
- App logo/title: "Task Manager"
- Tagline: "Organize your tasks efficiently"

**Main Content**:
- Login form (centered)
- Link to registration page

**Footer**:
- Copyright notice
- Links: About, Privacy, Terms (optional for MVP)

### Login Form

**Fields**:
1. Email
   - Type: email
   - Placeholder: "Enter your email"
   - Validation: Required, email format
   - Autocomplete: email

2. Password
   - Type: password
   - Placeholder: "Enter your password"
   - Validation: Required
   - Autocomplete: current-password

**Actions**:
- Submit button: "Login"
- Link: "Don't have an account? Register here" → `/register`

### Form Behavior

**On Submit**:
1. Validate fields (client-side)
2. Call `POST /api/auth/login` with email and password
3. On success:
   - Store JWT token in localStorage
   - Redirect to `/dashboard`
4. On error:
   - Display error message below form
   - Keep form populated (except password)

**Error Messages**:
- 401: "Invalid email or password. Please try again."
- 422: Display field-specific errors
- Network error: "Unable to connect. Please try again."

### Redirect Behavior

**If Already Logged In**:
- Check for valid JWT token
- If valid token exists, redirect to `/dashboard`
- If expired token, stay on login page, show message: "Your session expired. Please log in again."

### Page Meta

**Title**: "Login - Task Manager"
**Description**: "Log in to manage your tasks"

### Acceptance Criteria

- [ ] Login form renders with email and password fields
- [ ] Client-side validation prevents empty submissions
- [ ] Successful login stores token and redirects to dashboard
- [ ] Invalid credentials show error message
- [ ] Link to registration page works
- [ ] Already logged-in users are redirected to dashboard
- [ ] Responsive design works on mobile and desktop

---

## Page: Registration

**Route**: `/register`

**File**: `app/register/page.tsx`

**Access**: Public (unauthenticated users)

**Purpose**: New user registration

### Layout

**Header**:
- App logo/title: "Task Manager"
- Back link: "← Back to Login"

**Main Content**:
- Registration form (centered)

### Registration Form

**Fields**:
1. Email
   - Type: email
   - Placeholder: "Enter your email"
   - Validation: Required, email format, max 255 chars
   - Autocomplete: email

2. Password
   - Type: password
   - Placeholder: "Create a password (min 8 characters)"
   - Validation: Required, min 8 chars, max 128 chars
   - Autocomplete: new-password
   - Show/hide password toggle (optional)

3. Confirm Password (optional for MVP)
   - Type: password
   - Placeholder: "Confirm your password"
   - Validation: Must match password field

**Actions**:
- Submit button: "Create Account"
- Link: "Already have an account? Login here" → `/`

### Form Behavior

**On Submit**:
1. Validate fields (client-side)
2. Check passwords match (if confirm password field exists)
3. Call `POST /api/auth/register` with email and password
4. On success:
   - Redirect to `/` (login page)
   - Show success message: "Account created! Please log in."
5. On error:
   - Display error message below form
   - Keep form populated (except passwords)

**Error Messages**:
- 400 (duplicate email): "This email is already registered. Please log in instead."
- 422 (validation): Display field-specific errors
  - "Email must be a valid email address"
  - "Password must be at least 8 characters"
- Network error: "Unable to connect. Please try again."

### Validation Feedback

**Real-time Validation** (optional enhancement):
- Email format check as user types
- Password length indicator
- Password strength meter (weak/medium/strong)

**Submit Button State**:
- Disabled while submitting
- Show loading spinner during API call

### Redirect Behavior

**If Already Logged In**:
- Redirect to `/dashboard`

### Page Meta

**Title**: "Register - Task Manager"
**Description**: "Create your account to start managing tasks"

### Acceptance Criteria

- [ ] Registration form renders with email and password fields
- [ ] Client-side validation prevents invalid submissions
- [ ] Successful registration redirects to login with success message
- [ ] Duplicate email shows error message
- [ ] Validation errors are displayed clearly
- [ ] Link to login page works
- [ ] Responsive design works on mobile and desktop

---

## Page: Dashboard (Task List)

**Route**: `/dashboard`

**File**: `app/dashboard/page.tsx`

**Access**: Protected (requires authentication)

**Purpose**: Display list of user's tasks

### Layout

**Header** (Navigation):
- App logo/title: "Task Manager"
- User email (from JWT)
- Logout button

**Main Content**:
- Page title: "My Tasks"
- "New Task" button (prominent, top-right)
- Task list or empty state

**Footer**:
- Optional: Task count summary

### Task List

**Display Format**:
- Each task as a card or list item
- Order: created_at descending (newest first)

**Task Card Content**:
- Task title (bold, large)
- Status badge (colored pill)
- Description (truncated to 100 chars with "..." if longer)
- Created date (relative format: "2 hours ago", "Yesterday")
- Actions: Edit button, Delete button

**Status Badge Colors**:
- `pending`: Gray background
- `in_progress`: Blue background
- `completed`: Green background

**Empty State**:
- Icon: Empty box or clipboard
- Message: "No tasks yet. Create your first task!"
- Button: "Create Task" → `/dashboard/new`

### Actions

**New Task Button**:
- Location: Top-right of page
- Style: Primary button (filled, prominent)
- Action: Navigate to `/dashboard/new`

**Edit Task**:
- Location: On each task card
- Icon: Pencil/edit icon
- Action: Navigate to `/dashboard/[id]/edit` or `/dashboard/[id]`

**Delete Task**:
- Location: On each task card
- Icon: Trash/delete icon
- Action: Show confirmation dialog, then DELETE `/api/tasks/{id}`

**Delete Confirmation**:
- Modal/dialog: "Are you sure you want to delete this task? This action cannot be undone."
- Buttons: "Cancel" (secondary), "Delete" (danger, red)

**Logout**:
- Location: Header, top-right
- Action: Remove JWT token from localStorage, redirect to `/`

### Data Loading

**Server Component** (preferred):
- Fetch tasks on server using JWT from cookie
- Render task list server-side
- No loading spinner (instant render)

**Client Component** (fallback):
- Show loading spinner while fetching tasks
- Call `GET /api/tasks` with JWT from localStorage
- Render task list on data received

**Error Handling**:
- 401 (unauthorized): Redirect to login page
- Network error: Show error message with retry button

### Redirect Behavior

**If Not Logged In**:
- Redirect to `/` (login page)

### Page Meta

**Title**: "My Tasks - Task Manager"
**Description**: "Manage your tasks"

### Acceptance Criteria

- [ ] Task list displays all user's tasks
- [ ] Tasks ordered by created_at descending
- [ ] Status badges display with correct colors
- [ ] Empty state shown when no tasks
- [ ] New Task button navigates to creation page
- [ ] Edit button navigates to task detail/edit page
- [ ] Delete button shows confirmation and deletes task
- [ ] Logout button clears token and redirects to login
- [ ] Unauthenticated users are redirected to login
- [ ] Responsive design works on mobile and desktop

---

## Page: New Task

**Route**: `/dashboard/new`

**File**: `app/dashboard/new/page.tsx`

**Access**: Protected (requires authentication)

**Purpose**: Create a new task

### Layout

**Header**: Same as dashboard (navigation bar)

**Main Content**:
- Page title: "Create New Task"
- Task form

**Breadcrumb** (optional):
- Dashboard > New Task

### Task Creation Form

**Fields**:
1. Title
   - Type: text
   - Placeholder: "Enter task title"
   - Validation: Required, max 200 chars
   - Show character count: "0 / 200"

2. Description
   - Type: textarea
   - Placeholder: "Enter task description (optional)"
   - Validation: Optional, max 2000 chars
   - Rows: 5
   - Show character count: "0 / 2000"

3. Status
   - Type: select/dropdown
   - Options: Pending (default), In Progress, Completed
   - Default: Pending

**Actions**:
- Submit button: "Create Task" (primary)
- Cancel button: "Cancel" (secondary) → Navigate back to `/dashboard`

### Form Behavior

**On Submit**:
1. Validate fields (client-side)
2. Call `POST /api/tasks` with title, description, status
3. On success:
   - Redirect to `/dashboard`
   - Show success toast: "Task created successfully!"
4. On error:
   - Display error message below form
   - Keep form populated

**Error Messages**:
- 401: Redirect to login
- 422: Display field-specific errors
- Network error: "Unable to save task. Please try again."

**Cancel Button**:
- Navigate back to `/dashboard`
- No confirmation dialog (form state lost)

### Validation Feedback

**Real-time Validation**:
- Character count updates as user types
- Title length limit enforced (prevent typing beyond 200 chars or show warning)

**Submit Button State**:
- Disabled if title is empty
- Disabled while submitting (show loading spinner)

### Page Meta

**Title**: "New Task - Task Manager"
**Description**: "Create a new task"

### Acceptance Criteria

- [ ] Form renders with title, description, and status fields
- [ ] Character counters display and update
- [ ] Client-side validation prevents invalid submissions
- [ ] Successful creation redirects to dashboard with success message
- [ ] Validation errors are displayed clearly
- [ ] Cancel button navigates back to dashboard
- [ ] Unauthenticated users are redirected to login
- [ ] Responsive design works on mobile and desktop

---

## Page: Task Detail / Edit

**Route**: `/dashboard/[id]`

**File**: `app/dashboard/[id]/page.tsx`

**Access**: Protected (requires authentication)

**Purpose**: View and edit an existing task

### Layout

**Header**: Same as dashboard (navigation bar)

**Main Content**:
- Page title: "Edit Task" or task title
- Task edit form
- Delete button (danger zone)

**Breadcrumb** (optional):
- Dashboard > [Task Title]

### Task Edit Form

**Fields**: Same as creation form, but pre-populated with existing task data

1. Title (pre-filled with task.title)
2. Description (pre-filled with task.description or empty)
3. Status (pre-selected with task.status)

**Actions**:
- Save button: "Save Changes" (primary)
- Cancel button: "Cancel" (secondary) → Navigate back to `/dashboard`
- Delete button: "Delete Task" (danger, bottom of form)

### Form Behavior

**On Load**:
1. Fetch task data: `GET /api/tasks/{id}`
2. If 404: Show error "Task not found" and link back to dashboard
3. If success: Populate form fields

**On Save**:
1. Validate fields (client-side)
2. Call `PUT /api/tasks/{id}` with updated data
3. On success:
   - Redirect to `/dashboard`
   - Show success toast: "Task updated successfully!"
4. On error:
   - Display error message
   - Keep form populated

**On Delete**:
1. Show confirmation dialog
2. If confirmed, call `DELETE /api/tasks/{id}`
3. On success:
   - Redirect to `/dashboard`
   - Show success toast: "Task deleted successfully!"

**Cancel Button**:
- Navigate back to `/dashboard`
- No save, no confirmation

### Error Handling

**404 Not Found**:
- Show message: "Task not found. It may have been deleted."
- Button: "Back to Dashboard" → `/dashboard`

**401 Unauthorized**:
- Redirect to login page

### Page Meta

**Title**: "[Task Title] - Task Manager" (dynamic)
**Description**: "Edit your task"

### Acceptance Criteria

- [ ] Form pre-populated with existing task data
- [ ] Character counters work correctly
- [ ] Save button updates task and redirects to dashboard
- [ ] Delete button shows confirmation and deletes task
- [ ] Cancel button navigates back without saving
- [ ] 404 error shown if task not found or not owned by user
- [ ] Validation errors are displayed clearly
- [ ] Unauthenticated users are redirected to login
- [ ] Responsive design works on mobile and desktop

---

## Global Components

### Authentication Provider

**Purpose**: Manage authentication state globally

**Implementation**:
```typescript
// app/providers/AuthProvider.tsx
"use client";
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext<{
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}>({
  token: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('token');
    setToken(stored);
  }, []);

  const login = (token: string) => {
    localStorage.setItem('token', token);
    setToken(token);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

### Protected Route Wrapper

**Purpose**: Redirect unauthenticated users to login

**Implementation**:
```typescript
// app/dashboard/layout.tsx
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

export default function DashboardLayout({ children }) {
  const token = cookies().get('token');

  if (!token) {
    redirect('/');
  }

  return <div>{children}</div>;
}
```

**Alternative** (client-side):
```typescript
"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';

export function ProtectedRoute({ children }) {
  const { token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!token) {
      router.push('/');
    }
  }, [token, router]);

  if (!token) return null;

  return <>{children}</>;
}
```

---

## Responsive Design

### Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Mobile Adaptations

**Navigation**:
- Hamburger menu for mobile
- Full navigation bar for desktop

**Task Cards**:
- Stack vertically on mobile
- Grid layout (2-3 columns) on desktop

**Forms**:
- Full width inputs on mobile
- Max-width container (600px) on desktop

**Buttons**:
- Full width on mobile
- Auto width on desktop

---

## Accessibility

**WCAG 2.1 Level AA**:
- Color contrast ratios met (4.5:1 for text)
- Keyboard navigation supported
- ARIA labels for interactive elements
- Focus indicators visible
- Alt text for images (if any)

**Form Accessibility**:
- Labels associated with inputs
- Error messages announced by screen readers
- Required fields marked with aria-required

---

## Acceptance Criteria Summary

**All pages are DONE when**:
- [ ] All routes defined and navigable
- [ ] Authentication flow works (login, register, logout)
- [ ] Protected routes redirect unauthenticated users
- [ ] Task CRUD operations work through UI
- [ ] All forms have validation
- [ ] Error states are handled gracefully
- [ ] Success/error messages are shown
- [ ] Responsive design works on all screen sizes
- [ ] Accessibility standards met
- [ ] TypeScript types defined for all props and state

---

## References

- See: `specs/features/authentication.md` (Auth requirements)
- See: `specs/features/task-crud.md` (Task CRUD requirements)
- See: `specs/ui/components.md` (Reusable component specs)
- See: `specs/api/rest-endpoints.md` (API contracts)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
