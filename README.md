# AI Research Template

A Copier template for creating new AI research Python projects with best practices built-in.

## Quick Start

```bash
# Create a new project from this template
copier copy --trust https://github.com/your-org/ai-research-template.git ./my-new-project
```

> **Note:** The `--trust` flag is required because this template includes post-generation tasks that initialize git, sync dependencies with `uv`, and run tests.

## Usage

### Create a New Project

```bash
copier copy --trust https://github.com/your-org/ai-research-template.git ./your-project-name
```

### Update an Existing Project

If you've already generated a project from this template, you can update it when the template changes:

```bash
cd your-project
copier update --trust
```

This preserves your customizations while applying template updates.

## Available Prompts

When you run `copier copy`, you'll be prompted for the following values:

| Prompt | Type | Description | Default |
|--------|------|-------------|---------|
| `project_name` | string | Your project name in `snake_case` (used for Python package naming) | `my_project` |
| `project_description` | string | Brief description of your project | `A Python project` |
| `author_name` | string | Your full name (used in LICENSE and `pyproject.toml`) | `Your Name` |
| `author_email` | string | Your email address (used in `pyproject.toml`) | `your.email@example.com` |
| `include_template_docs` | bool | Whether to include `TEMPLATE.md` in the generated project | `false` |

### Project Name Validation

The `project_name` must:
- Start with a lowercase letter
- Contain only lowercase letters, numbers, and underscores

Valid examples: `my_project`, `ai_research_2024`, `data_processor`

## Post-Generation Tasks

After project generation, the following tasks run automatically:

1. **Git initialization** — `git init`
2. **Dependency sync** — `uv sync`
3. **Test verification** — `uv run pytest`

These tasks require the `--trust` flag since they execute code on your system.

## Requirements

- [Copier](https://copier.readthedocs.io/) >= 9.0.0
- [uv](https://docs.astral.sh/uv/) (for post-generation tasks)
- Git

## Links

- [Copier Documentation](https://copier.readthedocs.io/en/stable/)
- [Copier Creating Templates Guide](https://copier.readthedocs.io/en/stable/creating/)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

MIT
