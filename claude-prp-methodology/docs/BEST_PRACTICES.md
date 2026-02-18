# Best Practices for Writing Effective PRPs

## Golden Rules

1. **Context is King** - Include URLs, file paths, code examples
2. **Be Specific** - "MODIFY src/api/users.py line 45" not "update the API"
3. **Reference Patterns** - "MIRROR pattern from src/auth.py" not "implement auth"
4. **Document Gotchas** - "Library X requires Y before Z"
5. **Validate Everything** - Every task needs a validation command

## Writing Great Context Sections

### ✅ Good Context
```yaml
Documentation:
  - url: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    why: Official JWT auth pattern, shows token generation
    critical: Uses PyJWT, not python-jose

  - file: src/auth/admin.py (lines 45-78)
    why: Our existing auth pattern for admin routes
    note: Uses @require_auth decorator, see line 12

  - gotcha: "PyJWT 2.0+ required for RS256 algorithm"
    solution: "pip install 'PyJWT[crypto]>=2.0'"
```

### ❌ Bad Context
```yaml
Documentation:
  - Read the FastAPI docs
  - Look at existing auth
  - Install PyJWT
```

## Writing Clear Tasks

### ✅ Good Task Format
```yaml
Task 3: Add JWT token generation
CREATE src/auth/jwt.py:
  - MIRROR pattern from: src/auth/admin.py (lines 45-60)
  - IMPLEMENT: generate_token(user_id: int) -> str
    * Use RS256 algorithm (not HS256)
    * Expiry: 1 hour from now
    * Include claims: user_id, exp, iat
  - VALIDATE: pytest tests/test_jwt.py::test_generate_token -v
  - IF_FAIL: Check RS256 keys exist in config/keys/
```

### ❌ Bad Task Format
```yaml
Task 3: Create JWT functionality
- Make a file for JWT stuff
- Test it
```

## Pseudocode Guidelines

### ✅ Good Pseudocode (guidance, not implementation)
```python
async def register_user(email: str, password: str) -> User:
    # PATTERN: Always validate first (see validators.py)
    validated_email = validate_email(email)  # raises ValidationError
    validated_pass = validate_password(password)  # min 12 chars

    # GOTCHA: Check existence BEFORE expensive hashing
    if await db.users.exists(email=validated_email):
        raise UserExistsError("Email taken")

    # PATTERN: Use bcrypt with cost=12 (see auth/hash.py)
    password_hash = await hash_password(validated_pass)

    # PATTERN: All inserts use this format (see db/base.py)
    user = await db.users.create({
        "email": validated_email,
        "password_hash": password_hash,
        "verified": False  # email verification required
    })

    return User.from_db(user)
```

### ❌ Bad Pseudocode (too detailed or too vague)

Too detailed (just write the code yourself):
```python
def register_user(email: str, password: str) -> User:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValidationError("Invalid email format")
    if len(password) < 12:
        raise ValidationError("Password must be at least 12 characters")
    # ... 50 more lines of complete implementation
```

