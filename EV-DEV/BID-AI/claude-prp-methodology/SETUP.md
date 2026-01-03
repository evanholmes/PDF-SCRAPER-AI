# Setup Guide - Claude PRP Methodology

Get up and running with the PRP system in under 30 minutes.

## Prerequisites Check

Before starting, ensure you have:

- [ ] **VS Code** installed (version 1.80 or higher)
- [ ] **Git** installed and configured
- [ ] **Claude Code extension** (we'll install this)
- [ ] **Basic command line knowledge** (cd, ls, cp)

## Step 1: Install VS Code (if needed)

1. Download VS Code from https://code.visualstudio.com/
2. Install following default instructions for your OS
3. Launch VS Code to verify installation

**Time**: 5 minutes

## Step 2: Install Claude Code Extension

1. Open VS Code
2. Click Extensions icon in sidebar (or Cmd/Ctrl+Shift+X)
3. Search for "Claude Code"
4. Click "Install" on the official Anthropic extension
5. Wait for installation to complete
6. Click "Reload" if prompted

**Verification**:
- Open Command Palette (Cmd/Ctrl+Shift+P)
- Type "Claude"
- You should see Claude Code commands

**Time**: 5 minutes

## Step 3: Copy PRP Methodology to Your Project

Option A: **Copy entire folder** (recommended for new projects)
```bash
# Navigate to your project directory
cd ~/Projects/your-project

# Copy the PRP methodology folder
cp -r ~/Desktop/claude-prp-methodology/.claude .
cp -r ~/Desktop/claude-prp-methodology/workspace .

# Create .gitignore for workspace (optional)
echo "workspace/PRPs/in-progress/*" >> .gitignore
echo "workspace/PRPs/completed/*.md" >> .gitignore
echo "!workspace/PRPs/in-progress/.gitkeep" >> .gitignore
```

Option B: **Symlink for multiple projects** (advanced)
```bash
# Create a central location
mkdir -p ~/.claude-methodology
cp -r ~/Desktop/claude-prp-methodology/.claude ~/.claude-methodology/
cp -r ~/Desktop/claude-prp-methodology/workspace ~/.claude-methodology/

# Symlink to each project
cd ~/Projects/project1
ln -s ~/.claude-methodology/.claude .claude
ln -s ~/.claude-methodology/workspace workspace

cd ~/Projects/project2
ln -s ~/.claude-methodology/.claude .claude
ln -s ~/.claude-methodology/workspace workspace
```

**Time**: 2 minutes

## Step 4: Configure Claude Code

1. Open your project in VS Code
2. Verify `.claude/commands/` directory exists
3. Open Command Palette (Cmd/Ctrl+Shift+P)
4. Type "Claude Code: Reload Commands"
5. Press Enter

**Verification**:
- Open Command Palette
- Type `/` to see available commands
- You should see `/prp-create`, `/prp-base-execute`, etc.

**Time**: 2 minutes

## Step 5: Set Up Workspace Folders

Create the working directories for your PRPs:

```bash
cd your-project-directory

# Create workspace structure (if you didn't copy it)
mkdir -p workspace/PRPs/in-progress
mkdir -p workspace/PRPs/completed
mkdir -p workspace/ai_docs

# Add .gitkeep files to preserve empty directories
touch workspace/PRPs/in-progress/.gitkeep
touch workspace/PRPs/completed/.gitkeep
touch workspace/ai_docs/.gitkeep
```

**Time**: 1 minute

## Step 6: Create Project Context Files (Optional but Recommended)

### Create README.md (if you don't have one)

```bash
touch README.md
```

Add basic project info:
- What the project does
- How to set it up
- How to run it
- Directory structure

### Create CLAUDE.md (recommended)

```bash
touch CLAUDE.md
```

Add AI-specific instructions:
```markdown
# Project Context for Claude

## Architecture Patterns
- [Describe your architecture]
- [Key design decisions]

## Coding Conventions
- [Naming conventions]
- [File organization]
- [Testing requirements]

## Common Gotchas
- [Library quirks]
- [Framework-specific issues]
- [Performance considerations]

## File Organization
- [Where different types of files go]
```

**Time**: 5-10 minutes (optional)

## Step 7: Test Your Setup

### Test 1: Command Discovery
1. Open VS Code Command Palette (Cmd/Ctrl+Shift+P)
2. Type `/`
3. Verify you see PRP commands listed

### Test 2: Read Docs Command
1. In Claude Code chat, type: `/read-docs`
2. Press Enter
3. Claude should read your README.md and CLAUDE.md

### Test 3: Create a Simple PRP
1. Create a file: `workspace/PRPs/in-progress/INITIAL.md`
2. Add content:
   ```markdown
   # Feature Request: Add Health Check Endpoint

   Create a simple /health endpoint that returns:
   - Status: "ok"
   - Version: from package.json
   - Uptime: server uptime in seconds
   ```
3. In Claude Code chat, type: `/prp-create workspace/PRPs/in-progress/INITIAL.md`
4. Claude should generate a complete PRP

**Time**: 5 minutes

## Troubleshooting

### Commands Not Showing Up

**Problem**: `/prp-create` and other commands don't appear

**Solutions**:
1. Verify `.claude/commands/` directory exists in project root
2. Check that command files have `.md` extension
3. Reload Claude Code: Cmd/Ctrl+Shift+P → "Claude Code: Reload Commands"
4. Restart VS Code

### Claude Can't Find Templates

**Problem**: "Template not found" error when creating PRPs

**Solutions**:
1. Verify `workspace/PRPs/templates/` exists with prp.md files
2. Check file permissions (should be readable)
3. Use absolute paths in commands if needed

### Workspace Folders Not Found

**Problem**: "Cannot find workspace/PRPs" error

**Solutions**:
1. Ensure you're in the project root directory
2. Create folders manually: `mkdir -p workspace/PRPs/{in-progress,completed}`
3. Check that VS Code opened the correct project folder

### Extension Not Working

**Problem**: Claude Code extension not responding

**Solutions**:
1. Check you have the official Anthropic extension (not a clone)
2. Restart VS Code
3. Check VS Code version (needs 1.80+)
4. Check extension logs: View → Output → Select "Claude Code"

## Directory Structure After Setup

Your project should look like this:

```
your-project/
├── .claude/
│   └── commands/           # PRP commands
│       ├── prp-create.md
│       ├── prp-base-execute.md
│       └── ... (8 total)
├── workspace/
│   ├── PRPs/
│   │   ├── in-progress/    # Active PRPs
│   │   └── completed/      # Finished PRPs
│   └── ai_docs/           # Curated documentation
├── README.md              # Project overview
├── CLAUDE.md              # AI-specific context (optional)
└── [your project files]
```

## Next Steps

1. **Read [METHODOLOGY.md](METHODOLOGY.md)** - Understand the PRP system deeply
2. **Try the examples** - See [examples/](examples/) for real PRPs
3. **Create your first real PRP** - Start with something small
4. **Iterate** - PRPs improve with practice

## Tips for Success

1. **Start Small** - Your first PRP should be simple (< 100 lines)
2. **Copy Examples** - Use [examples/](examples/) as templates
3. **Iterate** - PRPs are living documents, update as you learn
4. **Curate Docs** - Save important documentation in `workspace/ai_docs/`
5. **Use Read-Docs** - Run `/read-docs` at the start of each session

## Common Workflows

### Starting a New Feature
1. Create `INITIAL.md` with feature description
2. Run `/prp-create INITIAL.md`
3. Review generated PRP, add context
4. Run `/prp-base-execute [generated-prp].md`
5. Claude implements with validation loops

### Planning a Complex Project
1. Run `/prp-planning-create "Your idea description"`
2. Answer clarifying questions
3. Get comprehensive PRD with diagrams
4. Use PRD to create implementation PRPs

### Breaking Down Large Tasks
1. Run `/task-list-init "Project description"`
2. Get detailed task list with validation commands
3. Run `/prp-task-execute [task-list].md`
4. Claude works through tasks sequentially

---

**Setup Complete!** 🎉

You're ready to use the PRP methodology. Next: [METHODOLOGY.md](METHODOLOGY.md)