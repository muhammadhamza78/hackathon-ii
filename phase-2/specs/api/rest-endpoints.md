# REST API Endpoints Specification

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Status:** Specification

## Overview

Complete specification of all REST API endpoints for the Task Management System. All endpoints follow REST conventions and use JSON for request/response payloads.

## Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: TBD

## Global Headers

### Request Headers

**All Requests**:
- `Content-Type: application/json`

**Authenticated Requests**:
- `Authorization: Bearer <JWT_TOKEN>`

### Response Headers

**All Responses**:
- `Content-Type: application/json`

## Authentication Endpoints

### POST /api/auth/register

**Description**: Create a new user account

**Authentication**: Not required

**Request**:
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Request Schema**:
```typescript
{
  email: string;      // Required, email format, max 255 chars, unique
  password: string;   // Required, min 8 chars, max 128 chars
}
```

**Success Response (201 Created)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Response Schema**:
```typescript
{
  id: number;
  email: string;
  created_at: string;  // ISO8601 datetime
}
```

**Error Responses**:

**400 Bad Request** - Email already exists:
```json
{
  "detail": "Email already registered"
}
```

**422 Validation Error** - Invalid input:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Status Codes**:
- 201: User created successfully
- 400: Email already exists
- 422: Validation error

---

### POST /api/auth/login

**Description**: Authenticate user and receive JWT token

**Authentication**: Not required

**Request**:
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Request Schema**:
```typescript
{
  email: string;      // Required
  password: string;   // Required
}
```

**Success Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzM1NzM2NDAwLCJpYXQiOjE3MzU2NTAwMDB9.signature",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**Response Schema**:
```typescript
{
  access_token: string;   // JWT token
  token_type: string;     // Always "Bearer"
  expires_in: number;     // Token expiry in seconds
}
```

**Error Responses**:

**401 Unauthorized** - Invalid credentials:
```json
{
  "detail": "Invalid credentials"
}
```

**422 Validation Error** - Missing fields:
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Status Codes**:
- 200: Login successful
- 401: Invalid email or password
- 422: Validation error

---

## Task Endpoints

### POST /api/tasks

**Description**: Create a new task for the authenticated user

**Authentication**: Required (JWT)

**Request**:
```http
POST /api/tasks
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

**Request Schema**:
```typescript
{
  title: string;            // Required, max 200 chars
  description?: string;     // Optional, max 2000 chars
  status?: "pending" | "in_progress" | "completed";  // Optional, defaults to "pending"
}
```

**Success Response (201 Created)**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "user_id": 1,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Response Schema**:
```typescript
{
  id: number;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  user_id: number;
  created_at: string;   // ISO8601 datetime
  updated_at: string;   // ISO8601 datetime
}
```

**Error Responses**:

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Unauthorized"
}
```

**422 Validation Error** - Invalid input:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length",
      "ctx": {"limit_value": 200}
    }
  ]
}
```

**Status Codes**:
- 201: Task created successfully
- 401: Unauthorized (missing/invalid token)
- 422: Validation error

---

### GET /api/tasks

**Description**: List all tasks for the authenticated user

**Authentication**: Required (JWT)

**Request**:
```http
GET /api/tasks
Authorization: Bearer <TOKEN>
```

**Query Parameters**: None (filtering/pagination out of scope for MVP)

**Success Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "pending",
      "user_id": 1,
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Write report",
      "description": null,
      "status": "in_progress",
      "user_id": 1,
      "created_at": "2025-12-30T11:00:00Z",
      "updated_at": "2025-12-30T11:30:00Z"
    }
  ]
}
```

**Response Schema**:
```typescript
{
  tasks: Array<{
    id: number;
    title: string;
    description: string | null;
    status: "pending" | "in_progress" | "completed";
    user_id: number;
    created_at: string;
    updated_at: string;
  }>;
}
```

**Error Responses**:

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Unauthorized"
}
```

**Status Codes**:
- 200: Tasks retrieved successfully
- 401: Unauthorized

---

### GET /api/tasks/{task_id}

**Description**: Get a single task by ID (only if owned by authenticated user)

**Authentication**: Required (JWT)

**Request**:
```http
GET /api/tasks/1
Authorization: Bearer <TOKEN>
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "user_id": 1,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Response Schema**:
```typescript
{
  id: number;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  user_id: number;
  created_at: string;
  updated_at: string;
}
```

**Error Responses**:

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Unauthorized"
}
```

**404 Not Found** - Task not found or not owned by user:
```json
{
  "detail": "Task not found"
}
```

**Status Codes**:
- 200: Task retrieved successfully
- 401: Unauthorized
- 404: Task not found or not owned by user

---

### PUT /api/tasks/{task_id}

**Description**: Update an existing task (only if owned by authenticated user)

**Authentication**: Required (JWT)

**Request**:
```http
PUT /api/tasks/1
Authorization: Bearer <TOKEN>
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": "in_progress"
}
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Request Schema** (all fields optional):
```typescript
{
  title?: string;       // Optional, max 200 chars
  description?: string; // Optional, max 2000 chars, can be null to clear
  status?: "pending" | "in_progress" | "completed";  // Optional
}
```

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "status": "in_progress",
  "user_id": 1,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Response Schema**:
