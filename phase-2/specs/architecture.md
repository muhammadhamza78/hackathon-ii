# Hackathon-II Phase-2: System Architecture

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Status:** Specification

## 1. Scope and Dependencies

### In Scope

**Backend:**
- FastAPI REST API server with JWT authentication middleware
- SQLModel ORM for database operations
- User and Task data models
- Authentication endpoints (register, login)
- Task CRUD endpoints with user isolation
- Database connection and session management
- Request/response validation with Pydantic

**Frontend:**
- Next.js 16+ App Router application
- Authentication pages (login, register)
- Task management dashboard
- Client-side JWT token management
- API client for backend communication
- TypeScript types for API contracts

**Database:**
- Neon Serverless PostgreSQL instance
- User table with credentials
- Task table with foreign key to users
- Proper indexing for performance

**Infrastructure:**
- Local development environment
- Environment configuration (.env files)
- Database migrations (Alembic)

### Out of Scope

- Deployment infrastructure and CI/CD
- Email services for verification
- Third-party OAuth providers
- Real-time features (WebSockets)
- File storage or attachments
- Caching layer (Redis)
- Load balancing or CDN
- Monitoring and observability (initial phase)

### External Dependencies

| Dependency | Purpose | Owner/Source | Version |
|------------|---------|--------------|---------|
| Neon PostgreSQL | Database hosting | Neon.tech | Latest |
| Better Auth | JWT authentication library | Better Auth | Latest stable |
| FastAPI | Backend framework | Tiangolo | 0.104+ |
| SQLModel | ORM and validation | Tiangolo | 0.0.14+ |
| Next.js | Frontend framework | Vercel | 16+ |
| TypeScript | Type safety | Microsoft | 5.3+ |
| Python | Backend runtime | Python.org | 3.11+ |
| Node.js | Frontend runtime | Node.js | 20+ LTS |

## 2. Key Decisions and Rationale

### Decision 1: API-First Architecture with Separate Frontend/Backend

**Options Considered:**
1. Monolithic Next.js with API routes and database access
2. Separate FastAPI backend with Next.js frontend (SELECTED)
3. Serverless functions (AWS Lambda, Vercel Functions)

**Trade-offs:**
- **Option 1** (Monolithic): Simpler deployment, but couples frontend and backend, harder to scale independently
- **Option 2** (Separate): Clean separation, independent scaling, API reusability, but requires CORS configuration
- **Option 3** (Serverless): Auto-scaling, but cold starts, vendor lock-in, harder local development

**Rationale:**
Selected Option 2 for:
- Clear separation of concerns (constitution principle IV)
- Independent development and testing
- API can be reused for mobile apps or other clients
- FastAPI provides automatic OpenAPI documentation
- Easier to enforce API contracts and type safety

**Principles Applied:**
- API-First Architecture (Constitution IV)
- Type Safety (Constitution V)
- Spec-First Development (Constitution I)

### Decision 2: JWT-Based Stateless Authentication

**Options Considered:**
1. Session-based authentication with server-side session store
2. JWT-based stateless authentication (SELECTED)
3. OAuth 2.0 with authorization server

**Trade-offs:**
- **Option 1** (Sessions): Server-side session invalidation, but requires session store (Redis), scaling challenges
- **Option 2** (JWT): Stateless, scalable, but token cannot be invalidated before expiry
- **Option 3** (OAuth): Industry standard, but overkill for simple use case

**Rationale:**
Selected Option 2 for:
- Stateless authentication aligns with API-first approach
- No additional infrastructure (session store) required
- Better Auth provides JWT utilities out of the box
- Simpler implementation for MVP
- Token expiry mitigates revocation issue (short-lived tokens)

**Principles Applied:**
- JWT Authentication Mandatory (Constitution II)
- Simplicity (avoiding unnecessary infrastructure)

### Decision 3: SQLModel for ORM

