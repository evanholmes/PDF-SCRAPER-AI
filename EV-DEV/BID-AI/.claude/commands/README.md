# Claude Commands - PRP System

Slash commands for creating and executing PRPs.

## Available Commands

| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/prp-planning-create` | Create PLANNING PRP from idea | Idea description |
| `/prp-create` | Create BASE PRP from requirements | Path to INITIAL.md |
| `/prp-base-execute` | Execute BASE PRP | Path to PRP file |
| `/prp-spec-execute` | Execute SPEC PRP | Path to SPEC file |
| `/prp-task-execute` | Execute TASK PRP | Path to task list |
| `/task-list-init` | Create task list | Project description |
| `/api-contract-define` | Define API contract | Feature name |
| `/read-docs` | Load project context | None |

## Command Workflow

### Creating a Feature (from scratch)

1. Create `workspace/PRPs/in-progress/INITIAL.md` with feature description
2. Run `/prp-create workspace/PRPs/in-progress/INITIAL.md`
3. Review generated PRP, add any missing context
4. Run `/prp-base-execute [generated-file].md`
5. Claude implements with validation loops

### Planning a Complex Feature

1. Run `/prp-planning-create "Your idea description"`
2. Answer clarifying questions
3. Review generated PRD
4. Use PRD as input for `/prp-create`

### Breaking Down Large Tasks

1. Run `/task-list-init "Project description"`
2. Review task list, adjust ordering
3. Run `/prp-task-execute task-list.md`
4. Claude executes tasks sequentially

## How Commands Work

Commands are markdown files with YAML frontmatter:

```yaml
---
name: command-name
description: What this command does
arguments: "Description of arguments"
---

# Command instructions follow...
```

When you type `/command-name`, Claude reads this file and follows the instructions.

## Creating Custom Commands

1. Create `.md` file in this directory
2. Add YAML frontmatter (name, description, arguments)
3. Write instructions for Claude to follow
4. Reload commands: Cmd/Ctrl+Shift+P → "Claude Code: Reload Commands"

## Tips

- Use `/read-docs` at start of each session for context
- Save completed PRPs to `workspace/PRPs/completed/` for future reference
- Create project-specific commands for common patterns