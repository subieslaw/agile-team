# Project: Agile Team Helper
## Business context
- Application to help manage agile teams
- Application consists of many modules
- **Domain**: `agile-team` — the Team is the core entity
- First module: gather information about team members, names, skills, project assignment

## What has been implemented (as of 2026-04-25)

### Module 1 — Team Members & Skills (complete)
- **DB models**: `TeamMember`, `Skill`, `MemberSkill` (join table) — UUIDs, timestamps, cascade deletes
  - `TeamMember.team_id` FK → `teams.id` (nullable, SET NULL on delete)
- **Service layer** (`src/app/core/members/`): full CRUD for members and skills, skill assignment, domain exceptions
- **REST API** (`/api/v1/`):
  - `POST/GET /members` — create & list members
  - `GET /members/{id}` — get single member
  - `POST/GET /members/{id}/skills` — assign & list member skills
  - `POST/GET /skills` — create & list skills
- **BDD integration tests**: ~25 scenarios covering happy paths, duplicates, not-found errors
- **Migration**: `e0e29e712e09_initial_schema.py` — creates `skills`, `team_members`, `member_skills`

### Team Entity — core domain entity (complete)
- **DB model**: `Team` with id, name (unique), description, status (`active`/`archived`), timestamps
- **Service layer** (`src/app/core/teams/`): create, list, get, update, archive, member assignment
- **REST API** (`/api/v1/teams`):
  - `POST/GET /teams` — create & list teams (archived excluded from list and get)
  - `GET/PATCH/DELETE /teams/{id}` — get, update, archive
  - `POST/DELETE /teams/{id}/members/{member_id}` — assign & remove member
  - `GET /teams/{id}/members` — list team members
- **BDD integration tests**: 13 scenarios, 38 total passing
- **Migration**: `b7e3f1a92c04_add_teams_table.py` — creates `teams`, migrates `team_members.team` string → `team_id` FK

### Infrastructure
- FastAPI app factory with lifespan, Pydantic v2 settings, SQLAlchemy 2.x async + Alembic
- Docker + docker-compose (app + PostgreSQL)
- Makefile, `.env.example`, `alembic.ini`, `pyproject.toml` with uv
- Memory files at `.claude/memory/` (project-local)

## Not yet implemented
- Project domain (project CRUD, member-project assignments)
- Health check endpoint
- Filtering/pagination on member list
- LLM integration (`/llm/` directory is empty)
- Authentication / RBAC
- `dependencies.py` (currently auth/db deps are inline)

## Technology Stack

### Runtime & Language
- **Python 3.13** (latest stable 3.x)
- Package manager: **uv** (dependency resolution, virtual environments, script running)

### Web Framework
- **FastAPI** — async REST API framework
- **Uvicorn** — ASGI server for running the application
- **Pydantic v2** — request/response validation and settings management

### Databases
- **PostgreSQL** — primary relational database
- **SQLite** (via aiosqlite / local fallback) — lightweight local storage or testing
- Use **SQLAlchemy 2.x** (async) as ORM with **Alembic** for migrations

### AI / LLM Integration
- **Local models only** — no external LLM API calls
- Inference via local runtime (e.g. **Ollama** or direct model loading)

### Infrastructure & Deployment
- **Docker** — containerized application and service orchestration
- **docker-compose** — local development stack (app + PostgreSQL)

### Testing
- **pytest** — primary test runner
- **pytest-asyncio** — async test support for FastAPI routes
- **pytest-bdd** - use for bdd testing
- **httpx** — async HTTP client for API integration tests

### Code Quality
- **ruff** — linting and formatting (replaces black, isort, flake8)
- Type hints required on all public functions and route handlers

### Project Conventions
- All configuration via environment variables using **Pydantic Settings**
- No frontend — pure backend API, consumed by external clients
- Async-first: prefer `async def` for all route handlers and DB calls

## Architecture
- Hexagonal architecture with ports and adapters
- REST API at resources level
- TDD: test driven design

## Project Structure
```
project-root/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py             # FastAPI app factory, lifespan, middleware
│       ├── config.py           # Pydantic Settings, env var loading
│       ├── dependencies.py     # Shared FastAPI dependencies (DB session, auth)
│       │
│       ├── api/                # Route handlers only, no business logic
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── router.py   # Aggregates all v1 routers
│       │   │   └── endpoints/  # One file per resource
│       │   │       ├── health.py
│       │   │       ├── members.py
│       │   │       ├── skills.py
│       │   │       └── teams.py
│       │
│       ├── core/               # Business logic, services, use cases
│       │   ├── __init__.py
│       │   ├── members/
│       │   │   ├── service.py
│       │   │   ├── schemas.py
│       │   │   └── exceptions.py
│       │   └── teams/
│       │       ├── service.py
│       │       ├── schemas.py
│       │       └── exceptions.py
│       │
│       ├── db/                 # Database layer
│       │   ├── __init__.py
│       │   ├── session.py      # Async SQLAlchemy engine & session factory
│       │   ├── base.py         # Declarative base + TimestampMixin
│       │   └── models/         # SQLAlchemy ORM models, one file per table
│       │       ├── team_member.py
│       │       ├── skill.py
│       │       ├── member_skill.py
│       │       └── team.py
│       │
│       ├── llm/                # Local model integration (not yet implemented)
│       │   ├── __init__.py
│       │   ├── client.py
│       │   └── prompts/
│       │
│       └── migrations/         # Alembic migrations
│           ├── env.py
│           ├── script.py.mako
│           └── versions/
│               └── e0e29e712e09_initial_schema.py
│
├── tests/
│   ├── conftest.py             # pytest fixtures, in-memory SQLite test DB
│   ├── unit/
│   └── integration/
│       ├── features/           # BDD .feature files
│       └── step_defs/          # pytest-bdd step implementations
│
├── docker/
├── .ruff.toml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── CLAUDE.md
```

### Key Conventions
- All source code lives under `src/app/` — installed as a package via `uv`
- Route handlers in `api/` are thin: validate input, call `core/` service, return response
- Database models in `db/models/` are strictly ORM definitions — no business logic
- Pydantic schemas in `core/<domain>/schemas.py` are separate from ORM models
- `tests/` mirrors `src/app/` structure where applicable
- Environment variables are never hardcoded — always loaded via `config.py`
- All API responses use `{ "data": ..., "error": null }` envelope
- Use async/await everywhere — no sync DB or HTTP calls

## Commands (uv)

### Setup
```bash
uv sync                          # install all dependencies
uv sync --all-extras --dev       # include dev dependencies
```

### Run
```bash
uv run uvicorn app.main:app --reload   # start dev server
uv run python -m <module>              # run module
```

### Dependencies
```bash
uv add <pkg>                     # add runtime dep
uv add --dev pytest ruff mypy    # add dev deps
uv remove <pkg>                  # remove dep
uv lock                          # regenerate lockfile
uv tree                          # show dep tree
```

### Testing
```bash
uv run pytest                    # run all tests
uv run pytest -v                 # verbose
uv run pytest -k "test_name"     # filter by name
uv run pytest --cov              # with coverage
```

### Code Quality
```bash
uv run ruff check .              # lint
uv run ruff check . --fix        # lint + autofix
uv run ruff format .             # format
uv run mypy .                    # type check
```

### Utilities
```bash
uv pip list                      # list packages
uv build                         # build dist
uv self update                   # update uv
```
