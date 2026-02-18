---
name: prp-create
description: Generate a complete, production-grade Product Requirement Prompt (PRP) by performing deep, agentic research
arguments: "Path to the initial feature request file (e.g., INITIAL.md)"
---

# Command: /prp-create
# Argument: $ARGUMENTS (Path to the initial feature request file, e.g., INITIAL.md)

## GOAL
Generate a complete, production-grade Product Requirement Prompt (PRP) by performing deep, agentic research based on an initial user request. The goal is to create a PRP so comprehensive that it enables one-pass implementation success.

## CONTEXT
- **User Request File:** $ARGUMENTS
- **PRP Template:** workspace/PRPs/templates/prp.md (use the template from this package)
- **Codebase:** The entire project directory
- **AI Docs:** The curated documentation in workspace/ai_docs/

---

## PROCESS

### 1. Ingest & Understand Initial Request
- Read the user-provided file at `$ARGUMENTS`
- Identify the core feature, user-provided examples, documentation links, and other considerations
- Clarify any ambiguities with the user upfront

### 2. Deep & Agentic Research Phase
> **Strategy:** Optimize for certainty and success, not speed. Use your full agentic capabilities.

- **ULTRATHINK:** Formulate a detailed research plan. Break it down into tasks for sub-agents using `TodoWrite`
- **Codebase Analysis (Sub-Agent Task):**
  - Search the codebase for any similar features, patterns, or modules
  - Identify all relevant files (code, tests, configs) to be used as patterns
  - Note all conventions (naming, styling, architecture) to be followed
  - Find existing API endpoints, database schemas, component structures
  - Identify integration patterns (how features connect together)
- **External Research (Sub-Agent Task):**
  - Perform deep web searches for library documentation, implementation examples, best practices, and common pitfalls related to the feature
  - Research framework-specific patterns (React hooks, FastAPI routers, etc.)
  - Find official documentation for key libraries
  - Look for common gotchas and edge cases
  - For critical documentation, summarize it into a new `.md` file in `workspace/ai_docs/` and reference it
- **Synthesize Findings:** Consolidate all research from your sub-agents into a coherent knowledge base for the next step

### 3. PRP Generation Phase
> **Strategy:** Use the gathered research to meticulously fill out the `templates/prp.md` template. Be precise and information-dense.

- **Fill `All Needed Context`:**
  - Populate the YAML block with URLs, file paths, and references to `ai_docs/`
  - Run `tree` to populate the codebase overview
  - Draw the desired codebase tree with the new files
  - Document all critical gotchas and library quirks found during research
  - Include actual code examples from the codebase (not just file paths)
- **Create `Implementation Blueprint`:**
  - Define data models first (database schemas, TypeScript interfaces, API contracts)
  - Create a list of tasks using precise keywords (`CREATE`, `MODIFY`, `MIRROR`, `REFACTOR`)
  - Write detailed pseudocode for complex tasks, referencing established patterns
  - Order tasks logically (database → backend → frontend, or similar)
  - Include integration points (API endpoints, event handlers, state management)
- **Define `Validation Loop`:**
  - Create a robust, multi-level validation loop (Syntax, Unit, Integration, Creative)
  - Write specific unit test cases and integration test commands
  - Level 1: Linting and type checking (`eslint`, `tsc`, `ruff`, `mypy`)
  - Level 2: Unit tests (`pytest`, `vitest`, `jest`)
  - Level 3: Integration tests (`curl` for APIs, browser tests for UI)
  - Level 4: Creative validation (performance checks, edge cases, user flows)

### 4. Quality Check & Output
- **Review:** Read through the generated PRP. Does it contain everything an AI agent would need?
- **Score:** Add a confidence score (1-10) for one-pass implementation success
- **Output:** Save the final PRP as `workspace/PRPs/in-progress/{feature-name}.md`

## Examples of Features to Create PRPs For

- **Authentication System:** User login, registration, password reset
- **Payment Processing:** Stripe integration, checkout flow, webhooks
- **Real-time Chat:** WebSocket implementation, message persistence
- **Data Export:** CSV/PDF generation, background jobs
- **Search Functionality:** Elasticsearch integration, autocomplete
- **File Upload:** S3 storage, image processing, validation
- **Admin Dashboard:** CRUD operations, data tables, filters
- **API Rate Limiting:** Redis-based throttling, token buckets
- **Email Notifications:** Template system, queue processing

## What Makes a Great PRP

1. **Context Density:** Include URLs, file paths, actual code examples
2. **Pattern Recognition:** Reference existing code patterns explicitly
3. **Gotcha Documentation:** Explicitly state common pitfalls
4. **Validation Built-In:** Each task has a validation command
5. **Pseudocode:** Enough detail to guide implementation
6. **Comprehensive Research:** Web searches + codebase analysis

EOF < /dev/null