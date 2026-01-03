# PRP Examples Gallery

Real-world examples demonstrating how to use each PRP type effectively.

## Available Examples

### 1. BASE PRP Example - Authentication System
**File**: `base_example.md`

**Scenario**: Add JWT authentication to a FastAPI application

**What You'll Learn**:
- How to gather complete context (library docs, existing patterns)
- Writing information-dense tasks with MIRROR/MODIFY keywords
- Creating 4-level validation loops
- Documenting gotchas with solutions

**Complexity**: Medium
**Time to Review**: 10 minutes

### 2. TASK PRP Example - User Dashboard
**File**: `task_example.md`

**Scenario**: Break down a complex dashboard feature into manageable tasks

**What You'll Learn**:
- Using task keywords (CREATE, MODIFY, VALIDATE)
- Embedding validation commands in tasks
- Ordering tasks with dependencies
- Tracking progress with [DONE] markers

**Complexity**: Simple
**Time to Review**: 5 minutes

### 3. PLANNING PRP Example - Notification System
**File**: `planning_example.md`

**Scenario**: Transform rough idea into comprehensive PRD

**What You'll Learn**:
- Research phase structure
- Creating Mermaid diagrams
- Writing user stories with acceptance criteria
- Defining implementation phases

**Complexity**: Advanced
**Time to Review**: 15 minutes

### 4. SPEC PRP Example - Database Migration
**File**: `spec_example.md`

**Scenario**: Migrate from SQLite to PostgreSQL systematically

**What You'll Learn**:
- Defining current → desired state
- Ordering transformation tasks
- Validation at each step
- Rollback planning

**Complexity**: Advanced
**Time to Review**: 10 minutes

## How to Use These Examples

### Learning Path

1. **Start Here**: Read `base_example.md` - This is the most common PRP type
2. **Next**: Read `task_example.md` - See how to break down complex work
3. **Advanced**: Read `planning_example.md` - Learn the full research → PRD flow
4. **Specialized**: Read `spec_example.md` - Understand transformation patterns

### Using as Templates

1. **Copy the structure** - Don't change the sections (Goal, Why, What, etc.)
2. **Replace the content** - Swap in your feature details
3. **Keep the patterns** - MIRROR/MODIFY keywords, validation loops
4. **Maintain density** - Keep the level of detail (URLs, file paths, gotchas)

### Progression

**Your First PRP** (Start Simple):
- Use `base_example.md` as template
- Pick a small feature (< 100 lines of code)
- Focus on getting the structure right
- Don't worry about perfection

**Your Second PRP** (Add Complexity):
- Use `task_example.md` if it's multi-phase
- Add more validation levels
- Include more gotcha documentation
- Reference more existing patterns

**Your Third PRP** (Advanced):
- Try `planning_example.md` for research-heavy features
- Or `spec_example.md` for transformations
- Focus on comprehensive context
- Aim for first-pass implementation success

## Example Comparison

| Type | Use When | Example Scenario |
|------|----------|------------------|
| **BASE** | Clear requirements | Add authentication |
| **TASK** | Need breakdown | Complex dashboard |
| **PLANNING** | Research needed | Notification system |
| **SPEC** | Transform code | Database migration |

## Common Questions

**Q: Which example should I read first?**
A: Start with `base_example.md` - it's the most common type

**Q: Can I mix PRP types?**
A: Yes! PLANNING → BASE, or BASE → TASK are common flows

**Q: How detailed should my PRP be?**
A: Match the detail level in these examples - specific but not over-detailed

**Q: Should I include diagrams?**
A: For PLANNING PRPs, yes. For BASE/TASK, only if they clarify complexity

## Next Steps

1. **Read an example** - Start with `base_example.md`
2. **Try creating one** - Use the example as a template
3. **Execute it** - Use the corresponding `/prp-*-execute` command
4. **Iterate** - Refine based on what worked/didn't work

---

**Remember**: These examples show real-world complexity. Your first PRPs can be simpler!