## 2026-03-20: pyproject.toml dependency conventions

- Use `dependencies = [...]` array under `[project]` section for production dependencies (PEP 621 standard)
- Use `[dependency-groups.dev]` for dev dependencies
- Keep dependencies in alphabetical order within each list
- Template files (.jinja) still need valid TOML syntax - Jinja variables are substituted at generation time

## 2026-03-20: Notify module skeleton patterns

- Module uses subpackage structure: `{{project_name_snake}}/notify/`
- Each file has module-level docstring
- Public functions use Google-style docstrings with Args/Returns/Raises
- Type hints use modern Python syntax (`list[str]`, `Path | None`)
- Stub implementations raise `NotImplementedError` with helpful messages
- `__init__.py` exports main public function (`send_task_notification`)
- Import Path from pathlib for file-related functions
## 2026-03-20: Test file conventions

- Test files in template must use `.jinja` extension for Copier processing
- Use `{{ project_name_snake }}` variable for imports (e.g., `from {{ project_name_snake }}.notify.core import ...`)
- Test class naming: `Test<Feature>` (e.g., `TestSendNotificationSuccess`, `TestRetryLogic`)
- TDD tests should FAIL initially - use `pytest.raises(NotImplementedError)` for stub tests
- Use `tmp_path: Path` fixture for file system tests
- Module docstrings on test files/classes/methods are acceptable for documenting test intent

## 2026-03-20: Sensitive data redaction patterns

- Use regex groups to preserve key names: `(key_pattern)\S+` → `\1[REDACTED]`
- Patterns implemented:
  - API keys: `sk-[a-zA-Z0-9]+`, `api_key[=:]\s*\S+`, `Bearer\s+\S+`
  - Passwords: `password[=:]\s*\S+`, `passwd\s+\S+`
  - Tokens: `token[=:]\s*\S+`, `auth[=:]\s*\S+`
- Apply patterns sequentially with `re.sub()` - order doesn't matter since patterns are non-overlapping
- Security code comments are justified for regex pattern categorization (audit purposes)

## 2026-03-20: Evidence module patterns

- Use `BLOCKED_EXTENSIONS: set[str]` module constant for blocked file extensions (case-insensitive comparison with `.lower()`)
- Custom exceptions extend `Exception` with pass body - e.g., `class EvidenceDirNotFoundError(Exception): pass`
- `Path.iterdir()` for non-recursive directory scanning, filter with `p.is_file()`
- Resend attachment format: `{"filename": str, "content": [bytes]}` - content must be list of bytes, not raw bytes
- Log warnings with `logger.warning("format string", variable)` - not f-strings for performance
- Check `directory.exists()` and `directory.is_dir()` before scanning
- Use `path.suffix.lower()` for extension comparison to handle case insensitivity
- Use `path.read_bytes()` to get file content as bytes
- Use `path.name` for just the filename (not full path)

## 2026-03-20: Email template implementation patterns

- Use `html.escape()` for ALL user-provided content (task_name, logs) to prevent XSS
- Email templates require inline CSS (style="...") because email clients strip `<style>` tags
- Use `<table>` for email layout for cross-client compatibility
- Status colors: success=#28a745 (green), failure=#dc3545 (red)
- Duration formatting: handle hours, minutes, seconds separately; skip zero units except seconds
- Function signature must match test calls exactly (e.g., `truncated=False` parameter)
- `attachment_info` parameter kept optional for future enhancement

## 2026-03-20: Core notification module patterns

- Import resend at module level: `import resend` and `from resend import exceptions`
- Set `resend.api_key` before calling `resend.Emails.send(params)`
- Retry pattern: tuple of retryable exceptions `(exceptions.RateLimitError, exceptions.ApplicationError)`
- Non-retryable exceptions: `MissingApiKeyError`, `InvalidApiKeyError`, `ValidationError`
- Use backoff delays as list `[1, 2, 4]` indexed by attempt number
- Custom exception `NotificationError(Exception)` follows same pattern as `EvidenceDirNotFoundError`
- Log redaction applies to each line individually before passing to email templates
- Truncated flag passed to both HTML and text email generators
- Attachments are optional in params dict - only add if present
- Resend email params: `from`, `to` (list), `subject`, `html`, `text`, `attachments` (optional)
- Use `@patch.dict(os.environ, {...})` for environment variable mocking in tests
- Use `@patch("module.path.resend.Emails.send")` for mocking the Resend API
- Template files show LSP errors for Jinja variables - this is expected behavior

## 2026-03-20: Package __init__.py export patterns

- Use explicit imports from submodules: `from .core import X, Y` and `from .evidence import Z`
- Define `__all__` list with exported symbols in alphabetical order
- Keep module docstrings brief - avoid duplicating `__all__` contents in docstring
- Import from multiple submodules separately (not `from .core import *`)
- Template path uses `{{ project_name_snake }}` for Copier variable substitution

## 2026-03-20: Integration test patterns

- Integration tests MUST use `@pytest.mark.integration` decorator to skip by default in CI
- Use `pytest.fixture(autouse=True)` to check env vars and call `pytest.skip()` if not set (graceful skip, not fail)
- File docstring must explain how to run: set env vars + `pytest -m integration`
- Test scenarios: success with evidence, failure notification, multiple evidence files, long-running tasks
- Use `tmp_path: Path` fixture for creating temporary evidence directories
- Create evidence files with `write_text()` for text and `write_bytes()` for binary
- Import exceptions (`NotificationError`, `EvidenceDirNotFoundError`) from `{{ project_name_snake }}.notify`
- Integration tests verify real API calls return email IDs (non-None strings)
