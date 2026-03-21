# Copier Template Conversion

## TL;DR

> **Quick Summary**: Convert ai-research-template to a Copier template, enabling easy project initialization with automated placeholder replacement and post-generation setup.
>
> **Deliverables**:
> - `copier.yml` configuration with prompts and computed values
> - All project references converted to `{{variable}}` placeholders
> - `template/` subdirectory structure for cleaner organization
> - Template test using pytest-copie
> - Git branch for this work
>
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Branch → copier.yml → template files → test

---

## Context

### Original Request
User wants to make it easier to reuse the AI Research Template when creating new projects. Currently requires manual `find` + `sed` commands to replace project references. Goal: Use Copier templating system for automated initialization.

### Interview Summary
**Key Discussions**:
- **Approach**: Copier (chosen over cookiecutter and custom script)
- **Placeholders**: Use `{{variable}}` Jinja2 syntax
- **Cleanup**: Offer to remove template-specific files after generation
- **Testing**: Include template generation test
- **Inconsistency**: Templatize `__init__.py` docstring (was "Agent Engineering Template")

**Research Findings**:
- 16 occurrences of `ai_research_template` in 6 files
- LICENSE has hardcoded author name - needs templating
- Copier supports `_subdirectory`, `_exclude`, `_tasks`, validators
- pytest-copie for testing Copier templates

### Metis Review
**Identified Gaps** (addressed):
- **LICENSE templating**: Added `{{author_name}}` and `{{copyright_year}}`
- **`template/` subdirectory**: Added restructure task
- **Answers file**: Added for `copier update` support
- **Validators**: Added regex validation for project names
- **pytest-copie**: Added as test dependency

---

## Work Objectives

### Core Objective
Transform the ai-research-template repository into a Copier template that allows users to create new projects with a single `copier copy` command.

### Concrete Deliverables
- `copier.yml` with prompts and computed values
- `template/` subdirectory containing all templated files
- `{{_copier_conf.answers_file}}.jinja` for upgradability
- All 8+ files converted to use `{{variable}}` placeholders
- `tests/test_template.py` with pytest-copie

### Definition of Done
- [x] `copier copy . /tmp/test-project` creates valid project
- [x] Generated project passes `uv sync`, `ruff check`, `mypy`, `pytest`
- [x] All placeholders replaced with user-provided values
- [x] No "ai_research_template" or "AI Research Template" in generated output

### Must Have
- Working Copier template with `copier copy` command
- `project_name`, `project_slug`, `project_name_snake`, `project_display_name` variables
- Template test that verifies generation succeeds
- `_tasks` for `git init` and `uv sync`

### Must NOT Have (Guardrails)
- Manual find/sed instructions in README (replaced by Copier workflow)
- Hardcoded author names or years in LICENSE
- Missing validators allowing invalid Python identifiers
- Shell string commands in `_tasks` (use array syntax)
- Edit `.sisyphus/plans/` existing content

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (pytest)
- **Automated tests**: YES (pytest-copie)
- **Framework**: pytest + pytest-copie
- **Test type**: Tests-after (template must exist first)

### QA Policy
Every task includes agent-executed QA scenarios.

- **Template generation**: Use Bash (copier copy) — Generate project, verify structure
- **Placeholder replacement**: Use Grep — Search for old references, should find none
- **Project validation**: Use Bash — Run uv sync, ruff, mypy, pytest on generated project
- **Evidence**: Screenshots of terminal output in `.sisyphus/evidence/`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation - 4 tasks, can start immediately):
├── Task 1: Create git branch [quick]
├── Task 2: Create template/ subdirectory structure [quick]
├── Task 3: Create copier.yml configuration [quick]
└── Task 4: Create answers file template [quick]

Wave 2 (Core Templating - 5 tasks, after Wave 1):
├── Task 5: Template pyproject.toml [quick]
├── Task 6: Template src/{{project_name_snake}}/ directory [quick]
├── Task 7: Template tests/test_hello.py [quick]
├── Task 8: Template LICENSE file [quick]
└── Task 9: Configure _exclude in copier.yml [quick]