**Options Considered:**
1. SQLAlchemy (pure ORM)
2. SQLModel (SELECTED)
3. Raw SQL with database drivers

**Trade-offs:**
- **Option 1** (SQLAlchemy): Mature, feature-rich, but verbose schema definition, separate Pydantic models needed
- **Option 2** (SQLModel): Combines SQLAlchemy ORM + Pydantic validation, less boilerplate
- **Option 3** (Raw SQL): Maximum control, but no type safety, manual query building, SQL injection risks

**Rationale:**
Selected Option 2 for:
- Single model definition for database and API validation
- Type safety across database and API layer (Constitution V)
- Automatic Pydantic integration for FastAPI
- Maintained by FastAPI author (consistent ecosystem)
- Reduces code duplication

**Principles Applied:**
- Type Safety (Constitution V)
- API-First Architecture (Constitution IV)

### Decision 4: User Data Isolation at Query Level

**Options Considered:**
1. Application-level filtering in business logic
2. Database row-level security (RLS)
3. Query-level filtering with user_id from JWT (SELECTED)

**Trade-offs:**
- **Option 1** (App-level): Easy to implement, but easy to forget, prone to developer error
- **Option 2** (Database RLS): Strongest guarantee, but Neon support unclear, adds complexity
- **Option 3** (Query-level): Enforced in data access layer, testable, clear audit trail

**Rationale:**
Selected Option 3 for:
- Explicit filtering in every query makes isolation visible
- Easier to test and audit
- No reliance on database-specific features (portable)
- User ID extracted from JWT ensures authenticity
- Fails closed (missing filter returns empty, not all data)

**Principles Applied:**
- User Data Isolation (Constitution III - NON-NEGOTIABLE)
- Test Coverage (Constitution VI)

### Decision 5: Next.js App Router (vs Pages Router)

**Options Considered:**
1. Next.js Pages Router (older stable pattern)
2. Next.js App Router (SELECTED)

**Trade-offs:**
- **Option 1** (Pages): More mature, broader community examples, simpler mental model
- **Option 2** (App Router): Modern React patterns, server components, better performance, future direction

**Rationale:**
Selected Option 2 for:
- User requirement specifies Next.js 16+ with App Router
- Server components enable better performance
- Streaming and suspense for improved UX
- Aligns with Next.js future direction
- Better data fetching patterns

**Principles Applied:**
- Technology Stack mandate (Constitution)
- Modern best practices

## 3. Interfaces and API Contracts

### Public API Endpoints

All endpoints except authentication must include:
- **Header**: `Authorization: Bearer <JWT_TOKEN>`
- **Error Response (401)**: `{"detail": "Unauthorized"}`

#### Authentication Endpoints

**POST /api/auth/register**
- **Purpose**: Create new user account
- **Input**:
  ```json
  {
    "email": "string (email format, max 255 chars)",
    "password": "string (min 8 chars, max 128 chars)"
  }
  ```
- **Output (201)**:
  ```json
  {
    "id": "integer",
    "email": "string",
    "created_at": "ISO8601 datetime"
  }
  ```
- **Errors**:
  - 400: Email already exists
  - 422: Validation error (invalid email, weak password)

**POST /api/auth/login**
- **Purpose**: Authenticate user and receive JWT token
- **Input**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Output (200)**:
  ```json
  {
    "access_token": "string (JWT)",
    "token_type": "Bearer",
    "expires_in": "integer (seconds)"
  }
  ```
- **Errors**:
  - 401: Invalid credentials
  - 422: Validation error

#### Task Endpoints

**POST /api/tasks**
- **Purpose**: Create new task for authenticated user
- **Auth**: Required (JWT)
- **Input**:
  ```json
  {
    "title": "string (required, max 200 chars)",
    "description": "string (optional, max 2000 chars)",
    "status": "pending | in_progress | completed (default: pending)"
  }
  ```
