# UI Components Specification

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Status:** Specification
**Framework**: React (Next.js 16+ App Router)

## Overview

Specification of reusable UI components for the Task Management System. Components follow atomic design principles and are built with TypeScript for type safety.

## Component Categories

1. **Layout Components**: Navigation, headers, containers
2. **Form Components**: Inputs, buttons, form wrappers
3. **Task Components**: Task-specific cards and lists
4. **Feedback Components**: Alerts, toasts, loading spinners
5. **Utility Components**: Protected route wrapper, error boundaries

---

## Layout Components

### NavBar

**Purpose**: Global navigation header with logo, user info, and logout

**File**: `components/layout/NavBar.tsx`

**Props**:
```typescript
interface NavBarProps {
  userEmail?: string;  // Optional, shown if user is logged in
  onLogout?: () => void;  // Logout handler
}
```

**Behavior**:
- Display app logo/title (link to `/dashboard` if logged in, `/` if not)
- If `userEmail` provided, show user email and logout button
- If no `userEmail`, show login/register links

**Variants**:
- **Authenticated**: Logo, user email, logout button
- **Unauthenticated**: Logo, login link, register link

**Styling**:
- Fixed top position (optional) or static
- Background: Primary color
- Text: White or contrasting color
- Responsive: Hamburger menu on mobile

**Acceptance Criteria**:
- [ ] Renders logo and title
- [ ] Shows user email when authenticated
- [ ] Logout button calls onLogout handler
- [ ] Login/register links shown when not authenticated
- [ ] Responsive on mobile (hamburger menu)

---

### PageContainer

**Purpose**: Consistent page wrapper with max-width and padding

**File**: `components/layout/PageContainer.tsx`

**Props**:
```typescript
interface PageContainerProps {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl';  // Default: 'lg'
}
```

**Behavior**:
- Center content horizontally
- Apply max-width based on prop
- Add consistent padding (16px mobile, 24px desktop)

**Max-Width Values**:
- `sm`: 640px (forms)
- `md`: 768px (content pages)
- `lg`: 1024px (dashboard)
- `xl`: 1280px (wide layouts)

**Acceptance Criteria**:
- [ ] Centers content horizontally
- [ ] Applies correct max-width
- [ ] Responsive padding

---

## Form Components

### Input

**Purpose**: Reusable text input with label, validation, and error display

**File**: `components/form/Input.tsx`

**Props**:
```typescript
interface InputProps {
  id: string;
  name: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number';
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;  // Error message to display
  required?: boolean;
  maxLength?: number;
  showCharCount?: boolean;  // Show "X / Y" character count
  autoComplete?: string;
  disabled?: boolean;
}
```

**Behavior**:
- Render label above input
- Display error message below input (if provided)
- Show character count below input (if `showCharCount` and `maxLength` provided)
- Apply error styling (red border) if error exists
- Mark as required with asterisk if `required` is true

**Styling**:
- Label: Bold, small margin-bottom
- Input: Full width, border, padding, rounded corners
- Error: Red text, small font
- Character count: Gray text, small font, right-aligned

**Acceptance Criteria**:
- [ ] Renders label, input, and error message
- [ ] Shows character count when enabled
- [ ] Applies error styling when error exists
- [ ] Supports all input types
- [ ] Accessible (label associated with input)

---

### TextArea

**Purpose**: Multiline text input with label and validation

**File**: `components/form/TextArea.tsx`

**Props**:
```typescript
interface TextAreaProps {
  id: string;
  name: string;
  label: string;
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  error?: string;
  required?: boolean;
  maxLength?: number;
  showCharCount?: boolean;
  rows?: number;  // Default: 4
  disabled?: boolean;
}
```

**Behavior**: Same as Input, but with textarea element

**Acceptance Criteria**:
- [ ] Renders label, textarea, and error message
- [ ] Shows character count when enabled
- [ ] Applies error styling when error exists
- [ ] Accessible (label associated with textarea)

---

### Select

