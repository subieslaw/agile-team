---
name: Project state — Agile Team Helper
description: What has been built and what is next in the Agile Team Helper project
type: project
---

## Completed as of 2026-04-25

### Module 1 — Team Members & Skills (complete, session 1)
- DB models: `TeamMember`, `Skill`, `MemberSkill`
- Service layer `src/app/core/members/`: CRUD + skill assignment + domain exceptions
- REST API `/api/v1/members` and `/api/v1/skills` (7 endpoints)
- BDD integration tests: ~25 scenarios
- Migration: `e0e29e712e09_initial_schema.py` (do not modify — already applied)

### Team Entity — Core domain entity (session 2)
- **DB model** `src/app/db/models/team.py`: `Team` with id, name, description, status, timestamps
- **Core layer** `src/app/core/teams/`: schemas, exceptions, service (create/list/get/update/archive + member assignment)
- **REST API** `src/app/api/v1/endpoints/teams.py` — 8 endpoints:
  - `POST/GET /teams`, `GET/PATCH/DELETE /teams/{id}`
  - `POST/DELETE /teams/{id}/members/{member_id}`, `GET /teams/{id}/members`
- **Migration** `migrations/versions/b7e3f1a92c04_add_teams_table.py`: creates `teams` table, drops `team_members.team` string, adds `team_members.team_id` FK
- **BDD tests** `tests/integration/features/teams/` + `tests/integration/step_defs/teams/`: 13 scenarios, all passing
- **Breaking change**: `TeamMember.team` (String) replaced by `TeamMember.team_id` (FK → teams.id)
- All 38 tests pass
- PR #1 merged — all CI checks green (Lint, Test, Build & push Docker image)

### Infrastructure
- CLAUDE.md updated with full project state and structure
- Memory files at `/workspace/.claude/memory/` (project-local, version-controlled)
- Docker + docker-compose, Makefile, `.env.example`, `alembic.ini`

## Not yet implemented
- Project domain (project CRUD, member-project assignments)
- Health check endpoint (`/health`)
- Filtering/pagination on member/team list
- LLM integration (`src/app/llm/` is empty)
- Authentication / RBAC
- `src/app/dependencies.py` (auth/db deps currently inline in endpoints)

## Extensibility strategy for Team
All future team-level concepts hang off `teams.id` as child tables (contracts, projects, properties).
The `Team` model stays lean — adding a new concept = new table + new FK, no schema change to `teams`.

**Why:** Team is the core entity of the `agile-team` domain per CLAUDE.md.
**How to apply:** Next session can pick up from "Not yet implemented" above. Read CLAUDE.md first.

## Next session topic
Plan UX and UI for the developed REST API.
