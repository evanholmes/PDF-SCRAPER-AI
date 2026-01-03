# CLAUDE.md Setup Guide - Autonomous Project Navigation System

**Purpose**: This guide teaches Claude how to create an efficient CLAUDE.md file for your project using the router pattern - a token-efficient navigation system that maximizes context while minimizing overhead.

## What This Guide Does

When you run this guide, Claude will:
1. Analyze your project structure
2. Identify key areas and workflows
3. Create section-specific READMEs
4. Generate a router-based CLAUDE.md (< 500 lines)
5. Integrate PRP development workflow

**Time**: 30-45 minutes for autonomous execution

---

## The Router Pattern Philosophy

### Traditional Approach (BAD - Token Bloat)
```markdown
# CLAUDE.md (5000+ lines)

## Authentication System
[500 lines of detailed authentication docs]

## Database Layer
[600 lines of database schema and query patterns]

## API Endpoints
[800 lines of endpoint documentation]

... (repeat for every subsystem)
```

**Problem**: Claude loads ALL this context on EVERY initialization, wasting tokens on irrelevant information.

### Router Approach (GOOD - Token Efficient)
```markdown
# CLAUDE.md (< 500 lines)

## Agent Router

**IF** task mentions authentication → Read `src/auth/README.md`
**IF** task mentions database → Read `src/database/README.md`
**IF** task mentions API → Read `src/api/README.md`

... (concise routing table)
```

**Benefit**: Claude reads ~500 lines initially, then navigates to specific README only when needed. Token usage scales with task complexity, not project size.

---

## CLAUDE.md Structure Template

Use this structure for your project:

```markdown
# CLAUDE.md - Project Navigation

**Project**: [Your Project Name] - [One sentence description]

## Agent Router (EXECUTE FIRST)

Follow this router before any action. Do not explore outside the relevant README.

**IF** task mentions [feature area A] →
→ **Read `path/to/area-a/README.md`** and follow it
→ Work in: `path/to/area-a/**`

**IF** task mentions [feature area B] →
→ **Read `path/to/area-b/README.md`** and follow it
→ Work in: `path/to/area-b/**`

**IF** general/exploratory task →
→ Continue reading this file

**ALWAYS respect repo rules**:
- [Key constraint 1]
- [Key constraint 2]
- [Key constraint 3]

---

## Quick Navigation Index

### Most Common Tasks → Go Here
| Task | File Location | Notes |
|------|----------|-------|
| Add new feature | `src/features/` | See features/README.md |
| Fix bug | `src/[area]/` | Find area first, then read README |
| Run tests | `tests/` | See tests/README.md |
| Configure | `config/` | See config/README.md |

### Quick Modification Patterns
| Modification Type | Files to Edit | Dependencies to Check |
|-------------------|---------------|----------------------|
| Add API endpoint | `src/api/` | Database schema, auth |
| Update UI component | `src/components/` | State management |
| Change database | `migrations/` | Run migrations, update models |

---

## Repository Structure

```
your-project/
├── src/                # Source code
│   ├── features/      # (See features/README.md)
│   ├── api/           # (See api/README.md)
│   └── utils/         # (See utils/README.md)
├── tests/             # (See tests/README.md)
├── workspace/         # PRP workspace
│   └── PRPs/          # (See METHODOLOGY.md)
└── config/            # (See config/README.md)
```

---

## PRP Development Workflow

**Commands available**:
- `/prp-create [file]` - Generate implementation PRP
- `/prp-base-execute [file]` - Execute BASE PRP
- `/prp-planning-create "idea"` - Generate PRD from idea
- `/read-docs` - Load project context

**Workflow**:
1. Create `workspace/PRPs/in-progress/INITIAL.md` with feature description
2. Run `/prp-create workspace/PRPs/in-progress/INITIAL.md`
3. Review generated PRP, add context
4. Run `/prp-base-execute [generated-prp].md`
5. Claude implements with validation loops

**Full documentation**: See `METHODOLOGY.md`

---

## Critical Documents

- **`README.md`** - Project overview (start here for humans)
- **`CLAUDE.md`** - This file (start here for AI)
- **`METHODOLOGY.md`** - Complete PRP system guide
- **`[area]/README.md`** - Area-specific deep dives

---

## Git Workflow

- Branch naming: `feature/description`, `fix/issue`, `refactor/area`
- Commit messages: Follow conventional commits
- Before committing: Run linting and tests

---

## Development Environment

- Language/Framework: [Your stack]
- Package manager: [npm/pip/cargo/etc]
- Key commands:
  - Dev server: `[command]`
  - Tests: `[command]`
  - Linting: `[command]`
  - Build: `[command]`
```

---

## Step-by-Step Autonomous Setup

Claude should execute these steps when setting up CLAUDE.md for a new project:

### Step 1: Analyze Project Structure
```yaml
EXECUTE:
  - Run: tree -L 3 -I 'node_modules|__pycache__|.git'
  - Identify: Main source directories (src/, app/, lib/)
  - Identify: Key areas (api/, components/, utils/, features/)
  - Identify: Test directories
  - Identify: Configuration files
  - Note: Tech stack (package.json, requirements.txt, Cargo.toml, go.mod)
```

### Step 2: Identify Key Areas and Workflows
```yaml
FOR_EACH major directory:
  ASK:
    - What is this area's responsibility?
    - What tasks would someone do here?
    - What are the key patterns/conventions?
    - What are common gotchas?

RESULT:
  - List of areas: [auth, api, database, frontend, etc.]
  - List of common tasks per area
  - Key routing rules (task → area mapping)
```

### Step 3: Create Section-Specific READMEs
```yaml
FOR_EACH identified area:
  CREATE: [area]/README.md

  CONTENT:
    - Purpose: What this area does (2-3 sentences)
    - Key Files: Most important files and their roles
    - Common Tasks: How to add/modify/test in this area
    - Patterns: Code patterns to follow (with examples)
    - Gotchas: Common pitfalls and solutions
    - Dependencies: What this area depends on
    - Commands: Area-specific commands (tests, builds)

  EXAMPLE: src/api/README.md
    ```markdown
    # API Layer

    RESTful API endpoints using FastAPI.

    ## Key Files
    - `routes.py` - Route definitions
    - `models.py` - Request/response schemas
    - `dependencies.py` - Dependency injection

    ## Adding New Endpoint
    1. Define schema in `models.py`
    2. Add route in `routes.py`
    3. Add tests in `tests/api/test_[endpoint].py`
    4. Update OpenAPI docs

    ## Patterns
    - All endpoints use dependency injection for auth
    - Responses use standardize_response() helper
    - Errors raise HTTPException with status codes

    ## Gotchas
    - FastAPI requires async def for async routes
    - Don't forget @router decorator

    ## Commands
    - Test: `pytest tests/api/ -v`
    - Run: `uvicorn main:app --reload`
    ```
```

### Step 4: Generate CLAUDE.md Using Template
```yaml
CREATE: CLAUDE.md

SECTIONS:
  1. Project Mission (< 100 words)
  2. Agent Router (IF/THEN rules for each area)
  3. Quick Navigation Index (task → location table)
  4. Repository Structure (tree with README references)
  5. PRP Development Workflow (commands + basic flow)
  6. Critical Documents (links to key files)
  7. Git Workflow (branch naming, commits)
  8. Development Environment (key commands)

TOKEN_BUDGET: < 500 lines total

KEY_PRINCIPLE: Navigation, not documentation
  - Router: "IF task mentions X → Read Y"
  - Index: "Task → Location + README link"
  - Structure: "Directory tree + pointers"
  - NOT: Complete documentation of X
```

### Step 5: Test Navigation
```yaml
TEST_QUESTIONS:
  - "How do I add a new API endpoint?"
    EXPECTED: Routes to api/README.md

  - "Where are the tests?"
    EXPECTED: Points to tests/ + tests/README.md

  - "How do I configure authentication?"
    EXPECTED: Routes to auth/README.md or config/README.md

IF_FAIL:
  - Add missing router rule
  - Create missing section README
  - Update navigation index
```

### Step 6: Refine Based on Gaps
```yaml
REVIEW:
  - All major areas covered in router?
  - All common tasks in navigation index?
  - All README references valid?
  - Token count < 500 lines?
  - PRP workflow integrated?

REFINE:
  - Add missing routes
  - Consolidate redundant sections
  - Ensure all links work
  - Test with sample questions
```

---

## Examples

### Example 1: Minimal CLAUDE.md (< 200 lines)

**For**: Simple single-purpose applications

```markdown
# CLAUDE.md - Todo API

**Project**: Simple FastAPI todo application

## Agent Router

**IF** task mentions API/endpoints → Read `src/api/README.md`
**IF** task mentions database/models → Read `src/models/README.md`
**IF** task mentions tests → Read `tests/README.md`

## Quick Navigation

| Task | Location |
|------|----------|
| Add endpoint | `src/api/` (See api/README.md) |
| Modify schema | `src/models/` (See models/README.md) |
| Run tests | `pytest tests/` |

## Structure

```
todo-api/
├── src/
│   ├── api/      # Endpoints (See api/README.md)
│   └── models/   # Database (See models/README.md)
└── tests/        # Tests (See tests/README.md)
```

## PRP Workflow

- Create: `/prp-create [file]`
- Execute: `/prp-base-execute [file]`
- Docs: `METHODOLOGY.md`

## Commands

- Dev: `uvicorn main:app --reload`
- Test: `pytest tests/ -v`
- Lint: `ruff check src/`
```

### Example 2: Full CLAUDE.md with Router (< 500 lines)

**For**: Complex multi-subsystem applications

```markdown
# CLAUDE.md - E-commerce Platform

**Project**: Full-stack e-commerce platform with React frontend, FastAPI backend, PostgreSQL database

## Agent Router (EXECUTE FIRST)

**IF** task mentions frontend/UI/components/React →
→ **Read `frontend/README.md`**
→ Work in: `frontend/src/**`

**IF** task mentions API/endpoints/backend →
→ **Read `backend/README.md`**
→ Work in: `backend/src/**`

**IF** task mentions database/schema/migrations →
→ **Read `database/README.md`**
→ Work in: `database/**`

**IF** task mentions authentication/auth/users →
→ **Read `backend/src/auth/README.md`**
→ Work in: `backend/src/auth/**`

**IF** task mentions payments/Stripe/checkout →
→ **Read `backend/src/payments/README.md`**
→ Work in: `backend/src/payments/**`

**ALWAYS respect**:
- No hardcoded secrets (use .env)
- All API endpoints require authentication
- Run tests before committing
- Follow conventional commits

## Quick Navigation Index

| Task | Location | Notes |
|------|----------|-------|
| Add React component | `frontend/src/components/` | See frontend/README.md |
| Add API endpoint | `backend/src/api/` | See backend/README.md |
| Database migration | `database/migrations/` | See database/README.md |
| Payment integration | `backend/src/payments/` | See payments/README.md |
| User authentication | `backend/src/auth/` | See auth/README.md |

## Repository Structure

```
ecommerce/
├── frontend/             # React app (See frontend/README.md)
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   └── hooks/       # Custom hooks
│   └── tests/
├── backend/              # FastAPI backend (See backend/README.md)
│   ├── src/
│   │   ├── api/         # Endpoints (See api/README.md)
│   │   ├── auth/        # Auth (See auth/README.md)
│   │   ├── payments/    # Payments (See payments/README.md)
│   │   └── models/      # Database models
│   └── tests/
├── database/             # Schema & migrations (See database/README.md)
│   ├── migrations/
│   └── seeds/
└── workspace/           # PRP workspace
    └── PRPs/            # (See METHODOLOGY.md)
```

## PRP Development Workflow

**Create PRP**:
1. Write `workspace/PRPs/in-progress/INITIAL.md` with feature description
2. Run `/prp-create workspace/PRPs/in-progress/INITIAL.md`
3. Review and enhance generated PRP
4. Run `/prp-base-execute [generated-prp].md`

**Available Commands**:
- `/prp-planning-create "idea"` - Research → PRD
- `/prp-create [file]` - Requirements → Implementation PRP
- `/prp-base-execute [file]` - Execute PRP
- `/api-contract-define [feature]` - Define backend/frontend contract

**Full guide**: `METHODOLOGY.md`

## Development Commands

**Frontend**:
- Dev: `cd frontend && npm run dev`
- Test: `npm test`
- Build: `npm run build`
- Lint: `npm run lint`

**Backend**:
- Dev: `cd backend && uvicorn main:app --reload`
- Test: `pytest tests/ -v`
- Lint: `ruff check src/`
- Migrations: `alembic upgrade head`

**Database**:
- Connect: `psql -d ecommerce`
- Migrate: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

## Git Workflow

- Branch: `feature/description`, `fix/issue-number`
- Commits: Conventional commits (feat:, fix:, docs:, refactor:)
- Before commit: `npm run lint && pytest tests/`
- PR: Squash merge to main

## Critical Documents

- **`README.md`** - Project overview, setup instructions
- **`METHODOLOGY.md`** - PRP system guide
- **`frontend/README.md`** - Frontend architecture and patterns
- **`backend/README.md`** - Backend architecture and API design
- **`database/README.md`** - Schema, migrations, queries
```

### Example 3: Bad CLAUDE.md (DON'T DO THIS)

**Problem**: Too verbose, no routing, encyclopedic

```markdown
# CLAUDE.md (3000+ lines)

## Project Overview
[500 lines of project history and context]

## Authentication System - Complete Documentation
[800 lines of auth implementation details]
- JWT token generation
- Password hashing algorithms
- OAuth2 flow diagrams
- Session management
- [endless details...]

## Database Schema - Complete Reference
[600 lines of every table, column, relationship]

## API Endpoints - Complete Specification
[900 lines of every endpoint with examples]

... [2000 more lines]
```

**Why it's bad**:
- ❌ Loads 3000+ lines on every initialization
- ❌ Claude reads irrelevant details for simple tasks
- ❌ Token waste on 95% unused information
- ❌ Hard to maintain (must update CLAUDE.md for every change)

**Router alternative**:
- ✅ CLAUDE.md: 200 lines routing to area READMEs
- ✅ Claude loads only relevant README for task
- ✅ Token efficient (200 + 300 area-specific = 500 total)
- ✅ Easy maintenance (update area README, not CLAUDE.md)

---

## Maintenance Guidelines

### When to Update CLAUDE.md

**DO update when**:
- ✅ New major subsystem added (new router rule needed)
- ✅ Project structure changes significantly
- ✅ New common task patterns emerge
- ✅ PRP workflow changes

**DON'T update when**:
- ❌ Small feature added (update area README instead)
- ❌ Implementation details change (update area README)
- ❌ New endpoint added (update api/README.md)
- ❌ Bug fixed (no CLAUDE.md change needed)

### When to Create New READMEs

Create new section README when:
- New subsystem with distinct responsibility
- Area has 5+ files
- Common tasks specific to this area
- Unique patterns/gotchas to document

### Token Budget Monitoring

Check periodically:
```bash
# Count lines in CLAUDE.md
wc -l CLAUDE.md

# Should be < 500 lines
# If growing:
# - Move details to area READMEs
# - Consolidate redundant sections
# - Remove outdated information
```

### Keeping Current

Monthly review:
- [ ] Router rules cover all major areas?
- [ ] Navigation index has common tasks?
- [ ] All README references valid?
- [ ] Token count still < 500 lines?
- [ ] PRP workflow up to date?

---

## Integration with PRP System

Your CLAUDE.md should reference the PRP methodology:

```markdown
## PRP Development Workflow

This project uses Product Requirement Prompts (PRPs) for systematic feature development.

**Quick Start**:
1. Create feature description in `workspace/PRPs/in-progress/INITIAL.md`
2. Run `/prp-create workspace/PRPs/in-progress/INITIAL.md`
3. Review generated PRP
4. Run `/prp-base-execute [generated-prp].md`

**PRP Types**:
- **PLANNING** - Rough idea → Comprehensive PRD
- **BASE** - Requirements → Implementation (most common)
- **SPEC** - Transform existing code systematically
- **TASK** - Break complex work into tasks

**Commands**:
- `/prp-planning-create "idea"` - Generate PRD
- `/prp-create [file]` - Generate implementation PRP
- `/prp-base-execute [file]` - Execute BASE PRP
- `/prp-spec-execute [file]` - Execute SPEC PRP
- `/prp-task-execute [file]` - Execute TASK PRP
- `/task-list-init "description"` - Generate task list

**Full Documentation**: See `METHODOLOGY.md`

**Examples**: See `examples/` directory

**Templates**: See `templates/` directory
```

---

## Success Checklist

Your CLAUDE.md is ready when:

- [ ] **Token efficient**: < 500 lines total
- [ ] **Router complete**: All major areas have IF/THEN rules
- [ ] **Navigation works**: Quick index has common tasks
- [ ] **Structure clear**: Directory tree with README pointers
- [ ] **PRP integrated**: Workflow and commands documented
- [ ] **Links valid**: All README references exist
- [ ] **Tested**: Sample questions route correctly
- [ ] **Maintainable**: Clear what goes in CLAUDE.md vs. area READMEs

---

## Final Notes

**Remember**:
- CLAUDE.md is a **navigation map**, not documentation
- **Router pattern** saves tokens by loading only relevant context
- **Section READMEs** contain the detailed information
- **PRP workflow** enables systematic feature development
- **Token budget** matters - keep CLAUDE.md < 500 lines

**When in doubt**:
- Add to area README, not CLAUDE.md
- Create routing rule, not detailed docs
- Point to documentation, don't include it

**The goal**: Claude reads CLAUDE.md (500 lines), understands project navigation, then reads specific README (300 lines) only when needed = 800 total tokens vs. 3000+ for encyclopedic CLAUDE.md.