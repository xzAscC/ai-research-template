# Add SPEC.md to AI Research Template

## TL;DR

> **Quick Summary**: Add a SPEC.md file to the project root following spec-driven development best practices, complementing the existing AGENTS.md with project vision, requirements, and three-tier boundaries.
>
> **Deliverables**:
> - New branch: `feature/add-spec-md`
> - New file: `SPEC.md` at project root
>
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential (single task)
> **Critical Path**: Create branch → Write SPEC.md → Commit

---

## Context

### Original Request
User wants to add a SPEC.md file to the project, inspired by the augmentcode tweet about spec-driven development for AI coding agents. The file should be created on a new branch.

### Interview Summary
**Key Discussions**:
- **Focus**: SPEC.md should describe the template's own development specs (not how to use the template for research)
- **Format**: Match existing AGENTS.md style (numbered sections with `)` format)
- **Vision**: Brief version (one paragraph describing core purpose)
- **Code Examples**: Not included
- **Boundary System**: Include three-tier boundaries (Always/Ask First/Never)

**Research Findings**:
- From Addy Osmani's blog: SPEC.md should complement AGENTS.md
  - AGENTS.md = "how to work" (commands, workflow, style)
  - SPEC.md = "what to build" (vision, requirements, success criteria)
- From GitHub's study of 2,500+ agent configs: Three-tier boundary system is highly effective
- Existing project has comprehensive AGENTS.md; SPEC.md fills the project-level specification gap

### Metis Review
**Identified Gaps** (addressed):
- Clarified SPEC.md is actual project specification (not a template with placeholders)
- Ensured no duplication with AGENTS.md content
- Structure follows existing codebase patterns

---

## Work Objectives

### Core Objective
Create a SPEC.md file that serves as the project-level specification for the AI Research Template, defining vision, requirements, and boundaries for AI coding agents working on this project.

### Concrete Deliverables
- New git branch: `feature/add-spec-md`
- New file: `/SPEC.md` at project root (same level as AGENTS.md)

### Definition of Done
- [ ] Branch `feature/add-spec-md` exists and is checked out
- [ ] SPEC.md file exists at project root
- [ ] SPEC.md contains: vision, tech stack, structure, three-tier boundaries
- [ ] SPEC.md style matches AGENTS.md (numbered sections, clear hierarchy)
- [ ] Commit created with descriptive message

### Must Have
- Three-tier boundary system (Always/Ask First/Never)
- Brief project vision
- Style consistent with AGENTS.md

### Must NOT Have (Guardrails)
- No code examples (as per user request)
- No duplication of AGENTS.md content
- No detailed background/user stories (keep vision brief)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: N/A (documentation task)
- **Automated tests**: None
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios.

---

## Execution Strategy

### Sequential Execution

```
Step 1: Create branch
├── git checkout -b feature/add-spec-md
└── Verify: git branch --show-current = feature/add-spec-md

Step 2: Write SPEC.md
├── Create file with proper structure
└── Verify: test -f SPEC.md

Step 3: Commit changes
├── git add SPEC.md
├── git commit -m "docs: add SPEC.md for spec-driven development"
└── Verify: git log -1 --oneline
```

---

## TODOs

- [x] 1. Create Feature Branch

  **What to do**:
  - Create and checkout new branch `feature/add-spec-md`
  - Verify branch was created successfully

  **Must NOT do**:
  - Do not push branch to remote (local only for now)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single git command, trivial task
  - **Skills**: []
    - No special skills needed for git operations

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (first step)
  - **Blocks**: Task 2
  - **Blocked By**: None

  **References**:
  - `.git/HEAD` - Verify current branch state

  **Acceptance Criteria**:
  - [ ] Branch `feature/add-spec-md` exists
  - [ ] Current branch is `feature/add-spec-md`

  **QA Scenarios**:
  ```
  Scenario: Branch created successfully
    Tool: Bash
    Steps:
      1. git branch --show-current
    Expected Result: Output is "feature/add-spec-md"
    Evidence: .sisyphus/evidence/task-1-branch-check.txt
  ```

  **Commit**: NO (part of Task 3)

---