**Purpose**: Dropdown select input with label and validation

**File**: `components/form/Select.tsx`

**Props**:
```typescript
interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  id: string;
  name: string;
  label: string;
  options: SelectOption[];
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
}
```

**Behavior**:
- Render label above select
- Display options from `options` prop
- Apply error styling if error exists

**Acceptance Criteria**:
- [ ] Renders label, select, and error message
- [ ] Displays all options correctly
- [ ] Applies error styling when error exists
- [ ] Accessible (label associated with select)

---

### Button

**Purpose**: Reusable button with variants and loading state

**File**: `components/form/Button.tsx`

**Props**:
```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';  // Default: 'primary'
  type?: 'button' | 'submit' | 'reset';  // Default: 'button'
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;  // Show loading spinner
  fullWidth?: boolean;  // Full width on mobile
}
```

**Variants**:
- **Primary**: Filled button, primary color background
- **Secondary**: Outlined button, transparent background
- **Danger**: Filled button, red background (for delete actions)

**Behavior**:
- If `loading` is true, show spinner and disable button
- If `disabled` is true, apply disabled styling and prevent clicks
- If `fullWidth` is true, button takes full width on mobile

**Styling**:
- Primary: Blue background, white text
- Secondary: Blue border, blue text, transparent background
- Danger: Red background, white text
- Disabled: Gray background, gray text, cursor not-allowed
- Loading: Show spinner icon, disable interactions

**Acceptance Criteria**:
- [ ] Renders with correct variant styling
- [ ] Shows loading spinner when loading=true
- [ ] Disabled when loading or disabled prop is true
- [ ] Full width on mobile when fullWidth=true
- [ ] Accessible (keyboard navigation, focus indicators)

---

### Form

**Purpose**: Form wrapper with onSubmit handling and validation

**File**: `components/form/Form.tsx`

**Props**:
```typescript
interface FormProps {
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  error?: string;  // General form error (displayed at top)
}
```

**Behavior**:
- Prevent default form submission
- Call `onSubmit` handler
- Display general error message at top if provided

**Acceptance Criteria**:
- [ ] Prevents default form submission
- [ ] Calls onSubmit handler
- [ ] Displays general error message

---

## Task Components

### TaskCard

**Purpose**: Display a single task in card/list format

**File**: `components/task/TaskCard.tsx`

**Props**:
```typescript
interface TaskCardProps {
  task: {
    id: number;
    title: string;
    description: string | null;
    status: 'pending' | 'in_progress' | 'completed';
    created_at: string;
  };
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}
```

**Layout**:
- Title (large, bold)
- Status badge (colored pill)
- Description (truncated to 100 chars with "..." if longer)
- Created date (relative format: "2 hours ago")
- Action buttons: Edit, Delete

**Status Badge**:
- `pending`: Gray background, gray text
- `in_progress`: Blue background, white text
- `completed`: Green background, white text

**Actions**:
- Edit button: Calls `onEdit(task.id)`
- Delete button: Calls `onDelete(task.id)`

**Styling**:
- Card: Border, shadow, padding, rounded corners
- Hover: Slight elevation/shadow increase

**Acceptance Criteria**:
- [ ] Renders all task fields correctly
- [ ] Status badge displays with correct color
- [ ] Description truncated to 100 chars
- [ ] Created date in relative format
- [ ] Edit and delete buttons call handlers
- [ ] Accessible (keyboard navigation, focus indicators)

---

### TaskList

**Purpose**: Display a list of TaskCard components

**File**: `components/task/TaskList.tsx`

**Props**:
```typescript
interface TaskListProps {
  tasks: Array<{
    id: number;
    title: string;
    description: string | null;
    status: 'pending' | 'in_progress' | 'completed';
    created_at: string;
  }>;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  emptyMessage?: string;  // Message shown when tasks array is empty
}
```

**Behavior**:
- If `tasks` is empty, show empty state message
- Otherwise, render TaskCard for each task

