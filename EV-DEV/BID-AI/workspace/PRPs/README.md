# Product Requirement Prompts (PRPs)

This directory contains all PRPs for the BID-AI project.

## Directory Structure

- `in-progress/` - PRPs currently being worked on
- `completed/` - Finished PRPs (archived for reference)

## PRP Workflow

1. **Create requirements** - Write INITIAL.md with feature description
2. **Generate PRP** - Run `/prp-create INITIAL.md`
3. **Review PRP** - Check generated PRP for completeness
4. **Execute** - Run `/prp-base-execute [prp-file]`
5. **Archive** - Move completed PRP to `completed/`

## Available PRP Types

| Type | Command | Use Case |
|------|---------|----------|
| PLANNING | `/prp-planning-create` | Transform rough idea into PRD |
| BASE | `/prp-create` → `/prp-base-execute` | Standard feature implementation |
| SPEC | `/prp-spec-execute` | System transformations/migrations |
| TASK | `/task-list-init` → `/prp-task-execute` | Complex multi-phase projects |

## Example: Adding New Municipality

```bash
# Step 1: Create initial requirements
cat > in-progress/surrey-INITIAL.md << 'INITIAL'
# Add City of Surrey Portal

## Requirements
- Scrape Surrey's bidding portal
- Classify opportunities into tiers
- Create 4-agent team
INITIAL

# Step 2: Generate planning PRP
/prp-planning-create in-progress/surrey-INITIAL.md

# Step 3: Generate implementation PRP
/prp-create in-progress/surrey-PRD.md

# Step 4: Execute
/prp-base-execute in-progress/surrey-PRP.md

# Step 5: Archive when done
mv in-progress/surrey-* completed/
```

## Templates

All PRP templates are available in:
`../claude-prp-methodology/templates/`

- `BASE_PRP_TEMPLATE.md`
- `PLANNING_PRP_TEMPLATE.md`
- `SPEC_PRP_TEMPLATE.md`
- `TASK_LIST_TEMPLATE.md`
- `API_CONTRACT_TEMPLATE.md`

## See Also

- `../../METHODOLOGY.md` - Full PRP methodology guide
- `../../claude-prp-methodology/` - Complete PRP system documentation
