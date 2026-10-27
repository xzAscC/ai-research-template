"""Tests for Copier template generation using pytest-copie.

Each copy also runs the template's tasks (git init, uv sync, uv run pytest), so a
successful copy means the generated project's own tests pass.
"""

import subprocess
from pathlib import Path

import pytest

ANSWERS = {
    "project_name": "test_project",
    "project_description": "My custom description",
    "author_name": "Jane Doe",
    "author_email": "jane@example.com",
}

TEXT_SUFFIXES = {".py", ".toml", ".md", ".yml", ".yaml", ".txt", ".example", ""}


@pytest.fixture(scope="session")
def project(copie_session) -> Path:
    result = copie_session.copy(extra_answers=ANSWERS)
    assert result.exception is None, result.exception
    assert result.exit_code == 0
    return result.project_dir


def _text_files(project_dir: Path) -> list[Path]:
    skip = {".git", ".venv", ".pytest_cache", ".ruff_cache", "__pycache__"}
    return [
        path
        for path in project_dir.rglob("*")
        if path.is_file()
        and not skip & set(path.relative_to(project_dir).parts)
        and path.suffix in TEXT_SUFFIXES
    ]


def test_expected_files_exist(project: Path) -> None:
    for name in [
        "README.md",
        "SPEC.md",
        "ARCHITECTURE.md",
        "AGENTS.md",
        "AGENTS.local.md",
        "CLAUDE.local.md",
        "REVIEW.md",
        "LICENSE",
        "pyproject.toml",
        ".python-version",
        ".gitignore",
        ".copier-answers.yml",
        ".github/workflows/ci.yml",
        "src/test_project/__init__.py",
        "tests/test_package.py",
    ]:
        assert (project / name).is_file(), name


def test_folders_are_kept_by_gitkeep(project: Path) -> None:
    for folder in [
        "configs",
        "scripts",
        "data",
        "logs",
        "results",
        "figs",
        "checkpoints",
        "notebooks",
    ]:
        assert (project / folder / ".gitkeep").is_file(), folder


def test_removed_files_are_gone(project: Path) -> None:
    for name in [
        "docs",
        "TEMPLATE.md",
        ".github/ISSUE_TEMPLATE",
        "test_project",
        "src/test_project/hello.py",
        # emails come from the agent (agent-notify skill), not from experiment code
        "src/test_project/notify.py",
        "tests/test_notify.py",
        ".env.example",
    ]:
        assert not (project / name).exists(), name


def test_placeholders_replaced(project: Path) -> None:
    for path in _text_files(project):
        content = path.read_text(errors="ignore")
        assert "{{" not in content and "}}" not in content, path
        assert "ai_research_template" not in content.lower(), path


def test_pyproject_uses_answers(project: Path) -> None:
    content = (project / "pyproject.toml").read_text()
    assert 'name = "test_project"' in content
    assert "My custom description" in content
    assert "Jane Doe" in content
    assert "jane@example.com" in content
    assert 'requires-python = ">=3.13"' in content
    assert (project / ".python-version").read_text().strip() == "3.13"


def test_license_has_author_and_year(project: Path) -> None:
    content = (project / "LICENSE").read_text()
    assert "Jane Doe" in content
    assert "Copyright (c) 20" in content


def test_private_files_and_outputs_are_ignored(project: Path) -> None:
    for path in [
        "AGENTS.local.md",
        "CLAUDE.local.md",
        ".env",
        "results/x.json",
        "logs/x/run.log",
        "figs/x.pdf",
    ]:
        check = subprocess.run(["git", "check-ignore", "-q", path], check=False, cwd=project)
        assert check.returncode == 0, f"{path} is not ignored"
    for path in ["AGENTS.md", "results/.gitkeep", "configs/exp1.yaml"]:
        check = subprocess.run(["git", "check-ignore", "-q", path], check=False, cwd=project)
        assert check.returncode == 1, f"{path} is ignored"


def test_generated_project_passes_ruff(project: Path) -> None:
    check = subprocess.run(
        ["uv", "run", "ruff", "check"], check=False, cwd=project, capture_output=True, text=True
    )
    assert check.returncode == 0, check.stdout + check.stderr


def test_project_name_used_correctly(copie) -> None:
    result = copie.copy(extra_answers={**ANSWERS, "project_name": "my_awesome_project"})
    assert result.exit_code == 0, result.exception

    assert (result.project_dir / "src" / "my_awesome_project" / "__init__.py").is_file()
    assert 'name = "my_awesome_project"' in (result.project_dir / "pyproject.toml").read_text()
    assert "src/my_awesome_project/" in (result.project_dir / "ARCHITECTURE.md").read_text()


def test_git_branch_is_main(project: Path) -> None:
    # CI runs on main; a plain `git init` would give master on default git settings
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        check=True,
        cwd=project,
        capture_output=True,
        text=True,
    )
    assert branch.stdout.strip() == "main"
