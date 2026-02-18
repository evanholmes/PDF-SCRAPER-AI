# Task Keywords Reference

Complete vocabulary for writing clear, actionable PRP tasks.

## Primary Keywords

| Keyword | Meaning | Example |
|---------|---------|---------|
| **CREATE** | New file/component from scratch | `CREATE src/auth.py:` |
| **MODIFY** | Update existing file | `MODIFY src/api/users.py:` |
| **MIRROR** | Follow pattern from another file | `MIRROR pattern from: src/api/products.py` |
| **REFACTOR** | Restructure without changing behavior | `REFACTOR src/legacy.py:` |
| **DELETE** | Remove code/files | `DELETE src/deprecated.py` |
| **READ** | Understand existing code | `READ src/config.py:` |
| **FIND** | Search for specific pattern | `FIND pattern: "class User"` |
| **TEST** | Add or run tests | `TEST src/feature.py` |
| **VALIDATE** | Verify correctness | `VALIDATE: pytest tests/` |
| **FIX** | Debug and repair | `FIX failing test in test_auth.py` |

## Operation Keywords

| Keyword | Meaning | Example |
|---------|---------|---------|
| **INJECT** | Add code at specific location | `INJECT after line 45:` |
| **PRESERVE** | Keep existing functionality | `PRESERVE error handling pattern` |
| **KEEP** | Maintain existing code/pattern | `KEEP validation decorator usage` |
| **UPDATE** | Change specific values | `UPDATE timeout from 30 to 60` |
| **ADD** | Append new functionality | `ADD endpoint: POST /users` |

## Task Structure Pattern

```yaml
[ACTION] path/to/file:
  - [OPERATION]: [DETAILS]
  - VALIDATE: [COMMAND]
  - IF_FAIL: [DEBUG_HINT]
```

## Examples

### Create New File
```yaml
CREATE src/services/email.py:
  - MIRROR pattern from: src/services/sms.py
  - MODIFY for email sending (SMTP)
  - KEEP retry logic identical
  - VALIDATE: pytest tests/test_email.py -v
  - IF_FAIL: Check SMTP credentials in .env
```

### Modify Existing File
```yaml
MODIFY src/api/users.py:
  - FIND pattern: "router.get('/users')"
  - ADD new endpoint after existing one:
      router.get('/users/{id}/settings')
  - PRESERVE existing error handling
  - VALIDATE: curl http://localhost:8000/users/1/settings
  - IF_FAIL: Check route registration in main.py
```

### Refactor Code
```yaml
REFACTOR src/utils/helpers.py:
  - FIND: Duplicate code in parse_date, parse_datetime
  - CREATE: New function _parse_generic(date_string)
  - UPDATE: Both functions to use _parse_generic
  - PRESERVE: Existing function signatures
  - VALIDATE: pytest tests/test_utils.py -v
  - IF_FAIL: Check all call sites still work
```

### Delete Deprecated Code
```yaml
DELETE src/legacy/old_auth.py:
  - VERIFY: No imports of old_auth in codebase
    (Run: grep -r "from.*old_auth" src/)
  - DELETE: The file itself
  - UPDATE: Remove from __init__.py imports
  - VALIDATE: pytest tests/ -v (all tests still pass)
  - IF_FAIL: Check for remaining references
```

## Best Practices

1. **Be Specific**: `MODIFY src/api/users.py` not `Update the API`
2. **Reference Lines**: `FIND: "class User" around line 45`
3. **Include Validation**: Every task should have VALIDATE command
4. **Add Debug Hints**: IF_FAIL tells AI where to look
5. **Order Matters**: Dependencies first, integration last

## Common Patterns

### Adding a Feature
```
1. READ existing similar feature
2. CREATE new feature file (MIRROR pattern)
3. UPDATE router/registry to include it
4. CREATE tests for feature
5. VALIDATE all tests pass
```

### Fixing a Bug
```
1. CREATE failing test that reproduces bug
2. VALIDATE test fails (confirms bug)
3. MODIFY code with fix
4. VALIDATE test now passes
5. VALIDATE no regression (all tests pass)
```

### Database Migration
```
1. CREATE migration file (MIRROR previous migration)
2. UPDATE schema definition
3. MODIFY ORM models to match
4. VALIDATE migration runs: alembic upgrade head
5. VALIDATE rollback works: alembic downgrade -1
```