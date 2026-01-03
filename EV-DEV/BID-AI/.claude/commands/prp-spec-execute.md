---
name: prp-spec-execute
description: Execute specification PRP with systematic implementation
arguments: "Path to SPEC PRP file to execute"
---

# Execute SPEC PRP

Implement a specification using an existing SPEC PRP.

## PRP File: $ARGUMENTS

## Execution Process

1. **Understand Spec**
   - Read the SPEC PRP thoroughly
   - Current state analysis (what exists now)
   - Desired state goals (what should exist after)
   - Task dependencies (what must happen first)

2. **ULTRATHINK**
   - Think hard before you execute the plan
   - Create a comprehensive plan addressing all requirements
   - Break down complex tasks into smaller, manageable steps using your TodoWrite tool
   - Identify implementation patterns from existing code to follow
   - Map out the transformation path (A → B)

3. **Execute Tasks**
   - Follow task order precisely
   - Run validation after each task
   - Fix failures before proceeding to next task
   - Never skip steps

4. **Verify Transformation**
   - Confirm desired state achieved
   - Run all validation gates
   - Test integration with existing code
   - Verify no regressions

Progress through each objective systematically.

## Common SPEC PRP Use Cases

### Database Migrations
- Add new columns to existing tables
- Change column types safely
- Create new tables with foreign keys
- Migrate data from old to new schema
- Remove deprecated tables

### Code Refactoring
- Extract shared logic to utilities
- Split large files into modules
- Rename for consistency
- Update import patterns
- Modernize deprecated APIs

### Framework Upgrades
- Update dependencies
- Replace deprecated APIs
- Migrate configuration files
- Update test patterns
- Verify compatibility

### Architecture Changes
- Monolith → Microservices
- REST → GraphQL
- Class components → Hooks
- SQL → NoSQL
- Synchronous → Asynchronous

Each transformation should have clear before/after states and validation at every step.