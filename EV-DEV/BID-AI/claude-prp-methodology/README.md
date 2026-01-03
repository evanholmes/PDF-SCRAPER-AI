# Claude PRP Methodology

**A systematic approach to AI-driven development using Product Requirement Prompts (PRPs)**

## What is this?

The PRP (Product Requirement Prompt) system is a methodology for transforming ideas into detailed, executable specifications that AI agents (Claude Code) can implement successfully on the first pass.

**Core Philosophy**: Context is king. PRPs provide so much detail that implementation becomes mostly mechanical, leaving AI to handle the creative/technical parts while following a clear roadmap.

## Why PRPs Work

1. **Context Density** - Include URLs, file paths, actual code examples (not just descriptions)
2. **Pattern Recognition** - Reference existing code patterns explicitly
3. **Gotcha Documentation** - Explicitly state common pitfalls and how to avoid them
4. **Validation Built-In** - Each task has a validation command - AI runs and fixes iteratively
5. **Pseudocode Guidance** - Enough detail to guide implementation without being boilerplate

## Quick Start (5 Steps)

1. **Install the package** - Copy this folder to your project directory
2. **Read SETUP.md** - Configure VS Code and Claude Code (< 30 minutes)
3. **Read METHODOLOGY.md** - Understand the 4 PRP types (< 1 hour)
4. **Create your first PRP** - Use `/prp-create` command with templates
5. **Execute it** - Use `/prp-base-execute` command and watch it work

## The 4 PRP Types

### 1. PLANNING PRP (`/prp-planning-create`)
**When**: You have a rough idea and need to flesh it out

**Output**: Comprehensive PRD with diagrams, user stories, architecture, phases

**Example**: "Build a notification system" → Detailed PRD with Mermaid diagrams, API specs, data models

### 2. BASE PRP (`/prp-create` → `/prp-base-execute`)
**When**: You have clear requirements and need implementation

**Output**: Complete implementation with tests, validation, and integration

**Example**: Authentication system, payment processing, search functionality

### 3. SPEC PRP (`/prp-spec-execute`)
**When**: You need to transform existing code systematically

**Output**: Step-by-step transformation with validation at each step

**Example**: Database migration, framework upgrade, refactoring

### 4. TASK PRP (`/task-list-init` → `/prp-task-execute`)
**When**: You have complex work that needs breaking down

**Output**: Checklist with embedded validation commands

**Example**: Multi-phase feature implementation, systematic code updates

## What's In This Package

```
claude-prp-methodology/
├── README.md (you are here)
├── SETUP.md (installation guide)
├── METHODOLOGY.md (deep dive into PRP system)
├── .claude/commands/ (8 slash commands)
├── templates/ (5 PRP templates)
├── examples/ (4 complete examples)
├── docs/ (workflow guides, best practices)
└── workspace/ (your PRPs and curated docs go here)
```

## Prerequisites

- **VS Code** (latest version)
- **Claude Code extension** (from VS Code marketplace)
- **Git** (for version control)
- Basic understanding of your tech stack (Python, TypeScript, Go, etc.)

## Table of Contents

- **[SETUP.md](SETUP.md)** - Installation and configuration
- **[METHODOLOGY.md](METHODOLOGY.md)** - The PRP system explained
- **[docs/PRP_WORKFLOW.md](docs/PRP_WORKFLOW.md)** - When to use which PRP type
- **[docs/VALIDATION_PATTERNS.md](docs/VALIDATION_PATTERNS.md)** - Testing strategies
- **[docs/TASK_KEYWORDS.md](docs/TASK_KEYWORDS.md)** - CREATE, MODIFY, MIRROR vocabulary
- **[docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md)** - Tips and patterns
- **[examples/](examples/)** - Real-world PRP examples

## Available Commands

Once configured, you'll have access to these `/` commands in Claude Code:

| Command | Purpose |
|---------|---------|
| `/prp-planning-create` | Transform rough ideas into comprehensive PRDs |
| `/prp-create` | Generate implementation PRPs from requirements |
| `/prp-base-execute` | Execute BASE PRPs with validation |
| `/prp-spec-execute` | Execute SPEC PRPs for transformations |
| `/prp-task-execute` | Execute TASK PRPs from checklists |
| `/task-list-init` | Create task lists for complex work |
| `/api-contract-define` | Define API contracts between backend/frontend |
| `/read-docs` | Load project context documents |

## Real-World Use Cases

**Full-stack Development**:
- Authentication systems
- Payment processing (Stripe, PayPal)
- Real-time features (WebSockets, SSE)
- Data export (CSV, PDF generation)
- Search functionality (Elasticsearch, Algolia)

**Backend Development**:
- API endpoints (REST, GraphQL)
- Database migrations
- Background jobs
- Caching layers
- Rate limiting

**Frontend Development**:
- Component libraries
- State management
- Form handling
- Data fetching
- Performance optimization

**DevOps**:
- CI/CD pipelines
- Docker containerization
- Infrastructure as code
- Monitoring setup

## Success Metrics

A good PRP enables:
- **First-pass success** - Implementation works without major rework
- **Self-service** - AI can implement without additional clarification
- **Validation loops** - AI can test and fix iteratively
- **Pattern consistency** - Code follows established patterns

## Next Steps

1. **Read [SETUP.md](SETUP.md)** - Get configured (< 30 min)
2. **Read [METHODOLOGY.md](METHODOLOGY.md)** - Understand the system (< 1 hour)
3. **Try an example** - See [examples/](examples/) for inspiration
4. **Create your first PRP** - Start small, get comfortable
5. **Iterate and improve** - PRPs are living documents

## Contributing

Found a bug? Have a suggestion? This is a living methodology - feedback welcome!

## License

See [LICENSE](LICENSE) file for details.

---

**Remember**: Great PRPs prevent implementation confusion. Invest time in planning, reap benefits in execution.