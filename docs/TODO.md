# TODO

Deferred work tracked from PR #3 review.

## Branch name validation

- [ ] Add GitHub Actions workflow to enforce the branch naming convention (`.github/workflows/validate-branch-name.yml`)
- [ ] Add branch naming convention documentation (`docs/git-branch-naming.md`)

Convention: branches (except `main`) must follow `<prefix>/<description>` format,
e.g. `feature/add-login`. Allowed prefixes: `feature`, `fix`, `hotfix`, `release`,
`docs`, `refactor`, `test`, `chore`, `ci`, `perf`.
