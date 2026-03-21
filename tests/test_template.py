"""Tests for Copier template generation using pytest-copie."""

from pathlib import Path


def test_template_generates_successfully(copie):
    """Test that the template generates without errors."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    assert result.exit_code == 0
    assert result.project_dir is not None
    assert result.exception is None


def test_pyproject_toml_exists(copie):
    """Test that pyproject.toml is generated in the project."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    project_dir: Path = result.project_dir
    pyproject_path = project_dir / "pyproject.toml"

    assert pyproject_path.exists()
    assert pyproject_path.is_file()


def test_placeholders_replaced(copie):
    """Test that all placeholders are replaced in generated files."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    project_dir: Path = result.project_dir

    # Check pyproject.toml has no template markers
    pyproject_path = project_dir / "pyproject.toml"
    pyproject_content = pyproject_path.read_text()

    assert "{{" not in pyproject_content
    assert "}}" not in pyproject_content


def test_no_template_name_in_generated_files(copie):
    """Test that no 'ai_research_template' references remain in generated files."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    project_dir: Path = result.project_dir

    # Check all text files for template name references
    for file_path in project_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix in {
            ".py",
            ".toml",
            ".md",
            ".yml",
            ".yaml",
            ".txt",
        }:
            content = file_path.read_text(errors="ignore")
            assert "ai_research_template" not in content.lower(), (
                f"Found 'ai_research_template' in {file_path}"
            )


def test_project_structure(copie):
    """Test that the generated project has the expected structure."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    project_dir: Path = result.project_dir

    # Check expected directories exist
    assert (project_dir / "test_project").is_dir()
    assert (project_dir / "tests").is_dir()
    assert (project_dir / "docs").is_dir()

    # Check key files exist
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "LICENSE").exists()


def test_project_name_used_correctly(copie):
    """Test that project_name is properly used in generated files."""
    result = copie.copy(
        extra_answers={
            "project_name": "my_awesome_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "include_template_docs": False,
        }
    )

    project_dir: Path = result.project_dir

    # Check package directory is named correctly
    assert (project_dir / "my_awesome_project").is_dir()

    # Check pyproject.toml uses snake_case name
    pyproject_content = (project_dir / "pyproject.toml").read_text()
    assert 'name = "my_awesome_project"' in pyproject_content


def test_author_info_in_pyproject(copie):
    """Test that author information is correctly placed in pyproject.toml."""
    result = copie.copy(
        extra_answers={
            "project_name": "test_project",
            "project_description": "My custom description",
            "author_name": "Jane Doe",
            "author_email": "jane@example.com",
            "include_template_docs": False,
        }
    )

    pyproject_content = (result.project_dir / "pyproject.toml").read_text()

    assert "My custom description" in pyproject_content
