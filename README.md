# AI Research Template

![copier: template](https://img.shields.io/badge/copier-template-blue)

A Copier template for the code of a research project: one repository per paper, from the first experiment to the public release. Coding agents write most of the code, so the rules they follow are part of the template. Improvements found while using it in a project go back into the template.

## Quick Start

```bash
# Create a new project from this template
copier copy --trust gh:xzAscC/ai-research-template ./my_paper
```

> **Note:** The `--trust` flag is required because this template includes post-generation tasks that initialize git, sync dependencies with `uv`, and run tests.

## Usage

### Create a New Project

```bash
copier copy --trust gh:xzAscC/ai-research-template ./your_project_name
```

### Update an Existing Project

If you've already generated a project from this template, you can update it when the template changes:

```bash
cd your-project
copier update --trust
```

This preserves your customizations while applying template updates. `AGENTS.local.md` and `CLAUDE.local.md` are never overwritten.

## What a Project Gets

| Path | What it is | Source |
|------|------------|--------|
| `README.md` | Install, one command per result in the paper, pre-trained models, results, compute, and the versions and licenses of the models and data used | Papers with Code README template and ML Code Completeness Checklist; NeurIPS Paper Checklist items 4–8, 12 and 13 |
| `src/<project>/`, `scripts/`, `configs/`, `tests/` | Importable code; entry points `run_<experiment>.py` and `plot_<experiment>.py`; one YAML file per experiment; CPU tests, with `@pytest.mark.gpu` for tests that need a GPU, weights or the network | Good Research Code Handbook (layout); lightning-hydra-template (one config per experiment) |
| `data/`, `logs/`, `results/`, `figs/`, `checkpoints/`, `notebooks/` | Inputs and outputs. Only their `.gitkeep` is in git | Good Research Code Handbook; the Prefix repo |
| `SPEC.md` | The research question, and for each experiment what it compares, its metric, its output and its config | |
| `ARCHITECTURE.md` | The pipeline from config to figure, the components and the folders | |
| `AGENTS.md` | 13 short rules for coding agents: TDD, fixed folders, incremental logs, checkpoint and resume, large files on scratch, emails only from the agent through the agent-notify skill, draft PRs | The AGENTS.md of Prefix and PostDyn; kept short because long context files cost more and help little (see Sources) |
| `AGENTS.local.md`, `CLAUDE.local.md` | Private facts about machines, storage and credentials, and a pointer that makes Claude Code read both AGENTS files. Gitignored | Prefix and PostDyn |
| `REVIEW.md` | Rules for the pr-review skill: test command, risk paths, what counts as a failure | `REVIEW.template.md` of the pr-review skill |
| `.github/workflows/ci.yml` | `ruff check` and `pytest` | |

## Sources

- Papers with Code, [Tips for releasing research code in Machine Learning](https://github.com/paperswithcode/releasing-research-code): the ML Code Completeness Checklist and its README template.
- NeurIPS, [Paper Checklist](https://neurips.cc/public/guides/PaperChecklist): items 4–8 (reproducibility, open code, settings, error bars, compute), 12 (licenses) and 13 (new assets).
- P. Mineault, [The Good Research Code Handbook](https://goodresearch.dev/setup.html): one repository per paper, the `data docs results scripts src tests` layout, code installed as a package.
- [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template): experiment configs, per-run logs. Its Lightning and Hydra stack is not adopted.
- [Cookiecutter Data Science v2](https://cookiecutter-data-science.drivendata.org/): considered and not adopted, because it keeps data inside the repository.
- "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (ETH Zurich and LogicStar.ai, 2026; [summary](https://the-decoder.com/context-files-for-coding-agents-often-dont-help-and-may-even-hurt-performance/)): LLM-generated context files lowered success rates in most settings; short developer-written ones helped a little.

## Available Prompts

When you run `copier copy`, you'll be prompted for the following values:

| Prompt | Type | Description | Default |
|--------|------|-------------|---------|
| `project_name` | string | Your project name in `snake_case` (used for Python package naming) | `my_project` |
| `project_description` | string | Brief description of your project | `A Python project` |
| `author_name` | string | Your full name (used in LICENSE and `pyproject.toml`) | `Your Name` |
| `author_email` | string | Your email address (used in `pyproject.toml`) | `your.email@example.com` |

### Project Name Validation

The `project_name` must:
- Start with a lowercase letter
- Contain only lowercase letters, numbers, and underscores

Valid examples: `my_project`, `ai_research_2024`, `data_processor`

## Post-Generation Tasks

After `copier copy` (not after `copier update`), the following tasks run automatically:

1. **Git initialization** — `git init`, on branch `main`
2. **Dependency sync** — `uv sync`
3. **Test verification** — `uv run pytest`

These tasks require the `--trust` flag since they execute code on your system.

## Requirements

- Linux or macOS (the tasks run in a POSIX shell)
- [Copier](https://copier.readthedocs.io/) >= 9.6.0
- [uv](https://docs.astral.sh/uv/) (for post-generation tasks)
- Git

## Links

- [Copier Documentation](https://copier.readthedocs.io/en/stable/)
- [Copier Creating Templates Guide](https://copier.readthedocs.io/en/stable/creating/)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

MIT
