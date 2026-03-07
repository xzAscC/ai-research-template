# AGENTS.md

AI agents working in this repository MUST follow these rules.

## 1) Repository Snapshot

- Package manager: `uv`
- Python: 3.12+ (see `.python-version`)
- Lint/Format: `ruff`
- Type check: `mypy`
- Test: `pytest`

## 2) Build & Verify Commands

```bash
# Install dependencies
uv sync

# Lint check
uv run ruff check src/ tests/

# Format check
uv run ruff format --check src/ tests/

# Format fix
uv run ruff format src/ tests/

# Type check
uv run mypy src/

# Run all tests
uv run pytest

# Run single test file
uv run pytest tests/test_hello.py

# Run test by name
uv run pytest -k "test_name"
```

## 3) Definition of Done

Before opening a PR, ALL of these must pass:

- [ ] `uv sync` completes without errors
- [ ] `uv run ruff check src/ tests/` → 0 violations
- [ ] `uv run ruff format --check src/ tests/` → already formatted
- [ ] `uv run mypy src/` → Success with 0 errors
- [ ] `uv run pytest` → all tests pass

## 4) When Writing Code

- Use ESM-style imports (from x import y)
- Group imports: stdlib → third-party → local
- Use type hints on ALL function parameters and returns
- Never use `Any` — use `unknown` patterns or proper types
- Fail fast on invalid input
- Throw typed/domain-specific errors
- Preserve original error as `cause` when wrapping

## 5) When Writing Tests

- Use pytest style (plain functions, assert statements)
- Cover: happy path, edge cases, failure paths
- Keep tests deterministic and isolated
- Mock external boundaries (network, file I/O)

## 6) When Opening a PR

Include in description:
1. Summary of changes (2-3 sentences)
2. Linked issue (Closes #N)
3. Verification output (paste command results)
4. Self-review checklist completion
5. Risks & considerations

## 7) Escalation Rules

STOP and report to human if:
- Modifying more than 5 files not in the original plan
- Encountering unclear requirements after 2 clarification attempts
- Need to add new dependencies
- Changes affect security (auth, secrets, permissions)
- Test coverage would drop below existing level

## 8) Code Style

Enforced by ruff (see pyproject.toml):
- Line length: 100
- Quote style: double
- Naming: snake_case for functions/vars, PascalCase for classes

## 9) Architecture Cross-References

- System design: `ARCHITECTURE.md`
- Design docs: `docs/design-docs/`
- Exec plans: `docs/exec-plans/`
- Quality tracking: `docs/QUALITY_SCORE.md`