- **Output (201)**:
  ```json
  {
    "id": "integer",
    "title": "string",
    "description": "string | null",
    "status": "string",
    "user_id": "integer",
    "created_at": "ISO8601 datetime",
    "updated_at": "ISO8601 datetime"
  }
  ```
- **Errors**:
  - 401: Unauthorized (missing/invalid token)
  - 422: Validation error

**GET /api/tasks**
- **Purpose**: List all tasks for authenticated user
- **Auth**: Required (JWT)
- **Query Params**: None (filtering out of scope for MVP)
- **Output (200)**:
  ```json
  {
    "tasks": [
      {
        "id": "integer",
        "title": "string",
        "description": "string | null",
        "status": "string",
        "user_id": "integer",
        "created_at": "ISO8601 datetime",
        "updated_at": "ISO8601 datetime"
      }
    ]
  }
  ```
- **Errors**:
  - 401: Unauthorized

**GET /api/tasks/{task_id}**
- **Purpose**: Get single task by ID (only if owned by authenticated user)
- **Auth**: Required (JWT)
- **Path Params**: task_id (integer)
- **Output (200)**: Same as single task object above
- **Errors**:
  - 401: Unauthorized
  - 404: Task not found or not owned by user

**PUT /api/tasks/{task_id}**
- **Purpose**: Update existing task (only if owned by authenticated user)
- **Auth**: Required (JWT)
- **Path Params**: task_id (integer)
- **Input**:
  ```json
  {
    "title": "string (optional, max 200 chars)",
    "description": "string (optional, max 2000 chars)",
    "status": "pending | in_progress | completed (optional)"
  }
  ```
- **Output (200)**: Updated task object
- **Errors**:
  - 401: Unauthorized
  - 404: Task not found or not owned by user
  - 422: Validation error

**DELETE /api/tasks/{task_id}**
- **Purpose**: Delete task (only if owned by authenticated user)
- **Auth**: Required (JWT)
- **Path Params**: task_id (integer)
- **Output (204)**: No content
- **Errors**:
  - 401: Unauthorized
  - 404: Task not found or not owned by user

### Versioning Strategy

**Initial Version**: v1 (implicit, no version in URL for MVP)

**Future Versioning**:
- Breaking changes: `/api/v2/tasks`
- Non-breaking changes: Add optional fields, new endpoints
- Deprecation: 3-month notice, support two versions simultaneously

### Idempotency, Timeouts, Retries

**Idempotency**:
- GET, PUT, DELETE: Naturally idempotent
- POST (create task): NOT idempotent (creates new task each time)
- Future: Consider idempotency keys for POST operations

**Timeouts**:
- Client-side timeout: 30 seconds
- Database query timeout: 10 seconds

**Retries**:
- Client should retry on network errors (exponential backoff)
- Client should NOT retry on 4xx errors (client errors)
- Client MAY retry on 500, 502, 503, 504 (server errors)

### Error Taxonomy

| Status Code | Meaning | Client Action |
|-------------|---------|---------------|
| 200 | Success | Process response |
| 201 | Created | Process response |
| 204 | No Content | Success, no body |
| 400 | Bad Request | Fix request, don't retry |
| 401 | Unauthorized | Re-authenticate |
| 404 | Not Found | Resource missing or no access |
| 422 | Validation Error | Fix input, don't retry |
| 500 | Server Error | Retry with backoff |
| 502, 503, 504 | Gateway/Service Error | Retry with backoff |

**Error Response Format** (4xx, 5xx):
```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_ERROR_CODE",
  "validation_errors": [
    {
      "field": "field_name",
      "message": "error message"
    }
  ]
}
```

## 4. Non-Functional Requirements (NFRs) and Budgets

### Performance

**Latency Targets**:
- API response time (p95): < 500ms
- Database query time (p95): < 100ms
- Frontend page load (p95): < 2 seconds

**Throughput**:
- Minimum: 100 req/sec (MVP)
- Target: 1000 req/sec (future)