Wave 3 (Documentation - 5 tasks, after Wave 2):
├── Task 10: Template README.md [quick]
├── Task 11: Template ARCHITECTURE.md [quick]
├── Task 12: Template SPEC.md [quick]
├── Task 13: Template AGENTS.md [quick]
└── Task 14: Update root README for Copier usage [quick]

Wave 4 (Testing & Validation - 3 tasks, after Wave 3):
├── Task 15: Add pytest-copie dependency [quick]
├── Task 16: Create template test [quick]
└── Task 17: Test template generation end-to-end [unspecified-high]

Wave FINAL (4 parallel reviews):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA - copier copy test (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: T1 → T3 → T5 → T15 → T17 → F1-F4 → user okay
Parallel Speedup: ~60% faster than sequential
Max Concurrent: 5 (Wave 2)
```

### Dependency Matrix

- **1**: — — 2-17, 1
- **2**: 1 — 5-14, 1
- **3**: 1 — 9, 4, 1
- **4**: 3 — — 1
- **5-8**: 2 — 15, 17, 1
- **9**: 3 — — 1
- **10-14**: 2 — — 1
- **15**: 5-8 — 16, 1
- **16**: 15 — 17, 1
- **17**: 16 — F1-F4, 1
- **F1-F4**: 17 — user okay, 1

### Agent Dispatch Summary

- **Wave 1**: 4 tasks → all `quick`
- **Wave 2**: 5 tasks → all `quick`
- **Wave 3**: 5 tasks → all `quick`
- **Wave 4**: 3 tasks → T15-T16 `quick`, T17 `unspecified-high`
- **Final**: 4 tasks → F1 `oracle`, F2-F3 `unspecified-high`, F4 `deep`

---

## TODOs

- [x] 1. Create Git Branch for Copier Conversion

  **What to do**:
  - Create a new git branch named `feature/copier-template`
  - Push to remote for tracking
  - Verify branch is clean and ready for work

  **Must NOT do**:
  - Modify any files in this step
  - Create commits without changes

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple git operation, single command
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (starts first)
  - **Blocks**: Tasks 2-16
  - **Blocked By**: None (can start immediately)

  **References**:
  - Git workflow conventions in this repository

  **Acceptance Criteria**:
  - [ ] Branch `feature/copier-template` exists locally
  - [ ] `git branch --show-current` outputs `feature/copier-template`

  **QA Scenarios**:
  ```
  Scenario: Branch creation
    Tool: Bash
    Steps:
      1. git branch --show-current
    Expected Result: "feature/copier-template"
    Evidence: .sisyphus/evidence/task-1-branch-check.txt
  ```

  **Commit**: NO (no changes yet)

- [x] 2. Create Template Subdirectory Structure

  **What to do**:
  - Create `template/` directory at repository root
  - Move source files into `template/`:
    - `src/` → `template/src/`
    - `tests/` → `template/tests/`
    - `docs/` → `template/docs/`
    - `.github/` → `template/.github/`
    - `pyproject.toml` → `template/pyproject.toml`
    - `.python-version` → `template/.python-version`
    - `README.md` → `template/README.md`
    - `ARCHITECTURE.md` → `template/ARCHITECTURE.md`
    - `SPEC.md` → `template/SPEC.md`
    - `LICENSE` → `template/LICENSE`
    - `AGENTS.md` → `template/AGENTS.md`
  - Keep at root: `copier.yml`, `.sisyphus/`, `.git/`, root `README.md` (for template repo)
  - Add `_subdirectory: template` to copier.yml (Task 3)

  **Must NOT do**:
  - Move `.sisyphus/` or `.git/` directories
  - Delete any files during move
  - Edit file contents yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: File system operations, no complex logic
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3, 4)
  - **Blocks**: Tasks 5-13
  - **Blocked By**: Task 1

  **References**:
  - Copier docs: https://copier.readthedocs.io/en/stable/configuring/#subdirectory

  **Acceptance Criteria**:
  - [ ] `template/` directory exists
  - [ ] `template/src/`, `template/tests/`, `template/pyproject.toml` exist
  - [ ] Root still has `.sisyphus/` and `.git/`

  **QA Scenarios**:
  ```
  Scenario: Directory structure
    Tool: Bash
    Steps:
      1. ls -la template/
      2. ls -la template/src/
    Expected Result: Both directories exist with expected files
    Evidence: .sisyphus/evidence/task-2-structure.txt
  ```

  **Commit**: YES (groups with Task 3)
  - Message: `feat(copier): add template/ subdirectory structure`
  - Files: template/

- [x] 3. Create copier.yml Configuration

  **What to do**:
  - Create `copier.yml` at repository root
  - Define prompts:
    - `project_name`: str, validated as Python identifier
    - `project_description`: str, default "A Python project"
    - `author_name`: str
    - `author_email`: str
    - `include_template_docs`: bool, default false
  - Define computed values (`when: false`):
    - `project_slug`: `{{ project_name | lower | replace('_', '-') }}`
    - `project_name_snake`: `{{ project_name | lower | replace('-', '_') }}`
    - `project_display_name`: `{{ project_name | replace('_', ' ') | replace('-', ' ') | title }}`
    - `copyright_year`: `{{ current_year }}`
  - Add `_min_copier_version: "9.0.0"`
  - Add `_subdirectory: template`
  - Add `_templates_suffix: .jinja`
  - Add `_exclude` list (Task 9 will populate)
  - Add `_tasks` for post-generation (git init, uv sync)

  **Must NOT do**:
  - Add invalid YAML syntax
  - Forget validators for project_name

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Configuration file creation, straightforward
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 4)
  - **Blocks**: Tasks 4, 9
  - **Blocked By**: Task 1

  **References**:
  - Copier configuring: https://copier.readthedocs.io/en/stable/configuring/
  - Example: https://github.com/iloveitaly/python-starter-template/blob/main/copier.yml

  **Acceptance Criteria**:
  - [ ] `copier.yml` exists at root
  - [ ] Contains all required prompts
  - [ ] Contains all computed values
  - [ ] YAML is valid (parse with Python)

  **QA Scenarios**:
  ```
  Scenario: YAML validation
    Tool: Bash
    Steps:
      1. python -c "import yaml; yaml.safe_load(open('copier.yml'))"
    Expected Result: No errors, parses successfully
    Evidence: .sisyphus/evidence/task-3-yaml-valid.txt

  Scenario: Required fields present
    Tool: Bash
    Steps:
      1. grep -E "project_name|author_name|_subdirectory" copier.yml
    Expected Result: All fields found
    Evidence: .sisyphus/evidence/task-3-fields.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `feat(copier): add copier.yml configuration`
  - Files: copier.yml

- [x] 4. Create Answers File Template

  **What to do**:
  - Create `template/{{_copier_conf.answers_file}}.jinja`
  - Content should output YAML of answers
  - This enables `copier update` functionality

  **Must NOT do**:
  - Hardcode the answers file name
  - Forget the `.jinja` suffix

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file creation with standard content
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3)
  - **Blocks**: None
  - **Blocked By**: Task 3 (needs `_templates_suffix`)

  **References**:
  - Copier answers file: https://copier.readthedocs.io/en/stable/configuring/#answers_file

  **Acceptance Criteria**:
  - [ ] File exists at `template/{{_copier_conf.answers_file}}.jinja`
  - [ ] Contains `{{ _copier_answers|to_nice_yaml }}`

  **QA Scenarios**:
  ```
  Scenario: Answers file template exists
    Tool: Bash
    Steps:
      1. ls -la "template/{{_copier_conf.answers_file}}.jinja"
      2. grep "copier_answers" "template/{{_copier_conf.answers_file}}.jinja"
    Expected Result: File exists with correct content
    Evidence: .sisyphus/evidence/task-4-answers.txt
  ```

  **Commit**: YES (groups with Tasks 2, 3)
  - Message: `feat(copier): add answers file template for copier update`
  - Files: template/{{_copier_conf.answers_file}}.jinja

