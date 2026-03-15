# Consolidate Plans to .sisyphus/

## TL;DR

> **Quick Summary**: Consolidate all plan-related files into `.sisyphus/` directory. Remove the dual system (docs/exec-plans/ + .sisyphus/plans/) and establish a single source of truth.
>
> **Deliverables**:
> - New file: `.sisyphus/roadmap.md` (migrated from docs/PLANS.md)
> - Moved file: `.sisyphus/tech-debt-tracker.md` (from docs/exec-plans/)
> - Updated references in 6 files
> - Deleted: `PLAN.md`, `docs/exec-plans/`, `docs/PLANS.md`
>
> **Estimated Effort**: Quick
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Create files → Update references → Delete old → Verify

---

## Context

### Original Request
User wants to consolidate all plans into `.sisyphus/` directory instead of having two systems (docs/exec-plans/ and .sisyphus/plans/). The goal is a single source of truth for plan management.

### Interview Summary
**Key Discussions**:
- **docs/exec-plans/**: Delete entirely (including completed/)
- **PLAN.md (root)**: Delete (redundant)
- **docs/PLANS.md**: Merge into `.sisyphus/roadmap.md`
- **tech-debt-tracker.md**: Move to `.sisyphus/tech-debt-tracker.md`
- **Structure**: Flat structure in `.sisyphus/plans/` (no subdirectories)

**Research Findings**:
- `.sisyphus/plans/` already exists with active plans
- `boulder.json` points to `.sisyphus/plans/` (leave unchanged)
- Multiple files reference old paths and need updates

### Metis Review
**Identified Gaps** (addressed):
- **TEMPLATE.md line 72** was missed → Added to update list
- **tech-debt-tracker.md self-references** (lines 34, 37) → Update when moving
- **Pipeline workflow text in AGENTS.md** → Update to new workflow
- **Use git mv** → Preserve history when moving files

---

## Work Objectives

### Core Objective
Consolidate all plan-related files into `.sisyphus/` to create a single source of truth, eliminating the confusing dual-system of docs/exec-plans/ and .sisyphus/plans/.

### Concrete Deliverables
- `.sisyphus/roadmap.md` - Migrated project roadmap
- `.sisyphus/tech-debt-tracker.md` - Moved tech debt tracker
- Updated references in: AGENTS.md, ARCHITECTURE.md, SPEC.md, README.md, TEMPLATE.md
- Deleted: PLAN.md, docs/exec-plans/, docs/PLANS.md

### Definition of Done
- [ ] All old path references replaced with new paths
- [ ] New files created in .sisyphus/
- [ ] Old files deleted
- [ ] grep returns 0 matches for old paths

### Must Have
- All references updated (no broken links)
- Content preserved during migration
- git mv used to preserve history

### Must NOT Have (Guardrails)
- No subdirectories in .sisyphus/plans/ (keep flat)
- No changes to .sisyphus/boulder.json
- No changes to docs/QUALITY_SCORE.md or docs/design-docs/
- No content improvements (preserve verbatim)

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: N/A (documentation/file moves)
- **Automated tests**: None
- **Framework**: N/A

### QA Policy
Every task includes agent-executed QA scenarios using grep and file checks.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Create new files):
├── Task 1: Create .sisyphus/roadmap.md [quick]
└── Task 2: Move tech-debt-tracker.md to .sisyphus/ [quick]

Wave 2 (Update references - MAX PARALLEL):
├── Task 3: Update AGENTS.md references [quick]
├── Task 4: Update ARCHITECTURE.md references [quick]
├── Task 5: Update SPEC.md references [quick]
├── Task 6: Update README.md references [quick]
└── Task 7: Update TEMPLATE.md references [quick]

Wave 3 (Delete old files):
├── Task 8: Delete PLAN.md [quick]
├── Task 9: Delete docs/exec-plans/ directory [quick]
└── Task 10: Delete docs/PLANS.md [quick]

Wave 4 (Final verification):
└── Task 11: Verify all references updated [quick]

Critical Path: Task 1,2 → Task 3-7 → Task 8-10 → Task 11
Parallel Speedup: ~60% faster than sequential
Max Concurrent: 5 (Wave 2)
```

### Dependency Matrix

- **1-2**: — — 3-7
- **3-7**: 1-2 — 8-10
- **8-10**: 3-7 — 11
- **11**: 8-10 — —

### Agent Dispatch Summary

- **1-2**: quick × 2
- **3-7**: quick × 5
- **8-10**: quick × 3
- **11**: quick × 1

---

## TODOs

- [x] 1. Create .sisyphus/roadmap.md

  **What to do**:
  - Use `git mv docs/PLANS.md .sisyphus/roadmap.md` to preserve history
  - Verify file was moved successfully

  **Must NOT do**:
  - Do not modify content (preserve verbatim)
  - Do not use cp + rm (loses history)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single git mv command
  - **Skills**: [`git-master`]
    - `git-master`: For git mv best practices

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 3-7
  - **Blocked By**: None

  **References**:
  - `docs/PLANS.md` - Source file to move
  - `.sisyphus/` - Target directory

  **Acceptance Criteria**:
  - [ ] File exists at `.sisyphus/roadmap.md`
  - [ ] File does NOT exist at `docs/PLANS.md`
  - [ ] git log shows rename (not delete+add)

  **QA Scenarios**:
  ```
  Scenario: roadmap.md exists in .sisyphus/
    Tool: Bash
    Steps:
      1. test -f .sisyphus/roadmap.md && echo "EXISTS"
    Expected Result: "EXISTS"
    Evidence: .sisyphus/evidence/task-1-roadmap-exists.txt

  Scenario: Original file no longer exists
    Tool: Bash
    Steps:
      1. test ! -f docs/PLANS.md && echo "DELETED"
    Expected Result: "DELETED"
    Evidence: .sisyphus/evidence/task-1-old-deleted.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 2. Move tech-debt-tracker.md to .sisyphus/

  **What to do**:
  - Use `git mv docs/exec-plans/tech-debt-tracker.md .sisyphus/tech-debt-tracker.md`
  - Update self-referential paths inside the file (lines 34, 37):
    - `docs/exec-plans/active/` → `.sisyphus/plans/`
    - `docs/exec-plans/completed/` → `.sisyphus/plans/` (completed plans stay in same dir with status markers)
  - Also update line 18: "Link to execution plan in `docs/exec-plans/`" → "Link to work plan in `.sisyphus/plans/`"

  **Must NOT do**:
  - Do not modify other content
  - Do not add subdirectories to .sisyphus/plans/

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file move with minor edits
  - **Skills**: [`git-master`]
    - `git-master`: For git mv best practices

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 3-7
  - **Blocked By**: None

  **References**:
  - `docs/exec-plans/tech-debt-tracker.md:34,37` - Self-references to update
  - `docs/exec-plans/tech-debt-tracker.md:18` - Link instruction to update

  **Acceptance Criteria**:
  - [ ] File exists at `.sisyphus/tech-debt-tracker.md`
  - [ ] Self-references updated to `.sisyphus/plans/`
  - [ ] No references to `docs/exec-plans/` in the file

  **QA Scenarios**:
  ```
  Scenario: tech-debt-tracker.md moved successfully
    Tool: Bash
    Steps:
      1. test -f .sisyphus/tech-debt-tracker.md && echo "EXISTS"
    Expected Result: "EXISTS"
    Evidence: .sisyphus/evidence/task-2-tracker-exists.txt

  Scenario: Self-references updated
    Tool: Bash
    Steps:
      1. grep -c "docs/exec-plans" .sisyphus/tech-debt-tracker.md
    Expected Result: 0 (no matches)
    Evidence: .sisyphus/evidence/task-2-no-old-refs.txt

  Scenario: New references present
    Tool: Bash
    Steps:
      1. grep -c ".sisyphus/plans" .sisyphus/tech-debt-tracker.md
    Expected Result: >= 2 (at least 2 new references)
    Evidence: .sisyphus/evidence/task-2-new-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 3. Update AGENTS.md References

  **What to do**:
  - Line 98: Change "Read PLAN.md" → "Read .sisyphus/plans/ (active work plan)"
  - Line 101: Change "Complete → docs/exec-plans/completed/, In-progress → active/" → "Complete → mark as completed in .sisyphus/plans/, In-progress → .sisyphus/plans/"
  - Line 102: Change "PLANS.md, QUALITY_SCORE.md, ARCHITECTURE.md" → "roadmap.md, QUALITY_SCORE.md, ARCHITECTURE.md"
  - Line 129: Change "Exec plans: `docs/exec-plans/`" → "Work plans: `.sisyphus/plans/`"
  - Line 131: Change "Roadmap: `docs/PLANS.md`" → "Roadmap: `.sisyphus/roadmap.md`"

  **Must NOT do**:
  - Do not change other sections
  - Do not restructure the file

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text replacements only
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4-7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8-10
  - **Blocked By**: Tasks 1-2

  **References**:
  - `AGENTS.md:98-104` - Pipeline workflow section
  - `AGENTS.md:125-131` - Architecture cross-references section

  **Acceptance Criteria**:
  - [ ] No references to `PLAN.md` (root)
  - [ ] No references to `docs/exec-plans/`
  - [ ] No references to `docs/PLANS.md`
  - [ ] New references to `.sisyphus/plans/` and `.sisyphus/roadmap.md`

  **QA Scenarios**:
  ```
  Scenario: No old references in AGENTS.md
    Tool: Bash
    Steps:
      1. grep -E "(docs/exec-plans|docs/PLANS\.md|^PLAN\.md)" AGENTS.md | wc -l
    Expected Result: 0
    Evidence: .sisyphus/evidence/task-3-no-old-refs.txt

  Scenario: New references present
    Tool: Bash
    Steps:
      1. grep -c ".sisyphus/plans" AGENTS.md
      2. grep -c ".sisyphus/roadmap" AGENTS.md
    Expected Result: plans >= 2, roadmap >= 1
    Evidence: .sisyphus/evidence/task-3-new-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 4. Update ARCHITECTURE.md References

  **What to do**:
  - Line 37: Change `docs/exec-plans/     # Execution plans` → `.sisyphus/plans/      # Work plans`

  **Must NOT do**:
  - Do not change other sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single line replacement
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 3, 5-7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8-10
  - **Blocked By**: Tasks 1-2

  **References**:
  - `ARCHITECTURE.md:35-39` - Directory structure section

  **Acceptance Criteria**:
  - [ ] No references to `docs/exec-plans/`
  - [ ] Reference to `.sisyphus/plans/` present

  **QA Scenarios**:
  ```
  Scenario: No old references in ARCHITECTURE.md
    Tool: Bash
    Steps:
      1. grep -c "docs/exec-plans" ARCHITECTURE.md
    Expected Result: 0
    Evidence: .sisyphus/evidence/task-4-no-old-refs.txt

  Scenario: New reference present
    Tool: Bash
    Steps:
      1. grep -c ".sisyphus/plans" ARCHITECTURE.md
    Expected Result: >= 1
    Evidence: .sisyphus/evidence/task-4-new-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 5. Update SPEC.md References

  **What to do**:
  - Line 23: Change `docs/exec-plans/` → `.sisyphus/plans/`
  - Line 24: Change `docs/PLANS.md` → `.sisyphus/roadmap.md`

  **Must NOT do**:
  - Do not change other content

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Two line replacements
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 3-4, 6-7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8-10
  - **Blocked By**: Tasks 1-2

  **References**:
  - `SPEC.md:21-26` - Project structure section

  **Acceptance Criteria**:
  - [ ] No references to `docs/exec-plans/`
  - [ ] No references to `docs/PLANS.md`
  - [ ] References to `.sisyphus/plans/` and `.sisyphus/roadmap.md` present

  **QA Scenarios**:
  ```
  Scenario: No old references in SPEC.md
    Tool: Bash
    Steps:
      1. grep -E "(docs/exec-plans|docs/PLANS\.md)" SPEC.md | wc -l
    Expected Result: 0
    Evidence: .sisyphus/evidence/task-5-no-old-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 6. Update README.md References

  **What to do**:
  - Find and replace all references to `docs/exec-plans/` → `.sisyphus/plans/`
  - Find and replace all references to `docs/PLANS.md` → `.sisyphus/roadmap.md`
  - Update file structure diagram if present

  **Must NOT do**:
  - Do not change other content

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text replacements
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 3-5, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8-10
  - **Blocked By**: Tasks 1-2

  **References**:
  - `README.md` - File structure section

  **Acceptance Criteria**:
  - [ ] No references to `docs/exec-plans/`
  - [ ] No references to `docs/PLANS.md`
  - [ ] New references to `.sisyphus/plans/` and `.sisyphus/roadmap.md`

  **QA Scenarios**:
  ```
  Scenario: No old references in README.md
    Tool: Bash
    Steps:
      1. grep -E "(docs/exec-plans|docs/PLANS\.md)" README.md | wc -l
    Expected Result: 0
    Evidence: .sisyphus/evidence/task-6-no-old-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [x] 7. Update TEMPLATE.md References

  **What to do**:
  - Line 72: Change `docs/PLANS.md` → `.sisyphus/roadmap.md`
  - Update the description if needed: "Your project roadmap" stays the same

  **Must NOT do**:
  - Do not change other content

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single line replacement
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 3-6)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 8-10
  - **Blocked By**: Tasks 1-2

  **References**:
  - `TEMPLATE.md:64-74` - Files to Update table

  **Acceptance Criteria**:
  - [ ] No references to `docs/PLANS.md`
  - [ ] Reference to `.sisyphus/roadmap.md` present

  **QA Scenarios**:
  ```
  Scenario: No old references in TEMPLATE.md
    Tool: Bash
    Steps:
      1. grep -c "docs/PLANS\.md" TEMPLATE.md
    Expected Result: 0
    Evidence: .sisyphus/evidence/task-7-no-old-refs.txt

  Scenario: New reference present
    Tool: Bash
    Steps:
      1. grep -c ".sisyphus/roadmap" TEMPLATE.md
    Expected Result: >= 1
    Evidence: .sisyphus/evidence/task-7-new-refs.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [ ] 8. Delete PLAN.md (root)

  **What to do**:
  - Use `git rm PLAN.md` to remove the file
  - Verify file is deleted

  **Must NOT do**:
  - Do not use rm (use git rm to track deletion)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single git rm command
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9-10)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 11
  - **Blocked By**: Tasks 3-7

  **References**:
  - `PLAN.md` - File to delete

  **Acceptance Criteria**:
  - [ ] File does NOT exist at root
  - [ ] git status shows deletion

  **QA Scenarios**:
  ```
  Scenario: PLAN.md deleted
    Tool: Bash
    Steps:
      1. test ! -f PLAN.md && echo "DELETED"
    Expected Result: "DELETED"
    Evidence: .sisyphus/evidence/task-8-plan-deleted.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [ ] 9. Delete docs/exec-plans/ Directory

  **What to do**:
  - Use `git rm -r docs/exec-plans/` to remove entire directory
  - This removes:
    - `docs/exec-plans/tech-debt-tracker.md` (already moved, but original still exists)
    - `docs/exec-plans/completed/pipeline-update.md`
    - Any .gitkeep files
    - The directory itself

  **Must NOT do**:
  - Do not delete docs/ directory itself
  - Do not delete docs/design-docs/ or docs/QUALITY_SCORE.md

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single git rm -r command
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 10)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 11
  - **Blocked By**: Tasks 3-7

  **References**:
  - `docs/exec-plans/` - Directory to delete

  **Acceptance Criteria**:
  - [ ] Directory does NOT exist
  - [ ] docs/design-docs/ still exists
  - [ ] docs/QUALITY_SCORE.md still exists

  **QA Scenarios**:
  ```
  Scenario: docs/exec-plans/ deleted
    Tool: Bash
    Steps:
      1. test ! -d docs/exec-plans && echo "DELETED"
    Expected Result: "DELETED"
    Evidence: .sisyphus/evidence/task-9-exec-plans-deleted.txt

  Scenario: Other docs preserved
    Tool: Bash
    Steps:
      1. test -d docs/design-docs && echo "EXISTS"
      2. test -f docs/QUALITY_SCORE.md && echo "EXISTS"
    Expected Result: Both print "EXISTS"
    Evidence: .sisyphus/evidence/task-9-other-docs-preserved.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [ ] 10. Delete docs/PLANS.md

  **What to do**:
  - This should already be moved (Task 1), but verify and clean up if somehow still exists
  - Use `git rm docs/PLANS.md` if file still exists
  - If already moved, skip this task

  **Must NOT do**:
  - Do not delete .sisyphus/roadmap.md

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Verification + cleanup
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8-9)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 11
  - **Blocked By**: Tasks 3-7

  **References**:
  - `docs/PLANS.md` - File to verify/delete

  **Acceptance Criteria**:
  - [ ] File does NOT exist at docs/PLANS.md
  - [ ] File EXISTS at .sisyphus/roadmap.md

  **QA Scenarios**:
  ```
  Scenario: docs/PLANS.md deleted
    Tool: Bash
    Steps:
      1. test ! -f docs/PLANS.md && echo "DELETED"
    Expected Result: "DELETED"
    Evidence: .sisyphus/evidence/task-10-plans-deleted.txt
  ```

  **Commit**: NO (commit after Wave 3)

---

- [ ] 11. Final Verification

  **What to do**:
  - Run grep to verify zero matches for old paths
  - Verify all new files exist
  - Verify all deleted files do not exist
  - Create final evidence report

  **Must NOT do**:
  - Do not make any file changes

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Verification commands only
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (final)
  - **Blocks**: None
  - **Blocked By**: Tasks 8-10

  **References**:
  - All modified files for verification

  **Acceptance Criteria**:
  - [ ] grep for `docs/exec-plans` returns 0 matches in all .md files
  - [ ] grep for `docs/PLANS.md` returns 0 matches in all .md files
  - [ ] grep for root `PLAN.md` reference returns 0 matches
  - [ ] All new files exist
  - [ ] All old files deleted

  **QA Scenarios**:
  ```
  Scenario: Zero old path references
    Tool: Bash
    Steps:
      1. grep -r "docs/exec-plans" --include="*.md" . 2>/dev/null | wc -l
      2. grep -r "docs/PLANS\.md" --include="*.md" . 2>/dev/null | wc -l
      3. grep -r "PLAN\.md" --include="*.md" . 2>/dev/null | grep -v "PLAN.md:" | wc -l
    Expected Result: All return 0
    Evidence: .sisyphus/evidence/task-11-zero-old-refs.txt

  Scenario: New files exist
    Tool: Bash
    Steps:
      1. test -f .sisyphus/roadmap.md && echo "roadmap.md OK"
      2. test -f .sisyphus/tech-debt-tracker.md && echo "tech-debt-tracker.md OK"
    Expected Result: Both print OK
    Evidence: .sisyphus/evidence/task-11-new-files-exist.txt

  Scenario: Old files deleted
    Tool: Bash
    Steps:
      1. test ! -f PLAN.md && echo "PLAN.md deleted"
      2. test ! -f docs/PLANS.md && echo "docs/PLANS.md deleted"
      3. test ! -d docs/exec-plans && echo "docs/exec-plans deleted"
    Expected Result: All print "deleted"
    Evidence: .sisyphus/evidence/task-11-old-files-deleted.txt
  ```

  **Commit**: YES
  - Message: `refactor: consolidate plans to .sisyphus/ directory`
  - Files: All changed files
  - Pre-commit: None (documentation only)

---

## Final Verification Wave (MANDATORY)

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Verify all tasks completed: new files exist, old files deleted, references updated. Check evidence files.
  Output: `Files [N/N] | References [N/N] | Evidence [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Reference Integrity Check** — `quick`
  Run grep commands to verify zero old references. Check all new references are valid (files exist).
  Output: `Old refs [0] | New refs [N valid] | VERDICT: APPROVE/REJECT`

---

## Commit Strategy

- **Single Commit**: `refactor: consolidate plans to .sisyphus/ directory`
  - Files: All modified files from Waves 1-3
  - Pre-commit: None required (documentation/file moves)

---

## Success Criteria

### Verification Commands
```bash
# Verify zero old references
grep -r "docs/exec-plans" --include="*.md" .  # Expected: 0 matches
grep -r "docs/PLANS\.md" --include="*.md" .   # Expected: 0 matches

# Verify new files exist
test -f .sisyphus/roadmap.md && echo "OK"          # Expected: OK
test -f .sisyphus/tech-debt-tracker.md && echo "OK" # Expected: OK

# Verify old files deleted
test ! -f PLAN.md && echo "OK"                # Expected: OK
test ! -f docs/PLANS.md && echo "OK"          # Expected: OK
test ! -d docs/exec-plans && echo "OK"        # Expected: OK
```

### Final Checklist
- [ ] `.sisyphus/roadmap.md` exists
- [ ] `.sisyphus/tech-debt-tracker.md` exists with updated self-references
- [ ] `PLAN.md` deleted
- [ ] `docs/exec-plans/` deleted
- [ ] `docs/PLANS.md` deleted
- [ ] AGENTS.md references updated
- [ ] ARCHITECTURE.md references updated
- [ ] SPEC.md references updated
- [ ] README.md references updated
- [ ] TEMPLATE.md references updated
- [ ] All QA scenarios pass
- [ ] Single commit created