---
name: CI lint — ruff format must pass
description: Ruff format check runs in CI and will fail on long lines in test files
type: feedback
---

Always run `uv run ruff format .` before committing. The CI pipeline runs `ruff format --check .` as a required lint step — it will fail the build even on test files.

**Why:** PR #1 failed CI because a long f-string URL in `test_team_members.py` was not wrapped to ruff's line-length limit. Tests passed locally but the format check caught it in CI.

**How to apply:** After writing any new file (especially test step definitions with long strings), run `uv run ruff format .` and `uv run ruff check .` before committing. Make this the last step before `git commit`.