- [x] 5. Template pyproject.toml

  **What to do**:
  - Rename `template/pyproject.toml` to `template/pyproject.toml.jinja`
  - Replace hardcoded values with placeholders:
    - Line 6: `name = "ai_research_template"` → `name = "{{ project_name_snake }}"`
    - Line 9: `description = "AI Research Template - ..."` → `description = "{{ project_description }}"`
    - Line 35: `packages = ["ai_research_template"]` → `packages = ["{{ project_name_snake }}"]`
  - Add optional author fields if not present

  **Must NOT do**:
  - Change tool configurations (ruff, mypy, pytest)
  - Modify dependency versions
  - Break YAML syntax

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text replacement with placeholders
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 6-9)
  - **Blocks**: Task 14
  - **Blocked By**: Task 2

  **References**:
  - Current file: `pyproject.toml` lines 6, 9, 35

  **Acceptance Criteria**:
  - [ ] File renamed to `pyproject.toml.jinja`
  - [ ] Contains `{{ project_name_snake }}` for package name
  - [ ] Contains `{{ project_description }}` for description

  **QA Scenarios**:
  ```
  Scenario: Placeholder presence
    Tool: Bash
    Steps:
      1. grep "project_name_snake" template/pyproject.toml.jinja
      2. grep "project_description" template/pyproject.toml.jinja
    Expected Result: Both placeholders found
    Evidence: .sisyphus/evidence/task-5-placeholders.txt

  Scenario: No old references
    Tool: Bash
    Steps:
      1. grep "ai_research_template" template/pyproject.toml.jinja || echo "clean"
    Expected Result: "clean" (no matches)
    Evidence: .sisyphus/evidence/task-5-no-old-refs.txt
  ```

  **Commit**: NO (groups with Tasks 6-8)
  - Message: `feat(copier): template pyproject.toml`
  - Files: template/pyproject.toml.jinja

