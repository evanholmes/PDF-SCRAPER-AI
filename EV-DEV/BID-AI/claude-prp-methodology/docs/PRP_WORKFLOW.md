# PRP Workflow Guide - When to Use Which Type

## Quick Decision Tree

```
Do you have clear requirements?
├─ No → Use PLANNING PRP (research + structure)
└─ Yes
    ├─ Is it a transformation of existing code?
    │   └─ Yes → Use SPEC PRP (systematic change)
    └─ No (it's new functionality)
        ├─ Is it complex/multi-phase?
        │   └─ Yes → Use TASK PRP (breakdown)
        └─ No → Use BASE PRP (standard implementation)
```

## The 4 Types at a Glance

| Type | Input | Output | Time | Use When |
|------|-------|--------|------|----------|
| **PLANNING** | Rough idea | Comprehensive PRD | 30-60 min | Need research & structure |
| **BASE** | Requirements | Working feature | 20-40 min + exec | Have clear requirements |
| **SPEC** | Current → Desired | Transformation | 40-90 min + exec | Changing existing code |
| **TASK** | Project description | Task checklist | 15-30 min + exec | Need progress tracking |

## Real-World Scenarios

### Scenario 1: "Add user authentication"

**Without requirements**:
```
You: "Add authentication"
→ PLANNING PRP first
→ Research: OAuth vs JWT, libraries, patterns
→ Generate: PRD with architecture, flows, APIs
→ Then: BASE PRP for implementation
```

**With requirements**:
```
You: "Add JWT auth using PyJWT, follow pattern in src/auth"
→ BASE PRP directly
→ Context: Library docs, existing pattern
→ Generate: Implementation PRP
→ Execute: Working auth system
```

### Scenario 2: "Migrate database"

```
You: "Migrate SQLite to PostgreSQL"
→ SPEC PRP (transformation)
→ Define: Current state (SQLite schema)
→ Define: Desired state (Postgres schema)
→ Tasks: Schema conversion, data migration, code updates
→ Execute: Step-by-step with validation
```

### Scenario 3: "Build e-commerce checkout"

```
You: "Build checkout flow"
→ PLANNING PRP (if complex/unclear)
→ Research: Payment gateways, user flows, edge cases
→ Generate: PRD with architecture
→ Then: TASK PRP (break into phases)
→ Tasks: Cart → Payment → Confirmation
→ Execute: One phase at a time
```

## Workflow Progressions

### Simple Feature (Clear Requirements)
```
Requirements → BASE PRP → Execute → Done
Time: 1-2 hours total
```

### Complex Feature (Research Needed)
```
Idea → PLANNING PRP → BASE PRP → Execute → Done
Time: 2-4 hours total
```

### Multi-Phase Feature
```
Requirements → BASE PRP → TASK PRP → Execute (incremental) → Done
Time: 3-6 hours total
```

### Code Transformation
```
Current System → SPEC PRP → Execute (validated) → Transformed System
Time: 2-5 hours total
```

## When to Skip PRP Creation

Use direct implementation (no PRP) for:
- **Trivial changes**: Typos, simple bug fixes
- **Copy-paste work**: Exact replication of existing pattern
- **Configuration**: Adding environment variables
- **Documentation**: Writing docs (not code)

Use PRP for:
- **New features**: Even small ones benefit from structure
- **Integrations**: External APIs, libraries
- **Refactoring**: Changing architecture
- **Anything unclear**: If you're not 100% certain, write a PRP

## Tips for Choosing

1. **When in doubt, use PLANNING PRP** - Better to over-research than under-research
2. **BASE is your workhorse** - 80% of features use BASE PRP
3. **SPEC for transformations** - Don't use BASE for migration/refactoring
4. **TASK for visibility** - Use when others need to track progress

## Common Mistakes

❌ Using BASE PRP for database migration → Use SPEC PRP
❌ Using PLANNING PRP when requirements are clear → Use BASE PRP
❌ Skipping PRP for "quick feature" that becomes complex → Should have used BASE PRP
❌ Using TASK PRP for simple feature → Overkill, use BASE PRP

## Summary

- **Unclear what to build** → PLANNING PRP
- **Know what to build** → BASE PRP
- **Transforming existing code** → SPEC PRP
- **Complex multi-step work** → TASK PRP