**Resource Caps**:
- Database connections: Max 10 concurrent (Neon free tier)
- API server memory: < 512MB
- Frontend bundle size: < 500KB (gzipped)

### Reliability

**SLOs** (Service Level Objectives):
- Availability: 99% uptime (MVP acceptable)
- Error rate: < 1% of requests
- Data durability: 99.99% (Neon guarantee)

**Error Budget**:
- Allowed downtime: ~7 hours/month
- Allowed errors: < 1 in 100 requests

**Degradation Strategy**:
- Database unavailable: Return 503 with retry-after header
- Slow queries: Implement query timeout, return 504
- Rate limiting: Not implemented in MVP

### Security

**Authentication (AuthN)**:
- JWT tokens with HS256 algorithm
- Token expiry: 24 hours (configurable)
- Password hashing: bcrypt (cost factor 12) or argon2

**Authorization (AuthZ)**:
- User ID extracted from JWT token
- All queries filter by user_id
- No role-based access control (RBAC) in MVP

**Data Handling**:
- Passwords: Never logged, never returned in API responses
- JWT secret: Stored in environment variable, never committed
- Database credentials: Stored in environment variable

**Secrets Management**:
- Local: .env file (git-ignored)
- Production: Environment variables (deployment platform)

**Auditing**:
- Log all authentication attempts (success/failure)
- Log all data modification operations (create, update, delete)
- Include user_id in all audit logs

### Cost

**Unit Economics** (per user/month):
- Database: Neon free tier (512MB storage, 0.5 vCPU) = $0
- Backend hosting: Estimated $5-10/month (VPS or serverless)
- Frontend hosting: Vercel free tier or similar = $0
- Total: < $10/month for MVP

**Cost Optimization**:
- Use connection pooling to reduce database connections
- Optimize queries to reduce database CPU usage
- Use Next.js static generation where possible

## 5. Data Management and Migration

### Source of Truth

**Database**: Neon PostgreSQL is the single source of truth for all persistent data.

**Schema Definition**: SQLModel models in `backend/app/models/` are the authoritative schema definition.

### Schema Evolution

**Process**:
1. Update SQLModel model in code
2. Generate Alembic migration: `alembic revision --autogenerate -m "description"`
3. Review migration SQL
4. Test migration on dev database
5. Apply to production: `alembic upgrade head`

**Naming Convention**:
- Migrations: `YYYYMMDD_HHMM_description.py`
- Example: `20251230_1200_add_task_status.py`

### Migration and Rollback

**Migration Strategy**:
- Backward-compatible changes: Apply immediately
- Breaking changes: Multi-step migration (add column, migrate data, remove old column)

**Rollback Strategy**:
- Every migration MUST have a downgrade path
- Test rollback on dev database before production
- Rollback command: `alembic downgrade -1`

**Data Preservation**:
- Soft deletes for critical data (users, tasks)
- Backup before major migrations
- Retention: 30 days minimum

### Data Retention

**User Data**:
- Active users: Retained indefinitely
- Deleted users: Soft delete for 30 days, then hard delete

**Task Data**:
- Active tasks: Retained indefinitely
- Deleted tasks: Soft delete for 7 days, then hard delete
- Cascade: User deletion → all associated tasks deleted

**Audit Logs**:
- Retention: 90 days
- Rotation: Monthly archives

## 6. Operational Readiness

### Observability

**Logging**:
- Format: JSON structured logs
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Required fields: timestamp, level, message, user_id (if applicable), request_id
- Destination: stdout (captured by deployment platform)

**Metrics**:
- API request count (by endpoint, status code)
- API response time (p50, p95, p99)
- Database connection pool usage
- Authentication success/failure rate

**Traces**:
- Not implemented in MVP
- Future: OpenTelemetry for distributed tracing

### Alerting

**Critical Alerts**:
- Error rate > 5% (threshold: 5 errors in 5 minutes)
- API response time p95 > 2 seconds
- Database connection pool exhausted