- [x] 6. Template src/{{project_name_snake}}/ Directory

  **What to do**:
  - Rename `template/src/ai_research_template/` to `template/src/{{project_name_snake}}/`
  - Inside `__init__.py.jinja`:
    - Replace docstring "Agent Engineering Template" → `{{ project_display_name }}`
    - Keep `__version__ = "0.1.0"`
  - Ensure all files in directory use `.jinja` suffix

  **Must NOT do**:
  - Delete any source files
  - Change the module logic
  - Forget to rename the directory itself

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Directory rename and text replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 7-9)
  - **Blocks**: Task 14
  - **Blocked By**: Task 2

  **References**:
  - Current: `src/ai_research_template/__init__.py` line 1-2
  - Copier templating: https://copier.readthedocs.io/en/stable/creating/

  **Acceptance Criteria**:
  - [ ] Directory renamed to `template/src/{{project_name_snake}}/`
  - [ ] `__init__.py` renamed to `__init__.py.jinja`
  - [ ] Contains `{{ project_display_name }}` in docstring

  **QA Scenarios**:
  ```
  Scenario: Directory name is templated
    Tool: Bash
    Steps:
      1. ls -d "template/src/{{project_name_snake}}"
    Expected Result: Directory exists with templated name
    Evidence: .sisyphus/evidence/task-6-dir.txt

  Scenario: No old directory name
    Tool: Bash
    Steps:
      1. ls -d template/src/ai_research_template 2>&1 || echo "correctly removed"
    Expected Result: "correctly removed" (directory doesn't exist)
    Evidence: .sisyphus/evidence/task-6-no-old-dir.txt
  ```

  **Commit**: NO (groups with Tasks 5, 7-8)
  - Message: `feat(copier): template source directory`
  - Files: template/src/{{project_name_snake}}/

- [x] 7. Template tests/test_hello.py

  **What to do**:
  - Rename `template/tests/test_hello.py` to `template/tests/test_hello.py.jinja`
  - Replace import:
    - `from ai_research_template.hello import greet` → `from {{ project_name_snake }}.hello import greet`

  **Must NOT do**:
  - Change test logic
  - Remove test cases

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single line replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5-6, 8-9)
  - **Blocks**: Task 14
  - **Blocked By**: Task 2

  **References**:
  - Current: `tests/test_hello.py` line 1

  **Acceptance Criteria**:
  - [ ] File renamed to `test_hello.py.jinja`
  - [ ] Contains `{{ project_name_snake }}` in import

  **QA Scenarios**:
  ```
  Scenario: Import is templated
    Tool: Bash
    Steps:
      1. grep "project_name_snake" template/tests/test_hello.py.jinja
    Expected Result: Placeholder found in import
    Evidence: .sisyphus/evidence/task-7-import.txt
  ```

  **Commit**: NO (groups with Tasks 5-6, 8)
  - Message: `feat(copier): template test files`
  - Files: template/tests/test_hello.py.jinja