Too vague (AI doesn't know what to do):
```python
def register_user(email, password):
    # Validate the inputs
    # Hash the password
    # Save to database
    # Return the user
```

## Validation Best Practices

### ✅ Complete Validation Loop
```yaml
Validation Loop:
  Level 1 - Syntax:
    RUN: ruff check src/ && mypy src/
    EXPECT: No errors
    IF_FAIL: Read error message, fix syntax/types, re-run

  Level 2 - Unit Tests:
    RUN: pytest tests/test_feature.py -v
    EXPECT: All 8 tests pass
    IF_FAIL: Run with -vvs, check test setup, verify mocks

  Level 3 - Integration:
    RUN: curl -X POST http://localhost:8000/api/feature \
         -d '{"param": "test"}'
    EXPECT: {"status": "success"}
    IF_FAIL: Check logs at logs/app.log, verify DB connection

  Level 4 - Performance:
    RUN: ab -n 1000 -c 10 http://localhost:8000/api/feature
    EXPECT: <100ms p95 latency
    IF_FAIL: Profile with py-spy, check for N+1 queries
```

### ❌ Incomplete Validation
```yaml
Validation:
  - Run tests
  - Test the endpoint
  - Make sure it's fast
```

## Documenting Gotchas

### ✅ Actionable Gotchas
```python
# GOTCHA: This API rate limits at 10 req/sec
# → SOLUTION: Use rate_limiter.acquire() before each call
# → LOCATION: See src/external/rate_limiter.py

# GOTCHA: OAuth tokens expire after 1 hour
# → SOLUTION: Check expiry before each API call, refresh if needed
# → PATTERN: See src/auth/token_refresh.py for refresh logic

# GOTCHA: Database connection pool exhausted under load
# → SOLUTION: Use 'async with get_connection()' pattern, never hold connections
# → EXAMPLE: See src/db/queries.py for correct usage
```

### ❌ Vague Gotchas
```python
# Watch out for rate limiting
# Tokens expire
# Be careful with connections
```

## Common Anti-Patterns to Avoid

### 1. Assuming AI Knows Your Patterns
❌ "Implement authentication"
✅ "Implement JWT authentication following the pattern in src/auth/admin.py (lines 45-78)"

### 2. No Error Paths
❌ Task: "Call the external API"
✅ Task: "Call external API, handle 429 (rate limit), 503 (maintenance), timeout"

### 3. Missing Validation Commands
❌ "Test that it works"
✅ "VALIDATE: curl http://localhost:8000/health → expect {'status':'ok'}"

### 4. Incomplete Context
❌ "Use the FastAPI library"
✅ "Use FastAPI 0.100+, see https://fastapi.tiangolo.com/tutorial/dependencies/"

### 5. No Gotcha Documentation
❌ "Connect to the database"
✅ "Connect to DB, GOTCHA: pool_size must be < max_connections/2, see config/db.py"

## PRP Lifecycle Best Practices

### Before Writing
- [ ] Choose the right PRP type (PLANNING, BASE, SPEC, TASK)
- [ ] Gather all documentation URLs
- [ ] Identify existing patterns to reference
- [ ] List known gotchas

### While Writing
- [ ] Include specific file paths and line numbers
- [ ] Reference existing code patterns
- [ ] Write pseudocode for complex logic
- [ ] Add validation commands for every task
- [ ] Document all gotchas with solutions

### After Writing
- [ ] Review: Does AI have everything needed?
- [ ] Test: Try one task manually to verify clarity
- [ ] Refine: Add any missing context discovered
- [ ] Execute: Run the PRP and observe results

### After Execution
- [ ] Archive: Move completed PRPs to workspace/PRPs/completed/
- [ ] Learn: Note what worked well and what didn't
- [ ] Improve: Update templates based on learnings
- [ ] Share: Help others learn from your PRPs

## Tips for Different Project Types

### Backend APIs
- Reference OpenAPI/Swagger specs
- Include cURL commands for testing
- Document rate limits, timeouts
- Show database schema changes
- Include error response examples

### Frontend Apps
- Reference component library docs
- Show wireframes or mockups
- Document state management patterns
- Include accessibility requirements
- Test across browsers

### Full-Stack Features
- Start with API contract definition (`/api-contract-define`)
- Backend implementation first (testable with cURL)
- Frontend implementation second (uses working API)
- Integration testing last

### Database Migrations
- Always include rollback instructions
- Test migration on copy of production data
- Document data transformation logic
- Include before/after row counts

## Measuring PRP Quality

A high-quality PRP has:
- [ ] **Context density** → URLs, file paths, code examples
- [ ] **Specific tasks** → Precise keywords, line numbers
- [ ] **Pattern references** → MIRROR from existing code
- [ ] **Gotcha documentation** → Known issues with solutions
- [ ] **Validation loops** → 4 levels with specific commands
- [ ] **Pseudocode** → Guidance without complete implementation

A low-quality PRP has:
- [ ] Vague requirements
- [ ] No existing pattern references
- [ ] Missing gotchas
- [ ] No validation commands
- [ ] Either too much or too little detail

## Summary: The PRP Checklist

Before executing a PRP, verify:

**Context Section**:
- [ ] All URLs work and point to relevant docs
- [ ] All file paths exist in codebase
- [ ] All patterns are clearly referenced
- [ ] All gotchas have solutions

**Implementation Section**:
- [ ] Tasks use precise keywords
- [ ] Tasks reference specific files/lines
- [ ] Pseudocode provides guidance (not full implementation)
- [ ] Integration points documented

**Validation Section**:
- [ ] Every task has validation command
- [ ] 4-level loop is complete
- [ ] Expected outputs are specified
- [ ] IF_FAIL hints are helpful

**If all checked** → Execute with confidence
**If anything missing** → Add it before executing

---

**Remember**: The time spent writing a great PRP is time saved on implementation iterations.