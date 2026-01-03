# PRP Templates

Templates for creating different types of PRPs.

## Available Templates

### prp.md - BASE Implementation Template
**Use for**: Standard feature implementation

**Sections**:
- Goal, Why, What, Success Criteria
- All Needed Context (docs, files, gotchas)
- Codebase trees (current & desired)
- Implementation Blueprint (tasks, pseudocode)
- 4-Level Validation Loop
- Final Checklist

**When to use**: Clear requirements, new functionality

### prp_planning.md - Planning/PRD Template
**Use for**: Research and comprehensive planning

**Sections**:
- Idea expansion and research phase
- User stories with Mermaid diagrams
- System architecture
- Implementation strategy
- Risk analysis

**When to use**: Rough ideas that need structure

### prp_spec.md - Specification Template
**Use for**: Systematic transformations

**Sections**:
- High/Mid/Low-level objectives
- Current → Desired state
- Implementation notes
- Ordered tasks with validation

**When to use**: Database migrations, refactoring, framework upgrades

### prp_task.md - Task List Template
**Use for**: Breaking down complex work

**Sections**:
- Information-dense task format
- Embedded validation commands
- IF_FAIL debugging hints
- Status tracking

**When to use**: Complex multi-step features, progress tracking needed

### variants/prp_base_typescript.md - TypeScript Variant
**Use for**: TypeScript/Next.js projects

**Differences from base**:
- TypeScript-specific examples
- Next.js patterns (Server Components, App Router)
- Frontend validation (ESLint, type checking)
- React testing patterns

## How to Use

1. **Choose template** - See [docs/PRP_WORKFLOW.md](../docs/PRP_WORKFLOW.md) for decision tree
2. **Copy to workspace** - `cp templates/prp.md workspace/PRPs/in-progress/my-feature.md`
3. **Fill in sections** - Replace placeholder text with your content
4. **Execute** - Use corresponding `/prp-*-execute` command

## Customization Tips

- **Keep the structure** - Don't remove sections
- **Add project-specific sections** - Add custom validation levels
- **Create variants** - Make language-specific versions (Python, Go, Rust)
- **Save successful PRPs** - Move to workspace/PRPs/completed/ as future templates

## Template Checklist

Before executing a PRP, verify it has:
- [ ] Specific goal (not vague)
- [ ] Complete context (URLs, file paths, gotchas)
- [ ] Clear tasks (precise keywords)
- [ ] Validation commands (runnable, with expected output)
- [ ] Pseudocode (guidance, not full implementation)