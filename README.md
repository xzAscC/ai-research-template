# Agent Engineering Template

A reusable Python template for AI-assisted development workflows.

## What This Is

This template provides a complete foundation for projects where AI agents (Claude Code, Cursor, Aider, etc.) handle implementation. It includes documentation structure, tooling configuration, and CI/CD setup optimized for AI-driven development.

## Quick Start

1. **Use this template**
   - Click "Use this template" on GitHub, or
   - Clone: `git clone <repo-url>`

2. **Rename the package**
   ```bash
   # Replace 'my_project' with your project name
   find . -type f -name "*.py" -o -name "*.toml" | xargs sed -i 's/my_project/your_project_name/g'
   mv src/my_project src/your_project_name
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Verify everything works**
   ```bash
   uv run ruff check src/ tests/
   uv run mypy src/
   uv run pytest
   ```

## What's Included

- **AGENTS.md** — AI agent operational policy (commands, escalation rules)
- **ARCHITECTURE.md** — System design template
- **docs/** — Documentation structure (design-docs, exec-plans, quality tracking)
- **pyproject.toml** — Configured with ruff, mypy, pytest
- **.github/** — CI workflow, PR template, issue templates

## Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  You define │───▶│  Write exec │───▶│  AI reads   │
│    tasks    │    │    plan     │    │    docs     │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   You       │◀───│  AI opens   │◀───│  AI codes,  │
│   review    │    │     PR      │    │  tests,     │
└─────────────┘    └─────────────┘    │  verifies   │
       │                               └─────────────┘
       ▼
┌─────────────┐
│   Merge     │───▶ Periodic: doc-gardening + refactor + tech debt cleanup
└─────────────┘
```

## File Structure

```
.
├── AGENTS.md              # AI agent instructions
├── ARCHITECTURE.md        # System design
├── README.md              # This file
├── pyproject.toml         # Project config
├── .python-version        # Python version
├── src/my_project/        # Source code
├── tests/                 # Test files
├── docs/
│   ├── design-docs/       # Design documents
│   ├── exec-plans/        # Execution plans
│   ├── PLANS.md           # Project roadmap
│   └── QUALITY_SCORE.md   # Quality tracking
└── .github/
    ├── workflows/ci.yml   # CI pipeline
    ├── pull_request_template.md
    └── ISSUE_TEMPLATE/    # Issue templates
```

## Renaming Guide

After cloning, replace all instances of `my_project`:

1. **pyproject.toml**: Change `name = "my_project"`
2. **src/my_project/**: Rename directory
3. **Imports**: Update all `from my_project` imports
4. **AGENTS.md**: Update package references

## License

[Add your license here]