**Layout**:
- Desktop: Grid layout (2-3 columns)
- Mobile: Single column (stacked)

**Acceptance Criteria**:
- [ ] Renders TaskCard for each task
- [ ] Shows empty state when tasks array is empty
- [ ] Responsive grid layout
- [ ] Passes handlers to TaskCard correctly

---

### StatusBadge

**Purpose**: Display task status as colored badge

**File**: `components/task/StatusBadge.tsx`

**Props**:
```typescript
interface StatusBadgeProps {
  status: 'pending' | 'in_progress' | 'completed';
}
```

**Behavior**:
- Display status text with appropriate color
- Capitalize and format status (e.g., "in_progress" → "In Progress")

**Colors**:
- `pending`: Gray background, gray text
- `in_progress`: Blue background, white text
- `completed`: Green background, white text

**Styling**:
- Pill shape (rounded full)
- Small padding
- Uppercase text or capitalized

**Acceptance Criteria**:
- [ ] Displays correct color for each status
- [ ] Formats status text correctly
- [ ] Pill-shaped badge

---

## Feedback Components

### Alert

**Purpose**: Display informational, warning, or error messages

**File**: `components/feedback/Alert.tsx`

**Props**:
```typescript
interface AlertProps {
  type: 'info' | 'success' | 'warning' | 'error';
  message: string;
  onClose?: () => void;  // Optional close handler
}
```

**Types**:
- **Info**: Blue background, info icon
- **Success**: Green background, checkmark icon
- **Warning**: Yellow background, warning icon
- **Error**: Red background, error icon

**Layout**:
- Icon on left
- Message text in center
- Close button on right (if `onClose` provided)

**Acceptance Criteria**:
- [ ] Displays correct color and icon for each type
- [ ] Shows message text
- [ ] Close button calls onClose handler
- [ ] Accessible (ARIA role="alert")

---

### Toast

**Purpose**: Temporary notification message (auto-dismiss)

**File**: `components/feedback/Toast.tsx`

**Props**:
```typescript
interface ToastProps {
  message: string;
  type?: 'info' | 'success' | 'error';  // Default: 'info'
  duration?: number;  // Auto-dismiss after milliseconds, default: 3000
  onClose: () => void;
}
```

**Behavior**:
- Display message with appropriate color
- Auto-dismiss after `duration` milliseconds
- Manual close button

**Position**: Fixed bottom-right corner

**Acceptance Criteria**:
- [ ] Displays with correct color
- [ ] Auto-dismisses after duration
- [ ] Close button works
- [ ] Accessible (ARIA live region)

---

### LoadingSpinner

**Purpose**: Indicate loading state

**File**: `components/feedback/LoadingSpinner.tsx`

**Props**:
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';  // Default: 'md'
  color?: string;  // Default: primary color
}
```

**Behavior**:
- Render spinning animation (CSS animation or SVG)

**Sizes**:
- `sm`: 16px
- `md`: 24px
- `lg`: 48px

**Acceptance Criteria**:
- [ ] Renders spinning animation
- [ ] Correct size based on prop
- [ ] Accessible (ARIA label)

---

### Modal

**Purpose**: Overlay dialog for confirmations or forms

**File**: `components/feedback/Modal.tsx`

**Props**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;  // Optional footer with action buttons
}
```

**Behavior**:
- Display overlay (semi-transparent background)
- Center modal dialog
- Show title, children (content), and footer
- Close on overlay click or ESC key

**Styling**:
- Overlay: Dark semi-transparent background
- Dialog: White background, shadow, rounded corners
- Title: Bold, large
- Footer: Right-aligned buttons

**Acceptance Criteria**:
- [ ] Renders when isOpen=true
- [ ] Hidden when isOpen=false
- [ ] Closes on overlay click
- [ ] Closes on ESC key press
- [ ] Accessible (ARIA role="dialog", focus trap)

---

## Utility Components

### ProtectedRoute

**Purpose**: Redirect unauthenticated users to login

**File**: `components/utility/ProtectedRoute.tsx`