- [x] 8. Template LICENSE File

  **What to do**:
  - Rename `template/LICENSE` to `template/LICENSE.jinja`
  - Replace hardcoded values:
    - `2026 XUDONG ZHU` → `{{ copyright_year }} {{ author_name }}`
  - Keep license text unchanged

  **Must NOT do**:
  - Change license type
  - Remove copyright notice

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single line replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5-7, 9)
  - **Blocks**: Task 14
  - **Blocked By**: Task 2

  **References**:
  - Current: `LICENSE` line 3

  **Acceptance Criteria**:
  - [ ] File renamed to `LICENSE.jinja`
  - [ ] Contains `{{ copyright_year }}` and `{{ author_name }}`

  **QA Scenarios**:
  ```
  Scenario: License placeholders
    Tool: Bash
    Steps:
      1. grep -E "copyright_year|author_name" template/LICENSE.jinja
    Expected Result: Both placeholders found
    Evidence: .sisyphus/evidence/task-8-license.txt

  Scenario: No hardcoded author
    Tool: Bash
    Steps:
      1. grep "XUDONG ZHU" template/LICENSE.jinja || echo "clean"
    Expected Result: "clean"
    Evidence: .sisyphus/evidence/task-8-no-hardcoded.txt
  ```

  **Commit**: YES (groups with Tasks 5-7)
  - Message: `feat(copier): template all core project files`
  - Files: template/pyproject.toml.jinja, template/src/, template/tests/, template/LICENSE.jinja

- [x] 9. Configure _exclude in copier.yml

  **What to do**:
  - Add `_exclude` list to `copier.yml`:
    - Exclude template-specific files from generated projects
    - Items to exclude:
      - `TEMPLATE.md` (unless `include_template_docs` is true)
      - `.sisyphus/drafts/`
      - `.sisyphus/plans/`
      - `.sisyphus/notepads/`
      - `.sisyphus/boulder.json`
      - `copier.yml` (always excluded by Copier)
      - `*.pyc`, `__pycache__`, `.git`, `.DS_Store`
  - Use conditional exclusion for TEMPLATE.md

  **Must NOT do**:
  - Exclude necessary template files
  - Break YAML syntax

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Adding list to existing config
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5-8)
  - **Blocks**: None
  - **Blocked By**: Task 3

  **References**:
  - Copier exclude: https://copier.readthedocs.io/en/stable/configuring/#exclude

  **Acceptance Criteria**:
  - [ ] `_exclude` key exists in copier.yml
  - [ ] Contains entries for `.sisyphus/drafts/`, `.sisyphus/plans/`, etc.

  **QA Scenarios**:
  ```
  Scenario: Exclude list present
    Tool: Bash
    Steps:
      1. grep "_exclude" copier.yml
      2. grep ".sisyphus" copier.yml
    Expected Result: Both found
    Evidence: .sisyphus/evidence/task-9-exclude.txt
  ```

  **Commit**: NO (groups with documentation tasks)
  - Message: `feat(copier): configure file exclusions`
  - Files: copier.yml