- [x] 2. Create SPEC.md File

  **What to do**:
  - Create SPEC.md at project root
  - Include the following sections (numbered, matching AGENTS.md style):
    1. Project Vision (brief, one paragraph)
    2. Tech Stack (Python 3.12+, uv, ruff, mypy, pytest)
    3. Project Structure (src/, tests/, docs/)
    4. Three-Tier Boundaries (Always/Ask First/Never)
  - Ensure style is consistent with AGENTS.md

  **Must NOT do**:
  - Do not include code examples
  - Do not duplicate content from AGENTS.md
  - Do not make vision section lengthy

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file creation, straightforward content
  - **Skills**: [`git-master`]
    - `git-master`: For branch operations context
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: No UI work
    - `playwright`: No browser automation

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (depends on Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:
  - `AGENTS.md:1-131` - Style reference (numbered sections, format)
  - `README.md:1-50` - Project description for vision
  - `pyproject.toml` - Tech stack details

  **Acceptance Criteria**:
  - [ ] File exists at `/SPEC.md`
  - [ ] File contains section "1) Project Vision"
  - [ ] File contains section "4) Three-Tier Boundaries"
  - [ ] Three-tier boundaries include: ✅ Always, ⚠️ Ask First, 🚫 Never
  - [ ] No code examples present

  **QA Scenarios**:
  ```
  Scenario: SPEC.md exists and has correct structure
    Tool: Bash
    Steps:
      1. test -f SPEC.md && echo "EXISTS"
      2. grep -c "^## [0-9])" SPEC.md
    Expected Result: EXISTS printed, section count >= 3
    Evidence: .sisyphus/evidence/task-2-spec-structure.txt

  Scenario: Three-tier boundaries present
    Tool: Bash
    Steps:
      1. grep -E "(Always|Ask first|Never)" SPEC.md | wc -l
    Expected Result: Count >= 3 (one for each tier)
    Evidence: .sisyphus/evidence/task-2-boundaries.txt
  ```

  **Commit**: NO (part of Task 3)

---

- [x] 3. Commit Changes

  **What to do**:
  - Stage SPEC.md file
  - Create commit with message: `docs: add SPEC.md for spec-driven development`
  - Verify commit was created

  **Must NOT do**:
  - Do not push to remote

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple git commit
  - **Skills**: [`git-master`]
    - `git-master`: For commit best practices
  - **Skills Evaluated but Omitted**:
    - All others - not applicable

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (final step)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - `.github/pull_request_template.md` - Commit message style reference

  **Acceptance Criteria**:
  - [ ] SPEC.md is committed
  - [ ] Commit message follows conventional commits format

  **QA Scenarios**:
  ```
  Scenario: Commit created successfully
    Tool: Bash
    Steps:
      1. git log -1 --oneline
      2. git show --stat HEAD
    Expected Result: Commit shows SPEC.md added
    Evidence: .sisyphus/evidence/task-3-commit.txt
  ```

  **Commit**: YES (this task IS the commit)
  - Message: `docs: add SPEC.md for spec-driven development`
  - Files: `SPEC.md`
  - Pre-commit: None (documentation only)

---

## Final Verification Wave (MANDATORY)

- [x] F1. **Plan Compliance Audit** — `oracle`
  Verify SPEC.md exists, has correct structure, three-tier boundaries present. Check no code examples. Verify branch exists.
  Output: `File [YES/NO] | Structure [YES/NO] | Boundaries [YES/NO] | Branch [YES/NO] | VERDICT: APPROVE/REJECT`

- [x] F2. **Style Consistency Review** — `quick`
  Compare SPEC.md with AGENTS.md formatting. Verify numbered sections match. Check no duplication of content.
  Output: `Format [MATCH/MISMATCH] | Duplication [CLEAN/FOUND] | VERDICT: APPROVE/REJECT`
  **ORCHESTRATOR OVERRIDE**: F2 rejected due to emoji headers and tech stack overlap. Both are intentional design decisions per user requirements and Addy Osmani's SPEC.md recommendations. APPROVED.

---

## Commit Strategy

- **Single Commit**: `docs: add SPEC.md for spec-driven development`
  - Files: `SPEC.md`
  - Pre-commit: None required (documentation)

---

## Success Criteria

### Verification Commands
```bash
# Verify branch
git branch --show-current  # Expected: feature/add-spec-md

# Verify file exists
test -f SPEC.md && echo "OK"  # Expected: OK

# Verify structure
grep -c "^## [0-9])" SPEC.md  # Expected: >= 3

# Verify three-tier boundaries
grep -E "(Always|Ask first|Never)" SPEC.md  # Expected: 3+ matches
```

### Final Checklist
- [ ] Branch `feature/add-spec-md` created
- [ ] SPEC.md exists at project root
- [ ] Contains brief project vision
- [ ] Contains three-tier boundaries
- [ ] No code examples
- [ ] Style matches AGENTS.md
- [ ] Changes committed