**Props**:
```typescript
interface ProtectedRouteProps {
  children: React.ReactNode;
}
```

**Behavior**:
- Check for JWT token in localStorage or cookie
- If no token or expired, redirect to `/` (login page)
- If valid token, render children

**Implementation**:
```typescript
"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function ProtectedRoute({ children }) {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
    }
  }, [router]);

  return <>{children}</>;
}
```

**Acceptance Criteria**:
- [ ] Redirects to login if no token
- [ ] Renders children if token exists

---

### ErrorBoundary

**Purpose**: Catch and display React errors gracefully

**File**: `components/utility/ErrorBoundary.tsx`

**Props**:
```typescript
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;  // Optional custom error UI
}
```

**Behavior**:
- Catch JavaScript errors in child components
- Display fallback UI or default error message
- Log error to console (or error tracking service)

**Default Fallback**:
- Message: "Something went wrong. Please refresh the page."
- Button: "Refresh Page"

**Acceptance Criteria**:
- [ ] Catches errors in child components
- [ ] Displays fallback UI
- [ ] Logs error to console

---

## Component Composition Examples

### Login Form Composition

```typescript
<Form onSubmit={handleLogin} error={formError}>
  <Input
    id="email"
    name="email"
    label="Email"
    type="email"
    value={email}
    onChange={(e) => setEmail(e.target.value)}
    error={emailError}
    required
  />
  <Input
    id="password"
    name="password"
    label="Password"
    type="password"
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    error={passwordError}
    required
  />
  <Button type="submit" loading={isLoading}>
    Login
  </Button>
</Form>
```

### Task List Page Composition

```typescript
<PageContainer maxWidth="lg">
  <NavBar userEmail={user.email} onLogout={handleLogout} />

  <h1>My Tasks</h1>

  <Button variant="primary" onClick={() => router.push('/dashboard/new')}>
    New Task
  </Button>

  <TaskList
    tasks={tasks}
    onEdit={(id) => router.push(`/dashboard/${id}`)}
    onDelete={handleDelete}
    emptyMessage="No tasks yet. Create your first task!"
  />
</PageContainer>
```

---

## Styling Approach

### Option 1: TailwindCSS (Recommended)

**Pros**:
- Utility-first CSS
- Fast development
- Consistent design system
- Built-in responsive utilities

**Configuration**:
```javascript
// tailwind.config.js
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#64748B',
        danger: '#EF4444',
        success: '#10B981',
      },
    },
  },
};
```

### Option 2: CSS Modules

**Pros**:
- Scoped styles
- No class name conflicts
- Familiar CSS syntax

**Example**:
```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
}

.primary {
  background-color: #3B82F6;
  color: white;
}
```

---

## TypeScript Types

**Shared Types** (`types/index.ts`):
```typescript
export type TaskStatus = 'pending' | 'in_progress' | 'completed';

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  email: string;
  created_at: string;
}
```

---

## Accessibility Standards

**WCAG 2.1 Level AA Compliance**:
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation: All interactive elements focusable
- Focus indicators: Visible focus outlines
- ARIA labels: Descriptive labels for screen readers
- Semantic HTML: Use correct HTML elements (button, input, form, etc.)

**Testing**:
- Manual keyboard navigation testing
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Automated accessibility testing (axe, Lighthouse)

---

## Acceptance Criteria Summary

**All components are DONE when**:
- [ ] All specified components implemented
- [ ] TypeScript props interfaces defined
- [ ] Accessibility standards met
- [ ] Responsive design works on all screen sizes
- [ ] Reusable and composable
- [ ] Unit tests written (optional for MVP)
- [ ] Storybook stories created (optional)

---

## References

- See: `specs/ui/pages.md` (Page usage of components)
- See: `specs/features/authentication.md` (Auth form requirements)
- See: `specs/features/task-crud.md` (Task component requirements)
- [React Documentation](https://react.dev/)
- [Next.js Documentation](https://nextjs.org/docs)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