- [x] 10. Template README.md

  **What to do**:
  - Rename `template/README.md` to `template/README.md.jinja`
  - Replace all occurrences:
    - `# AI Research Template` → `# {{ project_display_name }}`
    - `ai_research_template` → `{{ project_name_snake }}`
    - `src/ai_research_template/` → `src/{{ project_name_snake }}/`
  - Replace manual rename instructions with Copier usage:
    - Change "Quick Start" section to mention `copier copy`
    - Remove `find` + `sed` commands
    - Add Copier usage instructions

  **Must NOT do**:
  - Remove the file structure diagram
  - Change the Research Workflow section
  - Break Markdown formatting

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text replacement and section rewrite
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 11-13)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - Current: `README.md` lines 1, 22-24, 77, 93-97

  **Acceptance Criteria**:
  - [ ] File renamed to `README.md.jinja`
  - [ ] Contains `{{ project_display_name }}` in title
  - [ ] No `ai_research_template` references remain
  - [ ] Contains `copier copy` instructions

  **QA Scenarios**:
  ```
  Scenario: README placeholders
    Tool: Bash
    Steps:
      1. grep "project_display_name" template/README.md.jinja
      2. grep "copier copy" template/README.md.jinja
    Expected Result: Both found
    Evidence: .sisyphus/evidence/task-10-readme.txt

  Scenario: No old references
    Tool: Bash
    Steps:
      1. grep -i "ai.research.template" template/README.md.jinja || echo "clean"
    Expected Result: "clean"
    Evidence: .sisyphus/evidence/task-10-no-old.txt
  ```

  **Commit**: NO (groups with Tasks 11-13)
  - Message: `feat(copier): template README.md`
  - Files: template/README.md.jinja

- [x] 11. Template ARCHITECTURE.md

  **What to do**:
  - Rename `template/ARCHITECTURE.md` to `template/ARCHITECTURE.md.jinja`
  - Replace directory reference:
    - `src/ai_research_template/` → `src/{{ project_name_snake }}/`

  **Must NOT do**:
  - Change the architecture template structure
  - Remove sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single reference replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10, 12-13)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - Current: `ARCHITECTURE.md` line 30

  **Acceptance Criteria**:
  - [ ] File renamed to `ARCHITECTURE.md.jinja`
  - [ ] Contains `{{ project_name_snake }}` for directory

  **QA Scenarios**:
  ```
  Scenario: Architecture placeholder
    Tool: Bash
    Steps:
      1. grep "project_name_snake" template/ARCHITECTURE.md.jinja
    Expected Result: Placeholder found
    Evidence: .sisyphus/evidence/task-11-arch.txt
  ```

  **Commit**: NO (groups with Tasks 10, 12-13)
  - Message: `feat(copier): template ARCHITECTURE.md`
  - Files: template/ARCHITECTURE.md.jinja

- [x] 12. Template SPEC.md

  **What to do**:
  - Rename `template/SPEC.md` to `template/SPEC.md.jinja`
  - Replace directory reference:
    - `src/ai_research_template/` → `src/{{ project_name_snake }}/`

  **Must NOT do**:
  - Change the spec template structure
  - Remove sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single reference replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10-11, 13)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - Current: `SPEC.md` line 19

  **Acceptance Criteria**:
  - [ ] File renamed to `SPEC.md.jinja`
  - [ ] Contains `{{ project_name_snake }}` for directory

  **QA Scenarios**:
  ```
  Scenario: SPEC placeholder
    Tool: Bash
    Steps:
      1. grep "project_name_snake" template/SPEC.md.jinja
    Expected Result: Placeholder found
    Evidence: .sisyphus/evidence/task-12-spec.txt
  ```

  **Commit**: NO (groups with Tasks 10-11, 13)
  - Message: `feat(copier): template SPEC.md`
  - Files: template/SPEC.md.jinja

- [x] 13. Template AGENTS.md

  **What to do**:
  - Rename `template/AGENTS.md` to `template/AGENTS.md.jinja`
  - Replace mypy packages reference:
    - Line 35: `packages = ["ai_research_template"]` → `packages = ["{{ project_name_snake }}"]`

  **Must NOT do**:
  - Change any other AGENTS.md content
  - Modify the pipeline workflow section

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single reference replacement
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10-12, 14)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - Current: `AGENTS.md` line 35

  **Acceptance Criteria**:
  - [ ] File renamed to `AGENTS.md.jinja`
  - [ ] Contains `{{ project_name_snake }}` for mypy packages

  **QA Scenarios**:
  ```
  Scenario: AGENTS placeholder
    Tool: Bash
    Steps:
      1. grep "project_name_snake" template/AGENTS.md.jinja
    Expected Result: Placeholder found in mypy config
    Evidence: .sisyphus/evidence/task-13-agents.txt
  ```

  **Commit**: NO (groups with Tasks 10-12, 14)
  - Message: `feat(copier): template AGENTS.md`
  - Files: template/AGENTS.md.jinja

