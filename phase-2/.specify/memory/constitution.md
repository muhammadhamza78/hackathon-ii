<!--
Sync Impact Report:
- Version change: initial → 1.0.0
- New principles: Spec-First Development, JWT Authentication, User Data Isolation, API-First Architecture, Type Safety, Test Coverage
- New sections: Technology Stack, Development Workflow
- Templates: ✅ Will align spec/plan/tasks templates with principles
- Follow-up: None
-->

# Hackathon-II Phase-2 Constitution

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)
All work MUST be done via Spec-Driven Development. No manual coding is allowed until complete specifications exist.

**Rules:**
- Every feature begins with a complete specification in `specs/`
- Specifications MUST be reviewed and approved before implementation
- Code MUST implement exactly what the spec defines - no more, no less
- Changes to requirements require spec updates first, then code changes

**Rationale:** Ensures alignment between requirements and implementation, prevents scope creep, and maintains traceability.

### II. JWT Authentication Mandatory
All API endpoints MUST require valid JWT authentication. No anonymous access is permitted except for authentication endpoints.

**Rules:**
- Every API request (except login/register) MUST validate JWT token
- Invalid or missing tokens MUST return 401 Unauthorized
- Token validation MUST happen at the middleware/dependency level
- Tokens MUST contain user_id for isolation enforcement

**Rationale:** Protects user data and ensures all actions are attributable to authenticated users.

### III. User Data Isolation (NON-NEGOTIABLE)
Every user MUST only access their own data. Cross-user data access is strictly prohibited.

**Rules:**
- All database queries MUST filter by authenticated user's ID
- API endpoints MUST enforce user_id from JWT, never from request body
- Creation operations MUST auto-assign user_id from JWT
- Unit and integration tests MUST verify isolation
- Violation of isolation is a critical security bug

**Rationale:** Fundamental security requirement for multi-tenant applications. Prevents unauthorized data access.

### IV. API-First Architecture
Backend and frontend MUST be developed independently with contract-first approach.

**Rules:**
- REST API endpoints MUST be fully specified before implementation
- API contracts (request/response schemas) are source of truth
- Frontend MUST consume only documented API endpoints
- Breaking changes to APIs require versioning or migration plan
- Mock APIs can be used during parallel development

**Rationale:** Enables parallel development, clear separation of concerns, and easier testing.

### V. Type Safety
Strong typing MUST be enforced on both frontend and backend.

**Rules:**
- Backend: SQLModel for data models, Pydantic for request/response validation
- Frontend: TypeScript with strict mode enabled
- No `any` types without explicit justification
- Shared types should be generated from backend schemas where possible
- Type errors MUST be resolved before merge

**Rationale:** Prevents runtime errors, improves maintainability, and provides better IDE support.

### VI. Test Coverage
Critical paths MUST have automated test coverage.

**Rules:**
- Authentication flows: unit and integration tests required
- User isolation: MUST be tested with multi-user scenarios
- CRUD operations: unit tests for business logic, integration tests for API
- Database migrations: MUST be tested and reversible
- Tests MUST pass before merge

**Rationale:** Ensures reliability, prevents regressions, and documents expected behavior.

## Technology Stack

**Mandated Technologies:**
- **Frontend:** Next.js 16+ (App Router pattern)
- **Backend:** FastAPI (Python 3.11+)
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth (JWT-based)
- **Language:** TypeScript (frontend), Python (backend)

**Technology Decisions:**
- Next.js App Router for modern React patterns and server components
- FastAPI for async Python with automatic OpenAPI documentation
- SQLModel for type-safe ORM with Pydantic integration
- Neon for serverless PostgreSQL with branching capabilities
- Better Auth for modern, secure authentication with JWT

**Constraints:**
- No alternative frameworks or databases without approval
- All dependencies MUST be declared in package.json/requirements.txt
- Security patches MUST be applied within 7 days of disclosure

## Development Workflow

**Spec → Plan → Tasks → Implementation:**
1. **Specify** (`/sp.specify`): Create feature specification with requirements, constraints, and acceptance criteria
2. **Plan** (`/sp.plan`): Design architecture, identify components, define interfaces
3. **Tasks** (`/sp.tasks`): Break down into atomic, testable tasks with clear acceptance criteria
4. **Implement** (`/sp.implement`): Execute tasks following TDD principles
5. **Review**: Validate implementation against spec, run full test suite
6. **Document**: Create ADRs for architectural decisions, PHRs for prompt history

**Quality Gates:**
- Spec completeness review before planning
- Architecture review before task breakdown
- Code review against spec requirements
- All tests passing before merge
- User isolation verification before merge

**Branching Strategy:**
- `main`: production-ready code
- Feature branches: named by feature (e.g., `feature/authentication`)
- No direct commits to main
- Squash merge for clean history

## Governance

**Constitution Authority:**
This constitution supersedes all other development practices and guidelines. All team members, agents, and automated processes MUST comply.

**Amendment Process:**
1. Propose amendment with rationale and impact analysis
2. Document in ADR if architecturally significant
3. Update constitution with version bump (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
4. Propagate changes to dependent templates and documentation
5. Update LAST_AMENDED_DATE

**Compliance:**
- All PRs MUST include constitution compliance verification
- Violations MUST be flagged in code review
- Security principle violations block merge
- Constitution violations are tracked as technical debt if merged

**Versioning:**
- Format: MAJOR.MINOR.PATCH
- MAJOR: Breaking governance changes (principle removal/redefinition)
- MINOR: New principles or sections added
- PATCH: Clarifications, wording improvements

**Runtime Guidance:**
See `CLAUDE.md` for agent-specific development guidance and workflow instructions.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
