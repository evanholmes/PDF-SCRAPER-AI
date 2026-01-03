---
command: read-docs
description: Read essential project context documents
signature: ""
arguments: []
---

Read the core project context documents that provide essential information for working in your codebase. This command establishes the foundation for effective AI-assisted development.

This command automatically reads:

1. **README.md** - Project overview and quick reference
   - Project purpose and goals
   - Key features and architecture overview
   - Directory structure and organization
   - Setup and installation instructions
   - Command discovery and usage
   - Quick start guides for common tasks

2. **CLAUDE.md** (if present) - AI-specific context and working patterns
   - Project-specific AI instructions
   - Repository structure and patterns
   - Command system documentation
   - Working patterns and Git workflow
   - Coding standards and conventions
   - Architecture decisions and rationale

3. **workspace/ai_docs/** - Curated technical documentation
   - Framework documentation (cached for quick reference)
   - API references and SDK docs
   - Library gotchas and common pitfalls
   - Implementation patterns and examples
   - Integration guides and tutorials

These documents establish:
- The project's goals and context
- Repository organization and standards
- Available commands and workflows
- Current priorities and focus areas
- Development protocols and patterns
- Git and collaboration guidelines

After reading these documents, Claude will have the essential context to:
- Navigate the repository structure correctly
- Use appropriate commands for tasks
- Maintain code quality and consistency standards
- Follow established workflows and patterns
- Understand the project's architecture and goals
- Reference curated documentation effectively

Usage:
```
/read-docs
```

No arguments required. This command should be run at the start of any significant work session to ensure full context awareness.

## Setting Up Project Context

For your projects, create these files:

### README.md
Standard project documentation:
- What the project does
- How to set it up
- How to run it
- Key commands and workflows
- Directory structure

### CLAUDE.md (optional but recommended)
AI-specific instructions:
- Architecture patterns to follow
- Coding conventions
- Testing requirements
- Common gotchas
- File organization principles

### workspace/ai_docs/
Cache important documentation here:
- Framework docs (React, FastAPI, etc.)
- API references
- Library quirks and patterns
- Integration guides
- Copy from official docs or create summaries

This makes future sessions faster and more accurate.