- [x] 14. Update Root README for Copier Usage

  **What to do**:
  - Create/update root `README.md` (not in template/) to document:
    - This is a Copier template repository
    - How to use: `copier copy <this-repo-url> <destination>`
    - Available prompts and their descriptions
    - Example usage with all options
    - Link to Copier documentation
  - Remove or update TEMPLATE.md content
  - Add `--trust` flag documentation for `_tasks`

  **Must NOT do**:
  - Remove the template/
  - Add this to template/README.md.jinja

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation writing
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10-12)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - Copier docs: https://copier.readthedocs.io/
  - Example template repos

  **Acceptance Criteria**:
  - [ ] Root README.md explains Copier usage
  - [ ] Contains `copier copy` example command
  - [ ] Documents all available prompts

  **QA Scenarios**:
  ```
  Scenario: Root README has Copier instructions
    Tool: Bash
    Steps:
      1. grep "copier copy" README.md
      2. grep "prompts" README.md
    Expected Result: Both found
    Evidence: .sisyphus/evidence/task-13-root-readme.txt
  ```

  **Commit**: YES (groups with Tasks 9-12)
  - Message: `feat(copier): update documentation for Copier usage`
  - Files: README.md, template/README.md.jinja, template/ARCHITECTURE.md.jinja, template/SPEC.md.jinja, template/AGENTS.md.jinja, copier.yml

- [x] 15. Add pytest-copie Dependency

  **What to do**:
  - Add `pytest-copie` to dev dependencies in `pyproject.toml` (NOT template/):
    ```bash
    uv add --dev pytest-copie
    ```
  - Create `tests/conftest.py` if needed for pytest-copie configuration
  - Verify pytest still runs correctly

  **Must NOT do**:
  - Add to template/pyproject.toml.jinja (this is for testing the template repo itself)
  - Modify existing test configuration

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single dependency addition
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Task 16, starts after Wave 3)
  - **Blocks**: Task 16
  - **Blocked By**: Tasks 5-8 (need templated files to test)

  **References**:
  - pytest-copie: https://pypi.org/project/pytest-copie/

  **Acceptance Criteria**:
  - [ ] `pytest-copie` in dev dependencies
  - [ ] `uv sync` succeeds
  - [ ] `uv run pytest` still passes

  **QA Scenarios**:
  ```
  Scenario: Dependency installed
    Tool: Bash
    Steps:
      1. grep "pytest-copie" pyproject.toml
      2. uv sync
    Expected Result: Dependency found, sync succeeds
    Evidence: .sisyphus/evidence/task-15-dep.txt
  ```

  **Commit**: NO (groups with Task 16)
  - Message: `test(copier): add pytest-copie for template testing`
  - Files: pyproject.toml, uv.lock

- [x] 16. Create Template Test

  **What to do**:
  - Create `tests/test_template.py`
  - Test cases:
    - Template generates successfully
    - All placeholders are replaced
    - Generated project has correct structure
    - Generated project passes basic validation (uv sync works)
  - Use pytest-copie fixture for template testing:
    ```python
    def test_copier_generates_project(copie):
        result = copie.copy(extra_answers={
            "project_name": "test_project",
            "project_description": "A test project",
            "author_name": "Test Author",
            "author_email": "test@example.com"
        })
        assert result.exit_code == 0
        assert result.project_dir.joinpath("pyproject.toml").exists()
    ```

  **Must NOT do**:
  - Add slow tests (template generation takes time)
  - Test in template/ directory

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Test file creation with standard patterns
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Task 15)
  - **Blocks**: Task 17
  - **Blocked By**: Task 15

  **References**:
  - pytest-copie docs: https://github.com/13giesler/pytest-copie

  **Acceptance Criteria**:
  - [ ] `tests/test_template.py` exists
  - [ ] Contains test for successful generation
  - [ ] Contains test for placeholder replacement
  - [ ] `uv run pytest tests/test_template.py` passes

  **QA Scenarios**:
  ```
  Scenario: Test file exists and runs
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_template.py -v
    Expected Result: All tests pass
    Evidence: .sisyphus/evidence/task-16-test-run.txt
  ```

  **Commit**: YES (groups with Task 15)
  - Message: `test(copier): add template generation tests`
  - Files: tests/test_template.py, pyproject.toml