**Warning Alerts**:
- Error rate > 1%
- API response time p95 > 1 second

**On-Call Owner**: TBD (post-deployment)

### Runbooks

**Common Tasks**:
1. **Database Migration**: See "Schema Evolution" section
2. **User Password Reset**: Manual SQL update (no UI in MVP)
3. **Rollback Deployment**: Revert to previous version, rollback database migration
4. **Scale Up**: Increase backend instances, adjust database connection pool

### Deployment and Rollback

**Deployment Strategy**:
- Blue-green deployment (zero downtime)
- Automated tests must pass before deployment
- Database migrations run before new code deployment

**Rollback Strategy**:
- Code rollback: Deploy previous version
- Database rollback: `alembic downgrade -1`
- Maximum rollback window: 24 hours

**Health Checks**:
- Endpoint: `GET /health`
- Response: `{"status": "ok", "database": "connected"}`

### Feature Flags

**Not implemented in MVP.**

**Future**:
- Use environment variables for simple flags
- Consider LaunchDarkly or similar for complex flag management

## 7. Risk Analysis and Mitigation

### Top 3 Risks

**Risk 1: User Data Isolation Breach**
- **Likelihood**: Medium (developer error)
- **Impact**: Critical (data leak, security breach)
- **Blast Radius**: All users
- **Mitigation**:
  - Comprehensive multi-user test scenarios
  - Code review checklist for user_id filtering
  - Automated test for every endpoint (attempt cross-user access)
- **Kill Switch**: Immediate deployment rollback, database audit

**Risk 2: JWT Secret Exposure**
- **Likelihood**: Low (if following best practices)
- **Impact**: Critical (all tokens compromised)
- **Blast Radius**: All users
- **Mitigation**:
  - Never commit secrets to git
  - Use environment variables
  - Secret rotation procedure documented
- **Kill Switch**: Rotate JWT secret, force all users to re-login

**Risk 3: Database Connection Exhaustion**
- **Likelihood**: Medium (under load)
- **Impact**: High (service unavailable)
- **Blast Radius**: All users
- **Mitigation**:
  - Connection pooling with max connections limit
  - Query timeout enforcement
  - Monitoring and alerting on connection pool usage
- **Kill Switch**: Restart backend service, scale up database

## 8. Evaluation and Validation

### Definition of Done

**Feature Complete**:
- All API endpoints implemented and tested
- All UI pages implemented and functional
- User isolation verified with multi-user tests
- All acceptance criteria met (see specs)

**Testing Complete**:
- Unit tests: > 80% coverage on business logic
- Integration tests: All API endpoints tested
- Security tests: User isolation verified
- Manual testing: All user flows tested

**Documentation Complete**:
- OpenAPI documentation generated
- README with setup instructions
- Database schema documented
- ADRs for major decisions

**Security Scans**:
- Dependency vulnerability scan (npm audit, pip-audit)
- No critical vulnerabilities
- SQL injection prevention verified

### Output Validation

**API Responses**:
- All responses match schema definitions
- No PII in logs
- Consistent error format

**Database**:
- No orphaned records (referential integrity)
- Proper indexing verified
- Query performance meets targets

**Frontend**:
- TypeScript type checking passes
- No console errors
- Responsive on mobile and desktop

## 9. Architectural Decision Records (ADRs)

The following ADRs will be created to document key decisions:

1. **ADR-001: API-First Architecture with Separate Backend/Frontend**
2. **ADR-002: JWT-Based Stateless Authentication**
3. **ADR-003: SQLModel for ORM and Validation**
4. **ADR-004: User Data Isolation at Query Level**
5. **ADR-005: Next.js App Router for Frontend**

Each ADR will be created using `/sp.adr <title>` command after planning phase.

## References

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Approval

This architecture specification must be reviewed and approved before proceeding to implementation planning.

**Specification Author**: AI Agent
**Review Date**: Pending
**Approval Status**: Pending User Review
