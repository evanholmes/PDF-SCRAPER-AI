---
name: prp-base-execute
description: Execute PRP implementation with comprehensive planning and validation
arguments: "Path to PRP file to execute"
---

# Execute BASE PRP

Implement a feature using the PRP file.

## PRP File: $ARGUMENTS

## Execution Process

1. **Load PRP**
   - Read the specified PRP file
   - Understand all context and requirements
   - Follow all instructions in the PRP and extend the research if needed
   - Ensure you have all needed context to implement the PRP fully
   - Do more web searches and codebase exploration as needed

2. **ULTRATHINK**
   - Ultrathink before you execute the plan. Create a comprehensive plan addressing all requirements
   - Break down the PRP into clear todos using the TodoWrite tool
   - Use agent subagents and batch tools to enhance the process
   - **Important:** YOU MUST ENSURE YOU HAVE EXTREMELY CLEAR TASKS FOR SUBAGENTS AND REFERENCE CONTEXT
   - **Important:** MAKE SURE EACH SUBAGENT READS THE PRP AND UNDERSTANDS ITS CONTEXT
   - Identify implementation patterns from existing code to follow
   - Never guess about imports, file names, function names etc. ALWAYS be based in reality and real context gathering

3. **Execute the Plan**
   - Implement all the code step by step
   - Follow task order from PRP
   - Reference established patterns from codebase
   - Use pseudocode from PRP as guidance

4. **Validate**
   - Run each validation command
   - The better validation that is done, the more confident we can be that the implementation is correct
   - Fix any failures
   - Re-run until all pass
   - Always re-read the PRP to validate and review the implementation to ensure it meets the requirements

5. **Complete**
   - Ensure all checklist items done
   - Run final validation suite
   - Report completion status
   - Read the PRP again to ensure you have implemented everything

6. **Reference the PRP**
   - You can always reference the PRP again if needed

Note: If validation fails, use error patterns in PRP to fix and retry.

## Validation Levels

### Level 1: Syntax & Style
- Run linters (eslint, ruff, etc.)
- Run type checkers (tsc, mypy, etc.)
- Check formatting (prettier, black, etc.)

### Level 2: Unit Tests
- Run unit test suite
- Verify test coverage
- Fix failing tests

### Level 3: Integration Tests
- Test API endpoints with curl/Postman
- Test UI flows in browser
- Verify database operations
- Check external integrations

### Level 4: Creative Validation
- Performance testing
- Edge case verification
- User flow testing
- Security checks

Each level must pass before moving to the next.