```typescript
{
  id: number;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  user_id: number;
  created_at: string;
  updated_at: string;
}
```

**Error Responses**:

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Unauthorized"
}
```

**404 Not Found** - Task not found or not owned by user:
```json
{
  "detail": "Task not found"
}
```

**422 Validation Error** - Invalid input:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

**Status Codes**:
- 200: Task updated successfully
- 401: Unauthorized
- 404: Task not found or not owned by user
- 422: Validation error

---

### DELETE /api/tasks/{task_id}

**Description**: Delete a task (only if owned by authenticated user)

**Authentication**: Required (JWT)

**Request**:
```http
DELETE /api/tasks/1
Authorization: Bearer <TOKEN>
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Success Response (204 No Content)**:
No response body.

**Error Responses**:

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Unauthorized"
}
```

**404 Not Found** - Task not found or not owned by user:
```json
{
  "detail": "Task not found"
}
```

**Status Codes**:
- 204: Task deleted successfully
- 401: Unauthorized
- 404: Task not found or not owned by user

---

## Health Check Endpoint

### GET /health

**Description**: Health check endpoint for monitoring

**Authentication**: Not required

**Request**:
```http
GET /health
```

**Success Response (200 OK)**:
```json
{
  "status": "ok",
  "database": "connected"
}
```

**Response Schema**:
```typescript
{
  status: "ok" | "degraded" | "down";
  database: "connected" | "disconnected";
}
```

**Status Codes**:
- 200: Service healthy
- 503: Service unavailable (database disconnected)

---

## Common Error Responses

### 401 Unauthorized

**Causes**:
- Missing Authorization header
- Invalid token format
- Invalid token signature
- Expired token

**Response**:
```json
{
  "detail": "Unauthorized"
}
```

### 404 Not Found

**Causes**:
- Resource not found
- Resource exists but belongs to different user (for isolation)

**Response**:
```json
{
  "detail": "Task not found"
}
```

### 422 Validation Error

**Causes**:
- Missing required fields
- Invalid data types
- Constraint violations (max length, format, etc.)

**Response Format**:
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

### 500 Internal Server Error

**Causes**:
- Unhandled server exceptions
- Database connectivity issues

**Response**:
```json
{
  "detail": "Internal server error"
}
```

**Note**: Detailed error messages should NOT be exposed in production.

---

## CORS Configuration

**Allowed Origins** (Development):
- `http://localhost:3000` (Next.js frontend)

**Allowed Methods**:
- GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers**:
- Authorization, Content-Type

**Credentials**:
- Allowed (for cookies, if needed in future)

---

## Rate Limiting

**Not implemented in MVP.**

**Future**:
- 100 requests per minute per IP for auth endpoints
- 1000 requests per minute per user for task endpoints

---

## API Versioning

**Current Version**: v1 (implicit, no version in URL)

**Future Versioning Strategy**:
- Breaking changes: `/api/v2/tasks`
- Non-breaking changes: Add optional fields, new endpoints
- Support two versions simultaneously during migration

---

## OpenAPI Documentation

**Auto-Generated**: FastAPI automatically generates OpenAPI (Swagger) documentation.

**Documentation URL**: `http://localhost:8000/docs`

**ReDoc URL**: `http://localhost:8000/redoc`

**OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Type Definitions (TypeScript)

**For Frontend Consumption**:

```typescript
// Auth Types
export interface RegisterRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  id: number;
  email: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// Task Types
export type TaskStatus = "pending" | "in_progress" | "completed";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  status?: TaskStatus;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string | null;
  status?: TaskStatus;
}

export interface TaskListResponse {
  tasks: Task[];
}

// Error Types
export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

export interface ErrorResponse {
  detail: string | ValidationError[];
}
```

---

## Testing

### Acceptance Criteria

- [ ] All endpoints return correct status codes
- [ ] All endpoints return correct response schemas
- [ ] All validation rules are enforced
- [ ] User isolation is enforced (cross-user access returns 404)
- [ ] Authentication is required for protected endpoints
- [ ] Error responses follow consistent format
- [ ] OpenAPI documentation is accurate

### Test Coverage

- Unit tests for request/response validation
- Integration tests for all endpoints
- Security tests for user isolation
- Performance tests for response times

---

## References

- See: `specs/features/authentication.md` (Authentication details)
- See: `specs/features/task-crud.md` (Task CRUD details)
- See: `specs/architecture.md` (API contracts and error taxonomy)
- See: `specs/database/schema.md` (Data models)

---

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
