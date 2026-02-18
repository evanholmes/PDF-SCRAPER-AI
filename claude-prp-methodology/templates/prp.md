name: "BASE PRP Template v2 - Context-Rich with Validation Loops"
description: |

## Purpose

Template optimized for AI agents to implement features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

## Core Principles

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal

[What needs to be built - be specific about the end state and desires]

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)

```yaml
# MUST READ - Include these in your context window
- url: [Official framework/library docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example file in your codebase]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Library documentation URL]
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [workspace/ai_docs/file.md]
  why: [Curated docs that you've saved locally]
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash

```

### Desired Codebase tree with files to be added and responsibility of file

```bash

```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: [Library name] requires [specific setup]
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
# Example: We use strict mode for [tool name]
```

## Implementation Blueprint

### Data models and structure

Create the core data models, ensuring type safety and consistency.

**Python Example**:
```python
Examples:
 - ORM models (SQLAlchemy, Django ORM)
 - Pydantic models for validation
 - API schemas
 - Dataclasses for business logic
```

**TypeScript Example**:
```typescript
Examples:
 - Zod schemas for validation
 - TypeScript interfaces/types
 - Database schema types
 - API response types
```

**Go Example**:
```go
Examples:
 - Structs with JSON tags
 - Validation tags
 - Interface definitions
 - Database models
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.py:
  - FIND pattern: "class OldImplementation"
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures

CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

### Per task pseudocode as needed added to each task

**Python Example**:
```python

# Task 1
# Pseudocode with CRITICAL details don't write entire code
async def new_feature(param: str) -> Result:
    # PATTERN: Always validate input first (see src/validators.py)
    validated = validate_input(param)  # raises ValidationError

    # GOTCHA: This library requires connection pooling
    async with get_connection() as conn:  # see src/db/pool.py
        # PATTERN: Use existing retry decorator
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # CRITICAL: API returns 429 if >10 req/sec
            await rate_limiter.acquire()
            return await external_api.call(validated)

        result = await _inner()

    # PATTERN: Standardized response format
    return format_response(result)  # see src/utils/responses.py
```

**TypeScript Example**:
```typescript

// Task 1
// Pseudocode with CRITICAL details don't write entire code
export async function newFeature(param: string): Promise<Result> {
    // PATTERN: Validate with Zod schema (see lib/validation.ts)
    const validated = validateInput(param)  // throws ValidationError

    // GOTCHA: Server Components can't use browser APIs
    // PATTERN: Use existing data fetching pattern
    try {
        // CRITICAL: Must use proper error boundaries
        const result = await fetchWithRetry(validated)  // see lib/fetch.ts

        // PATTERN: Standardized response format
        return formatResponse(result)  // see lib/responses.ts
    } catch (error) {
        // PATTERN: Standardized error handling
        return handleError(error)  // see lib/errors.ts
    }
}
```

### Integration Points

```yaml
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"

CONFIG:
  - add to: config/settings (or .env file)
  - pattern: "FEATURE_TIMEOUT = process.env.FEATURE_TIMEOUT || '30000'"

ROUTES:
  - add to: src/routes (or app/ for Next.js)
  - pattern: "Register feature router with main app"
```

## Validation Loop

### Level 1: Syntax & Style

**Python**:
```bash
# Run these FIRST - fix any errors before proceeding
ruff check src/new_feature.py --fix  # Auto-fix what's possible
mypy src/new_feature.py              # Type checking
black src/new_feature.py             # Formatting

# Expected: No errors. If errors, READ the error and fix.
```

**TypeScript/JavaScript**:
```bash
# Run these FIRST - fix any errors before proceeding
npm run lint                         # ESLint checks
npx tsc --noEmit                    # TypeScript type checking
npm run format                       # Prettier formatting

# Expected: No errors. If errors, READ the error and fix.
```

**Go**:
```bash
# Run these FIRST - fix any errors before proceeding
go fmt ./...                        # Format code
go vet ./...                        # Static analysis
golangci-lint run                   # Comprehensive linting

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests each new feature/file/function use existing test patterns

**Python**:
```python
# CREATE test_new_feature.py with these test cases:
def test_happy_path():
    """Basic functionality works"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """Handles timeouts gracefully"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# Run and iterate until passing:
pytest test_new_feature.py -v
# If failing: Read error, understand root cause, fix code, re-run
```

**TypeScript/JavaScript**:
```typescript
// CREATE __tests__/new-feature.test.ts with these test cases:
describe('newFeature', () => {
  test('handles valid input correctly', async () => {
    const result = await newFeature('valid')
    expect(result.status).toBe('success')
  })

  test('throws ValidationError on invalid input', async () => {
    await expect(newFeature('')).rejects.toThrow(ValidationError)
  })

  test('handles API timeout gracefully', async () => {
    jest.spyOn(api, 'call').mockRejectedValue(new TimeoutError())
    const result = await newFeature('valid')
    expect(result.status).toBe('error')
    expect(result.message).toContain('timeout')
  })
})
```

```bash
# Run and iterate until passing:
npm test new-feature.test.ts
# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test

**API Testing**:
```bash
# Start the service
npm run dev  # or: python -m uvicorn main:app --reload

# Test the endpoint
curl -X POST http://localhost:8000/api/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs for stack trace
```

**UI Testing**:
```bash
# For web applications
# Open browser to http://localhost:3000/feature-page
# Test user flows manually or with automation (Playwright, Cypress)
```

### Level 4: Deployment & Creative Validation

```bash
# Production build check (adjust for your tech stack)
npm run build  # or: docker build .

# Expected: Successful build with no errors

# Creative validation methods:
# - Load testing with realistic data
# - End-to-end user journey testing
# - Performance benchmarking
# - Security scanning
# - Documentation validation

# Custom validation specific to the feature
# [Add creative validation methods here]
```

## Final validation Checklist

- [ ] All tests pass: [run your test command]
- [ ] No linting errors: [run your lint command]
- [ ] No type errors: [run your type check command]
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't mix sync/async inappropriately
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
