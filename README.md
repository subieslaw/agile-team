# Agile Team Helper

Backend REST API for managing agile teams — members, skills, vacations, trainings, velocity, and goals.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL 16 (asyncpg) |
| ORM | SQLAlchemy 2.x async + Alembic |
| Validation | Pydantic v2 |
| Package manager | uv |
| Testing | pytest + pytest-bdd + httpx |
| Linting | ruff |
| Container | Docker + Docker Compose |

---

## Quick Start (Docker Compose)

### 1. Copy environment file

```sh
cp .env.example .env
```

Edit `.env` and set a real `POSTGRES_PASSWORD` for any non-local environment.

### 2. Start the stack

```sh
make dev
```

This builds the image, starts PostgreSQL, waits for it to be healthy, runs `alembic upgrade head`, then starts the API on port 8000.

### 3. Verify

```sh
curl http://localhost:8000/api/v1/members
# {"data":[],"error":null}
```

---

## Running Locally (without Docker)

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A running PostgreSQL instance (or use `sqlite+aiosqlite:///./dev.db` for quick local dev)

### Install dependencies

```sh
uv sync --dev
```

### Configure

```sh
cp .env.example .env
# Edit DATABASE_URL to point at your local DB
```

### Run migrations

```sh
make migrate
```

### Start the server

```sh
uv run uvicorn app.main:app --reload
```

API available at `http://localhost:8000`.

---

## Build

### Docker image only

```sh
make build
# produces agile-team-helper:local
```

### Push to a registry

```sh
docker tag agile-team-helper:local ghcr.io/<org>/agile-team-helper:latest
docker push ghcr.io/<org>/agile-team-helper:latest
```

The GitHub Actions CI workflow (`.github/workflows/ci.yml`) builds and pushes automatically on every merge to `main` using GHCR.

---

## Makefile Reference

```
make dev          Start full stack with docker compose (builds image first)
make down         Stop and remove containers
make logs         Tail app container logs
make shell        Open a shell in the running app container

make test         Run test suite (pytest, uses in-memory SQLite — no DB needed)
make test-v       Same, verbose output
make lint         ruff check + format check
make fmt          ruff auto-fix + format

make migrate      Run alembic upgrade head (against DATABASE_URL in .env)
make migrate-down Roll back one migration
make migration name=<desc>   Generate a new autogenerate migration

make build        Build Docker image tagged agile-team-helper:local
```

---

## Project Structure

```
src/app/
├── main.py                  # FastAPI app factory and lifespan
├── config.py                # Pydantic Settings (reads .env)
├── dependencies.py          # Shared FastAPI dependencies
├── api/v1/
│   ├── router.py            # Aggregates all v1 routers
│   └── endpoints/
│       ├── members.py       # /members routes
│       └── skills.py        # /skills routes
├── core/members/
│   ├── schemas.py           # Pydantic input/output models
│   ├── service.py           # Business logic (CRUD)
│   └── exceptions.py        # Domain exceptions
└── db/
    ├── base.py              # DeclarativeBase + TimestampMixin
    ├── session.py           # Async engine + session factory
    └── models/
        ├── team_member.py
        ├── skill.py
        └── member_skill.py

migrations/
├── env.py                   # Alembic async config
└── versions/                # Migration scripts

tests/
├── conftest.py              # Fixtures: in-memory SQLite client + session
└── integration/
    ├── features/            # .feature files (BDD scenarios)
    └── step_defs/           # pytest-bdd step implementations
```

---

## API Endpoints

All responses use the envelope `{"data": ..., "error": null}`.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/members` | Create a team member |
| GET | `/api/v1/members` | List active members |
| GET | `/api/v1/members/{id}` | Get a member by ID |
| POST | `/api/v1/members/{id}/skills` | Assign a skill to a member |
| GET | `/api/v1/members/{id}/skills` | List skills for a member |
| POST | `/api/v1/skills` | Create a skill |
| GET | `/api/v1/skills` | List all skills |

Interactive docs: `http://localhost:8000/docs`

---

## Testing

Tests use an in-memory SQLite database and require no running services.

```sh
make test        # quiet
make test-v      # verbose, shows each BDD scenario
```

BDD feature files are in `tests/integration/features/`. Each endpoint has a dedicated `.feature` file covering happy path and edge cases.

---

## Database Migrations

Migrations are managed with Alembic and run automatically on container startup via `entrypoint.sh`.

```sh
# Generate a new migration after changing ORM models
make migration name=add_seniority_column

# Apply
make migrate

# Roll back one step
make migrate-down
```

`DATABASE_URL` must be set in `.env` when running migrations locally.

---

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and PR:

1. **Lint** — `ruff check` + `ruff format --check`
2. **Test** — `pytest` with in-memory SQLite (no services required)
3. **Build** — Docker image built with BuildKit layer caching
4. **Push** — Image pushed to GHCR only on merge to `main`

Image tags: `sha-<commit>` (every build) and `latest` (main only).

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | SQLAlchemy async URL, e.g. `postgresql+asyncpg://user:pass@host/db` |
| `DEBUG` | No | `true` enables SQLAlchemy query echo (default: `false`) |
| `POSTGRES_USER` | Compose only | PostgreSQL username for the `db` service |
| `POSTGRES_PASSWORD` | Compose only | PostgreSQL password |
| `POSTGRES_DB` | Compose only | PostgreSQL database name |

See `.env.example` for a full template.
