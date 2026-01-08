---
name: task-list-init
description: Create comprehensive task list for a project with detailed implementation steps
arguments: "Project description for task list creation"
---

Create a comprehensive task list in workspace/PRPs/in-progress/checklist.md for building your project based on: $ARGUMENTS

## Process

1. **Ingest the Information**
   - Read the project description
   - Understand the scope and requirements
   - Identify key features and deliverables

2. **Dig Deep into Existing Codebase**
   - Search for similar features and patterns
   - Identify established conventions
   - Find reusable components and utilities
   - Note testing patterns and validation approaches

3. **ULTRATHINK**
   - Think deeply about the project task
   - Create a detailed plan based on project context
   - Consider dependencies and ordering
   - Identify risks and edge cases

4. **Create Detailed Tasks**

Follow this principle for task creation:

### List of tasks to be completed in the order they should be executed using information-dense keywords

Information-dense keyword examples:
- **ADD** - Add new functionality to existing code
- **CREATE** - Create new files/components from scratch
- **MODIFY** - Update existing code
- **MIRROR** - Follow existing pattern from another file
- **FIND** - Search/discover existing implementations
- **EXECUTE** - Run commands/scripts
- **KEEP** - Preserve existing functionality
- **PRESERVE** - Maintain existing behavior/patterns
- **DELETE** - Remove code/files
- **REFACTOR** - Restructure without changing behavior
- **TEST** - Add or run tests
- **VALIDATE** - Verify correctness

Mark done tasks with: STATUS [DONE], if not done leave empty

### Task Format

```yaml
Task 1: Setup Database Schema
STATUS [ ]
CREATE src/database/models/user.ts:
  - MIRROR pattern from: src/database/models/base.ts
  - ADD fields: email, password_hash, created_at, updated_at
  - KEEP timestamps pattern consistent with other models
VALIDATE: npm run typecheck && npm run db:migrate:dry-run

Task 2: Implement Authentication Service
STATUS [ ]
CREATE src/services/auth.service.ts:
  - MIRROR pattern from: src/services/base.service.ts
  - ADD methods: register, login, logout, verifyToken
  - PRESERVE error handling pattern from existing services
VALIDATE: npm test src/services/auth.service.test.ts

Task 3: Create API Endpoints
STATUS [ ]
MODIFY src/routes/index.ts:
  - FIND pattern: "router registration"
  - ADD new router: authRouter
  - KEEP middleware ordering consistent
CREATE src/routes/auth.routes.ts:
  - MIRROR pattern from: src/routes/users.routes.ts
  - ADD endpoints: POST /register, POST /login, POST /logout
  - PRESERVE validation middleware pattern
VALIDATE: npm test src/routes/auth.routes.test.ts

Task 4: Implement Frontend Components
STATUS [ ]
CREATE src/components/LoginForm.tsx:
  - MIRROR pattern from: src/components/SignupForm.tsx
  - MODIFY form fields for login (email, password only)
  - KEEP form validation pattern identical
VALIDATE: npm run test:e2e -- LoginForm

...(...)

Task N: Integration Testing
STATUS [ ]
EXECUTE integration tests:
  - TEST full authentication flow
  - VALIDATE error handling
  - TEST edge cases (expired tokens, invalid credentials)
VALIDATE: npm run test:integration && npm run test:e2e
```

### Best Practices

1. **Each task should have:**
   - Clear action using keywords
   - Pattern to mirror (if applicable)
   - Validation command
   - Test coverage

2. **Task ordering:**
   - Database/models first
   - Business logic second
   - API layer third
   - UI components fourth
   - Integration tests last

3. **Dependencies:**
   - Mark dependencies explicitly
   - Order tasks so each can build on previous
   - Group related tasks together

4. **Validation:**
   - Every task has a validation step
   - Tests run after implementation
   - Integration tests at the end

## Output

Save the task list to: `workspace/PRPs/in-progress/checklist.md`

## Example Projects

- **E-commerce Checkout:** Cart → Payment → Order Confirmation
- **Social Media Feed:** Posts → Comments → Likes → Notifications
- **Project Management:** Projects → Tasks → Assignments → Timeline
- **Blog Platform:** Posts → Categories → Tags → Comments
- **Analytics Dashboard:** Data Collection → Processing → Visualization

Each task should have unit test coverage. Ensure tests pass on each task before moving to the next.