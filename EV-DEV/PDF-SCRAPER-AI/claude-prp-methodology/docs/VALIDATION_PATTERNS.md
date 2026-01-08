# Validation Patterns - 4-Level Testing Strategy

The PRP methodology uses a progressive 4-level validation loop that catches errors early and validates thoroughly.

## The 4 Levels

```
Level 1: Syntax & Style (seconds) → Fast feedback
Level 2: Unit Tests (seconds-minutes) → Logic validation
Level 3: Integration (minutes) → System validation
Level 4: Creative (minutes-hours) → Real-world validation
```

## Level 1: Syntax & Style

**Purpose**: Catch syntax errors, type errors, style violations
**Speed**: < 10 seconds
**When**: After every code change

### Python
```bash
ruff check src/ --fix      # Auto-fix style issues
mypy src/                  # Type checking
black src/                 # Format code
```

### TypeScript/JavaScript
```bash
npm run lint               # ESLint
npx tsc --noEmit          # Type checking
npm run format             # Prettier
```

### Go
```bash
go fmt ./...              # Format
go vet ./...              # Static analysis
golangci-lint run         # Comprehensive linting
```

**Expected**: Zero errors
**If Fail**: Read error message, fix immediately, re-run

## Level 2: Unit Tests

**Purpose**: Validate business logic, edge cases
**Speed**: Seconds to minutes
**When**: After implementing each function/class

### Test Patterns

**Happy Path**:
```python
def test_happy_path():
    result = function("valid_input")
    assert result.status == "success"
    assert result.data is not None
```

**Error Handling**:
```python
def test_invalid_input():
    with pytest.raises(ValidationError):
        function("invalid")
```

**Edge Cases**:
```python
def test_edge_cases():
    assert function("") raises EmptyInputError
    assert function(None) raises NullError
    assert function(" "*1000) raises TooLongError
```

### Running Tests

**Python**:
```bash
pytest tests/ -v                    # All tests
pytest tests/test_feature.py -v    # Specific file
pytest -k "test_auth" -v           # Match pattern
pytest -vvs                        # Max verbosity
```

**TypeScript/JavaScript**:
```bash
npm test                           # All tests
npm test feature.test.ts           # Specific file
npm test -- --verbose              # Verbose output
```

**Expected**: 100% pass rate
**If Fail**: Run with `-vvs` to see details, fix, re-run

## Level 3: Integration Tests

**Purpose**: Validate system integration, API contracts
**Speed**: Minutes
**When**: After implementing feature

### API Testing
```bash
# Start server
npm run dev  # or: python -m uvicorn main:app

# Test endpoints
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secure123"}'

# Expected: {"status": "success", "id": 1}
```

### Database Testing
```bash
# Run migration
alembic upgrade head  # or: npm run db:migrate

# Test data insertion
psql -d mydb -c "SELECT * FROM users WHERE email='test@example.com';"

# Expected: 1 row returned
```

### Browser Testing (UI)
```bash
# Start dev server
npm run dev

# Open browser: http://localhost:3000
# Manually test user flows
# Or use Playwright/Cypress for automation
```

**Expected**: Feature works end-to-end
**If Fail**: Check logs, debug with breakpoints

## Level 4: Creative Validation

**Purpose**: Real-world validation beyond standard tests
**Speed**: Minutes to hours
**When**: Before considering feature "done"

### Performance Testing
```bash
# Load testing
ab -n 1000 -c 10 http://localhost:8000/api/users
# Expected: <100ms p95 latency

# Profile code
py-spy record -o profile.svg -- python -m app
# Expected: No obvious bottlenecks
```

### Security Testing
```bash
# SQL injection
curl -X POST ... -d '{"email": "admin@test.com\' OR 1=1--"}'
# Expected: Validation error, not SQL error

# XSS testing
curl -X POST ... -d '{"name": "<script>alert(1)</script>"}'
# Expected: Escaped in output
```

### Accessibility Testing
```bash
# Run axe (for web apps)
npm run test:a11y
# Expected: No violations

# Keyboard navigation
# Tab through all interactive elements
# Expected: All reachable, visible focus
```

### Edge Case Testing
```
# Concurrent requests
# Large payloads (1MB+)
# Network failures (disconnect mid-request)
# Browser compatibility
# Mobile responsiveness
```

## Validation Command Format

Every PRP task should include validation:

```yaml
VALIDATE:
  - RUN: [command]
  - EXPECT: [success criteria]
  - IF_FAIL: [debugging hint]
```

### Good Examples

```yaml
VALIDATE:
  - RUN: pytest tests/test_auth.py -v
  - EXPECT: All 12 tests pass
  - IF_FAIL: Run with -vvs to see failure details, check mock setup
```

```yaml
VALIDATE:
  - RUN: curl http://localhost:8000/health
  - EXPECT: {"status": "ok"}
  - IF_FAIL: Check server logs at logs/app.log, verify server is running
```

## Progressive Validation Strategy

```
After each code change:
1. Run Level 1 (syntax) → Fix if fails
2. Run Level 2 (unit tests) → Fix if fails
3. Continue to next task

After feature complete:
4. Run Level 3 (integration) → Fix if fails
5. Run Level 4 (creative) → Fix if fails
6. Feature is done
```

## Common Validation Mistakes

❌ **Skipping validation** - "It should work"
✅ **Always validate** - Run the command, see the output

❌ **Mock everything** - Tests pass but code doesn't work
✅ **Integration tests** - Test real integration points

❌ **Only happy path** - Production fails on edge cases
✅ **Test edge cases** - Empty, null, too long, invalid

❌ **No performance testing** - Slow in production
✅ **Benchmark** - Know your p95/p99 latencies

## Summary

**Level 1**: Syntax → Seconds → After every change
**Level 2**: Unit tests → Minutes → After each function
**Level 3**: Integration → Minutes → After feature complete
**Level 4**: Creative → Hours → Before considering done

**Rule**: Never skip a level. Each level catches different types of bugs.