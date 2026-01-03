# The PRP Methodology - Complete Guide

**Product Requirement Prompts (PRPs): A systematic approach to AI-driven development**

## Table of Contents

1. [Philosophy: Context is King](#philosophy-context-is-king)
2. [The 4 PRP Types](#the-4-prp-types)
3. [Workflow Progression](#workflow-progression)
4. [What Makes PRPs Work](#what-makes-prps-work)
5. [How to Write a Good PRP](#how-to-write-a-good-prp)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Philosophy: Context is King

The PRP methodology is built on one core principle: **AI agents succeed when they have comprehensive context**.

### The Traditional Problem

Traditional software requirements docs fail because they:
- **Assume knowledge** ("implement authentication" - which method? which library?)
- **Lack specificity** ("make it fast" - how fast? measured how?)
- **Miss gotchas** (no mention of library quirks or edge cases)
- **No validation path** (how do you know it works?)

### The PRP Solution

PRPs provide:
- **Complete context** - URLs, file paths, code examples
- **Explicit patterns** - "Use the pattern from src/auth.py lines 45-67"
- **Known gotchas** - "This library requires X before Y"
- **Built-in validation** - "Run this command, expect this output"

### Why This Works for AI

AI agents (like Claude) excel at:
- ✅ Following detailed instructions
- ✅ Recognizing patterns
- ✅ Iterating based on feedback (test failures)
- ✅ Writing code when given pseudocode

AI agents struggle with:
- ❌ Guessing your architecture preferences
- ❌ Knowing which of 5 valid approaches you want
- ❌ Understanding unstated requirements
- ❌ Inferring implicit gotchas

PRPs give AI what it needs to succeed.

## The 4 PRP Types

### 1. PLANNING PRP - Idea → Detailed PRD

**Purpose**: Transform rough ideas into comprehensive Product Requirements Documents

**When to Use**:
- You have a vague idea that needs structure
- You need to research approaches before implementing
- Stakeholders need to align before building
- The feature is complex with many unknowns

**What You Provide**:
```markdown
Rough idea: "Build a notification system for our app"
```

**What You Get**:
```markdown
Complete PRD with:
- Problem statement and solution overview
- User stories with acceptance criteria
- System architecture diagrams (Mermaid)
- API specifications
- Data models and relationships
- Sequence diagrams for key flows
- Implementation phases (no time estimates)
- Risks and mitigations
- Success metrics
```

**Command**: `/prp-planning-create "Your idea"`

**Example Flow**:
1. You: "Build a notification system"
2. Claude researches: Similar solutions, technical approaches, best practices
3. Claude asks: User personas? Success metrics? Constraints?
4. Claude generates: 10-page PRD with diagrams
5. You review and approve
6. PRD becomes input for BASE PRP

**Time Investment**: 30-60 minutes
**Value**: Prevents wasted implementation effort, aligns stakeholders

### 2. BASE PRP - Requirements → Implementation

**Purpose**: Standard feature implementation with comprehensive validation

**When to Use**:
- You have clear requirements (from PLANNING PRP or elsewhere)
- You're building new functionality
- You want validated, tested, working code
- The feature integrates with existing codebase

**What You Provide**:
```markdown
Feature request or requirements document
Can be:
- INITIAL.md with bullet points
- Output from PLANNING PRP
- User story with acceptance criteria
```

**What You Get**:
```markdown
Complete PRP with:
- Goal, Why, What, Success Criteria
- All Needed Context (URLs, files, gotchas)
- Current & Desired codebase tree
- Data models and structure
- Task list with precise keywords
- Pseudocode for complex logic
- 4-level validation loop
- Final checklist
```

**Commands**:
- `/prp-create [initial-request-file]` - Generate PRP
- `/prp-base-execute [generated-prp]` - Implement it

**Example Flow**:
1. You create: `INITIAL.md` with feature description
2. `/prp-create INITIAL.md`
3. Claude researches: Codebase patterns, library docs, gotchas
4. Claude generates: Complete PRP (~200-500 lines)
5. You review: Add any missing context
6. `/prp-base-execute [prp-file]`
7. Claude implements: Following PRP step-by-step
8. Claude validates: Runs tests, fixes failures, iterates
9. You get: Working, tested feature

**Time Investment**:
- PRP creation: 20-40 minutes
- PRP review: 10-20 minutes
- Execution: 30-120 minutes (automated)

**Value**: First-pass implementation success, validated code

### 3. SPEC PRP - Transform Existing Code Systematically

**Purpose**: Systematic transformations of existing codebases

**When to Use**:
- Database migrations
- Framework upgrades
- Large refactoring efforts
- Architectural changes
- Migration between technologies

**What You Provide**:
```markdown
Specification PRP with:
- High-level objective
- Mid-level objectives
- Low-level tasks
- Current state → Desired state
```

**What You Get**:
```markdown
Step-by-step transformation:
- Clear beginning state
- Clear ending state
- Ordered tasks with dependencies
- Validation at each step
- Rollback instructions
```

**Command**: `/prp-spec-execute [spec-prp-file]`

**Example Flow**:
1. You have: Existing system using SQLite
2. You want: Migrate to PostgreSQL
3. You create: SPEC PRP with migration steps
4. `/prp-spec-execute migration-spec.md`
5. Claude executes: Each task, validates, continues
6. You get: Fully migrated system

**Example Use Cases**:
- SQLite → PostgreSQL migration
- Monolith → Microservices refactoring
- Class components → Hooks (React)
- REST → GraphQL migration
- Python 2 → Python 3 upgrade

**Time Investment**:
- SPEC creation: 40-90 minutes
- Execution: 1-4 hours (automated)

**Value**: Systematic, validated transformations

### 4. TASK PRP - Break Down Complex Work

**Purpose**: Break complex features into manageable, validated tasks

**When to Use**:
- Complex multi-step features
- You need to track progress
- Multiple developers coordinating
- You want clear checkpoints

**What You Provide**:
```markdown
Project description: "Implement user dashboard with analytics"
```

**What You Get**:
```markdown
Task list with:
- Information-dense keywords (CREATE, MODIFY, MIRROR)
- Embedded validation commands
- IF_FAIL debugging hints
- Status tracking ([DONE] markers)
```

**Commands**:
- `/task-list-init "Project description"` - Generate task list
- `/prp-task-execute [task-list-file]` - Execute tasks

**Example Flow**:
1. You: "Implement user dashboard"
2. `/task-list-init "User dashboard..."`
3. Claude generates: 15-30 tasks with validation
4. You review: Adjust ordering if needed
5. `/prp-task-execute task-list.md`
6. Claude executes: One task at a time, marks [DONE]
7. You track: Progress through [DONE] markers

**Task Format**:
```yaml
Task 1: Setup Database Schema
STATUS [ ]
CREATE src/models/user_stats.ts:
  - MIRROR pattern from: src/models/base.ts
  - ADD fields: views, clicks, conversions
VALIDATE: npm run typecheck && npm run test:db

Task 2: Create API Endpoint
STATUS [ ]
CREATE src/api/dashboard.ts:
  - MIRROR pattern from: src/api/users.ts
  - ADD endpoint: GET /api/dashboard/stats
VALIDATE: curl http://localhost:3000/api/dashboard/stats
```

**Time Investment**:
- Task list creation: 15-30 minutes
- Execution: Varies by complexity

**Value**: Clear progress tracking, systematic execution

## Workflow Progression

### Linear Progression (Typical)

```
PLANNING PRP → BASE PRP → Execution → Done
```

**Example**:
1. Rough idea → PLANNING PRP → Comprehensive PRD
2. PRD → BASE PRP → Complete implementation plan
3. BASE PRP → Execute → Working feature

### Alternative Paths

**Direct to BASE** (when requirements are clear):
```
Requirements → BASE PRP → Execution → Done
```

**Complex Features** (need task breakdown):
```
Requirements → BASE PRP → TASK PRP → Execution → Done
```

**Transformations**:
```
Current System → SPEC PRP → Execution → Transformed System
```

## What Makes PRPs Work

### 1. Context Density

**Bad** (traditional):
```
Add authentication to the app.
```

**Good** (PRP):
```yaml
Goal: Add JWT-based authentication

Context:
- url: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
  why: Official FastAPI JWT auth pattern
- file: src/auth/example.py
  why: Shows our existing auth pattern for admin routes
- gotcha: "Our JWT library requires PyJWT 2.0+ for RS256"
- pattern: "All protected routes use @require_auth decorator"
```

### 2. Pattern Recognition

**Bad**:
```
Create a new API endpoint for users.
```

**Good**:
```yaml
CREATE src/api/users.py:
  - MIRROR pattern from: src/api/products.py (lines 12-45)
  - KEEP the same:
    * Error handling pattern
    * Response format (see src/utils/responses.py)
    * Validation decorator usage
  - MODIFY only:
    * Endpoint path: /api/v1/users
    * Schema: UserSchema instead of ProductSchema
```

### 3. Explicit Gotchas

**Bad**:
```
Connect to the external API.
```

**Good**:
```python
# CRITICAL GOTCHAS:
# 1. This API rate limits at 10 req/sec (returns 429)
#    → SOLUTION: Use rate_limiter.acquire() before calls
# 2. API returns 503 during maintenance (daily 2-3am UTC)
#    → SOLUTION: Implement retry with exponential backoff
# 3. OAuth tokens expire after 1 hour
#    → SOLUTION: Check expiry before each call, refresh if needed
```

### 4. Built-in Validation

**Bad**:
```
Implement the feature and test it.
```

**Good**:
```yaml
Implementation:
  - CREATE src/feature.py
  - [... code tasks ...]

Validation Loop:
  Level 1 - Syntax:
    RUN: ruff check src/feature.py && mypy src/feature.py
    EXPECT: No errors
    IF_FAIL: Read error message, fix syntax/types

  Level 2 - Unit Tests:
    RUN: pytest tests/test_feature.py -v
    EXPECT: All 8 tests pass
    IF_FAIL: Run pytest -vvs to see failure details

  Level 3 - Integration:
    RUN: curl -X POST http://localhost:8000/api/feature
    EXPECT: {"status": "success"}
    IF_FAIL: Check logs at logs/app.log for stack trace

  Level 4 - Creative:
    RUN: ab -n 1000 -c 10 http://localhost:8000/api/feature
    EXPECT: <100ms p95 latency
    IF_FAIL: Profile with py-spy, optimize bottlenecks
```

### 5. Pseudocode Guidance

**Bad**:
```
Implement the user registration function.
```

**Good**:
```python
async def register_user(email: str, password: str) -> User:
    # PATTERN: Always validate input first (see src/validators.py)
    validated_email = validate_email(email)  # raises ValidationError
    validated_pass = validate_password(password)  # min 12 chars, special chars

    # GOTCHA: Check for existing user BEFORE hashing password (expensive)
    existing = await db.users.find_one({"email": validated_email})
    if existing:
        raise UserExistsError("Email already registered")

    # PATTERN: Use our standard password hashing (see src/auth/hash.py)
    password_hash = await hash_password(validated_pass)  # bcrypt, cost=12

    # PATTERN: All DB inserts use this format (see src/db/base.py)
    user = await db.users.insert_one({
        "email": validated_email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
        "verified": False  # IMPORTANT: email verification required
    })

    # PATTERN: Standardized response format (see src/utils/responses.py)
    return User.from_db(user)  # Pydantic model
```

## How to Write a Good PRP

### Step 1: Choose the Right Template

- Rough idea? → PLANNING template
- Clear requirements? → BASE template
- Transformation? → SPEC template
- Task breakdown? → TASK template

### Step 2: Fill in Complete Context

**Documentation**:
- Include direct URLs to official docs
- Specify exact sections needed ("OAuth 2.0" not "authentication")
- Note which documentation is most critical

**Codebase Examples**:
- Reference specific files: `src/auth/example.py`
- Reference specific lines: `lines 45-67`
- Explain what pattern to copy

**Gotchas**:
- Be specific: "This library requires X before Y"
- Include solutions: "To avoid Z, always do A"
- Reference where you learned this

### Step 3: Write Clear Tasks

Use precise keywords:
- **CREATE** - New file/component
- **MODIFY** - Update existing file
- **MIRROR** - Copy pattern from another file
- **REFACTOR** - Restructure without changing behavior
- **DELETE** - Remove code
- **FIND** - Search for specific pattern

Be specific about locations:
- ❌ "Update the API file"
- ✅ "MODIFY src/api/users.py: FIND 'router.get' AFTER line 45"

### Step 4: Add Pseudocode for Complex Logic

Include:
- Function signatures with types
- Key algorithm steps
- Edge case handling
- Integration points with existing code

Don't include:
- Complete implementation (that's what AI generates)
- Boilerplate code
- Obvious steps

### Step 5: Build Validation Loops

**Level 1**: Syntax & style (fast, catches obvious errors)
**Level 2**: Unit tests (validates business logic)
**Level 3**: Integration tests (validates system integration)
**Level 4**: Creative validation (performance, security, UX)

Each level should have:
- **RUN**: Exact command to run
- **EXPECT**: What output indicates success
- **IF_FAIL**: Debugging hint

### Step 6: Review and Refine

Before executing, check:
- [ ] All URLs work and point to relevant docs
- [ ] All file paths exist in codebase
- [ ] All patterns referenced are clear
- [ ] All gotchas have solutions
- [ ] All tasks have validation commands
- [ ] Pseudocode is helpful but not complete code

## Anti-Patterns to Avoid

### 1. Vague Context

**❌ Bad**:
```
Use the authentication library.
```

**✅ Good**:
```yaml
- url: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
  why: Shows JWT implementation with FastAPI
- file: src/auth/jwt.py
  why: Our existing JWT helper functions
- gotcha: "We use PyJWT 2.4+, verify algorithm is RS256 not HS256"
```

### 2. Missing Patterns

**❌ Bad**:
```
CREATE src/api/new_endpoint.py
```

**✅ Good**:
```
CREATE src/api/new_endpoint.py:
  - MIRROR pattern from: src/api/users.py (our standard REST pattern)
  - KEEP: Error handling, response format, validation decorators
  - MODIFY: Endpoint path and schema only
```

### 3. No Validation Commands

**❌ Bad**:
```
Implement feature and test it.
```

**✅ Good**:
```
Level 1: ruff check src/ && mypy src/
Level 2: pytest tests/ -v
Level 3: curl http://localhost:8000/health
Level 4: ab -n 1000 -c 10 http://localhost:8000/api/feature
```

### 4. Pseudocode is Actually Code

**❌ Bad** (too detailed - just write it yourself):
```python
def register_user(email: str, password: str) -> User:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValidationError("Invalid email")
    if len(password) < 12:
        raise ValidationError("Password too short")
    # ... 50 more lines of complete implementation
```

**✅ Good** (guidance, not implementation):
```python
async def register_user(email: str, password: str) -> User:
    # PATTERN: Validate first (see validators.py)
    validated_email = validate_email(email)
    validated_pass = validate_password(password)

    # GOTCHA: Check existence BEFORE expensive hashing
    if await user_exists(validated_email):
        raise UserExistsError()

    # PATTERN: Standard password hashing (auth/hash.py)
    password_hash = await hash_password(validated_pass)

    # PATTERN: Standard DB insert (db/base.py)
    user = await db.users.insert_one({...})
    return User.from_db(user)
```

### 5. No Gotcha Documentation

**❌ Bad**:
```
Call the external API.
```

**✅ Good**:
```
Call the external API:
  - GOTCHA: Rate limit 10/sec → use rate_limiter.acquire()
  - GOTCHA: Maintenance 2-3am UTC → retry with backoff
  - GOTCHA: Tokens expire 1hr → check expiry before each call
  - PATTERN: See src/external/api_client.py for retry decorator
```

## Summary: The PRP Advantage

Traditional requirement: "Add user authentication"
- AI guesses at approach
- Doesn't know your patterns
- Misses edge cases
- No validation path
- **Result**: Multiple iterations, bugs

PRP requirement: "Add JWT authentication using..."
- Specific library and approach
- References existing auth patterns
- Lists known gotchas with solutions
- Includes 4-level validation loop
- **Result**: Working code, first pass

**The difference**: Context density

## Next Steps

1. **See it in action** - Check [examples/](examples/) for real PRPs
2. **Try creating one** - Start with a small feature
3. **Iterate** - Your PRPs will improve with practice
4. **Share** - Help others learn from your patterns

---

**Remember**: Time spent on a great PRP is time saved on implementation iterations.