- [x] 17. Test Template Generation End-to-End

  **What to do**:
  - Run full template generation test:
    ```bash
    copier copy . /tmp/test-project --trust --data project_name=my_awesome_project --data project_description="My awesome project" --data author_name="Test Author" --data author_email="test@example.com"
    ```
  - Verify generated project:
    - Directory structure is correct
    - All placeholders replaced
    - `uv sync` succeeds
    - `uv run ruff check src/ tests/` passes
    - `uv run mypy src/` passes
    - `uv run pytest` passes
    - No `ai_research_template` references remain (except in .copier-answers.yml)

  **Must NOT do**:
  - Skip validation steps
  - Leave test project in /tmp (clean up)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: End-to-end validation requires careful verification
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (final task before verification)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 16

  **References**:
  - Success criteria in this plan

  **Acceptance Criteria**:
  - [ ] `copier copy` succeeds without errors
  - [ ] Generated project has `src/my_awesome_project/` directory
  - [ ] `uv sync` in generated project succeeds
  - [ ] All quality checks pass in generated project
  - [ ] No `ai_research_template` references in generated files

  **QA Scenarios**:
  ```
  Scenario: Full template generation
    Tool: Bash
    Steps:
      1. copier copy . /tmp/test-project --trust --data project_name=my_awesome_project ...
      2. cd /tmp/test-project && uv sync
      3. cd /tmp/test-project && uv run ruff check src/ tests/
      4. cd /tmp/test-project && uv run mypy src/
      5. cd /tmp/test-project && uv run pytest
      6. grep -r "ai_research_template" /tmp/test-project --include="*.py" --include="*.toml" || echo "clean"
      7. rm -rf /tmp/test-project
    Expected Result: All steps succeed, no old references found
    Evidence: .sisyphus/evidence/task-17-e2e.txt
  ```

  **Commit**: YES
  - Message: `test(copier): verify end-to-end template generation`
  - Files: None (verification only)

---

## Final Verification Wave (MANDATORY)

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. Verify all "Must Have" items exist. Check evidence files. Compare deliverables against plan.
  Output: `Must Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `uv sync`, `ruff check`, `mypy`, `pytest`. Check for AI slop patterns.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high`
  Run `copier copy . /tmp/test-project` with test inputs. Verify all placeholders replaced. Run validation commands on generated project.
  Output: `Generation [PASS/FAIL] | Placeholders [N/N replaced] | Validation [PASS/FAIL] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  Verify 1:1 mapping between spec and implementation. Check "Must NOT do" compliance.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | VERDICT`

---

## Commit Strategy

- **Commit 1**: `feat(copier): add copier.yml and template structure` — copier.yml, template/, answers file
- **Commit 2**: `feat(copier): template all project files` — pyproject.toml, src/, tests/, LICENSE
- **Commit 3**: `feat(copier): update documentation for Copier usage` — README.md, ARCHITECTURE.md, SPEC.md
- **Commit 4**: `test(copier): add pytest-copie template tests` — tests/test_template.py, pyproject.toml

Pre-commit: `uv run pytest`

---

## Success Criteria

### Verification Commands
```bash
# Template generation test
copier copy . /tmp/test-project --data project_name=test_project --data project_description="Test" --data author_name="Test Author" --data author_email="test@example.com"
cd /tmp/test-project
uv sync                    # Expected: success
uv run ruff check src/ tests/  # Expected: 0 violations
uv run mypy src/            # Expected: success
uv run pytest              # Expected: all pass
grep -r "ai_research_template" .  # Expected: no matches (except copier-answers.yml)
```

### Final Checklist
- [x] All "Must Have" present
- [x] All "Must NOT Have" absent
- [x] All tests pass
- [x] `copier copy` works correctly
- [x] Generated project is valid Python package
