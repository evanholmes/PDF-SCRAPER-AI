---
name: prp-task-execute
description: Execute task list from existing TASK PRP
arguments: "Path to TASK PRP file to execute"
---

# Execute TASK PRP

Run through a task list from an existing TASK PRP.

## PRP File: $ARGUMENTS

## Execution Process

1. **Load Tasks**
   - Read task list from TASK PRP
   - Understand context and requirements
   - Note dependencies between tasks
   - Identify validation commands

2. **Execute Each Task**
   - Perform ACTION (CREATE, MODIFY, MIRROR, etc.)
   - Run VALIDATE command
   - Fix IF_FAIL issues
   - Mark task as [DONE] in checklist

3. **Complete Checklist**
   - Verify all tasks done
   - Run final validation suite
   - Check no regressions
   - Test integration

Work through tasks sequentially, validating each before moving to the next.

## Task Execution Pattern

For each task:

```yaml
Task N: [Description]
STATUS [ ] → [DONE]

ACTION:
  - Read context (files, patterns, requirements)
  - Implement according to keywords (CREATE, MODIFY, etc.)
  - Follow established patterns

VALIDATE:
  - Run validation command
  - Check output/results
  - Verify expected behavior

IF_FAIL:
  - Read error message
  - Fix issue
  - Re-run validation
  - Repeat until pass
```

## Keywords Reference

- **CREATE** - New file/component from scratch
- **MODIFY** - Update existing code
- **MIRROR** - Follow pattern from another file
- **REFACTOR** - Restructure without changing behavior
- **DELETE** - Remove code/files
- **READ** - Load context/understand existing code
- **FIND** - Search/discover implementations
- **TEST** - Add or run tests
- **VALIDATE** - Verify correctness
- **KEEP** - Preserve existing functionality
- **PRESERVE** - Maintain existing behavior

## Best Practices

1. **One task at a time** - Don't skip ahead
2. **Validate immediately** - Run tests after each task
3. **Fix before continuing** - Don't leave broken code
4. **Mark progress** - Update STATUS to [DONE]
5. **Read patterns** - Actually look at MIRROR references
6. **Test edge cases** - Don't just happy path

## Completion Criteria

- All tasks marked [DONE]
- All validations passing
- Integration tests passing
- No regressions introduced
- Code follows project patterns