# Project: Agile Team Helper
## Business context
- application to help manage agile team
- application consist of many modules
- First module: gather information about team memebers, names, skills, project assignment

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
- **SQLite** (via **grqlite** / local fallback) — lightweight local storage or testing
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
- hexagonal architectrure with ports and adapters
- rest api at resoureces level
- TDD: test driven design

## Project Structure
project-root/
├── src/
│ └── app/
│ ├── _init_.py
│ ├── main.py # FastAPI app factory, lifespan, middleware
│ ├── config.py # Pydantic Settings, env var loading
│ ├── dependencies.py # Shared FastAPI dependencies (DB session, auth)
│ │
│ ├── api/ # Route handlers only, no business logic
│ │ ├── _init_.py
│ │ ├── v1/
│ │ │ ├── _init_.py
│ │ │ ├── router.py # Aggregates all v1 routers
│ │ │ └── endpoints/ # One file per resource
│ │ │ ├── health.py
│ │ │ └── <resource>.py
│ │
│ ├── core/ # Business logic, services, use cases
│ │ ├── _init_.py
│ │ └── <domain>/
│ │ ├── service.py
│ │ └── schemas.py # Pydantic input/output models
│ │
│ ├── db/ # Database layer
│ │ ├── _init_.py
│ │ ├── session.py # Async SQLAlchemy engine & session factory
│ │ ├── base.py # Declarative base
│ │ └── models/ # SQLAlchemy ORM models, one file per table
│ │
│ ├── llm/ # Local model integration
│ │ ├── _init_.py
│ │ ├── client.py # Local model client (Ollama/llama.cpp wrapper)
│ │ └── prompts/ # Prompt templates
│ │
│ └── migrations/ # Alembic migrations
│ ├── env.py
│ ├── script.py.mako
│ └── versions/
│
├── tests/
│ ├── conftest.py # pytest fixtures, test DB setup
│ ├── unit/ # Pure logic, no I/O
│ └── integration/ # API route tests using httpx AsyncClient
│
├── docker/
│ ├── Dockerfile
│ └── docker-compose.yml # App + PostgreSQL services
│
├── .ruff.toml # Ruff linting & formatting config
├── alembic.ini
├── pyproject.toml # uv project config, dependencies, tool settings
├── uv.lock
├── .env.example # Template for required environment variables
├── .gitignore
└── CLAUDE.md

### Key Conventions
- All source code lives under `src/app/` — installed as a package via `uv`
- Route handlers in `api/` are thin: validate input, call `core/` service, return response
- Database models in `db/models/` are strictly ORM definitions — no business logic
- Pydantic schemas in `core/<domain>/schemas.py` are separate from ORM models
- `tests/` mirrors `src/app/` structure where applicable
- Environment variables are never hardcoded — always loaded via `config.py`

## Conventions
- Use async/await, not callbacks
- All API responses use { data, error } envelope
- Tests go in /tests, named *.test.js
## Commands (uv)

### Setup
```bash
uv sync                          # install all dependencies
uv sync --all-extras --dev       # include dev dependencies
uv python pin 3.12               # pin Python version
```

### Run
```bash
uv run python main.py            # run app
uv run python -m <module>        # run module
uv run python                    # interactive shell
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
uv export --format requirements-txt > requirements.txt
uv build                         # build dist
uv self update                   # update uv
```- `npm run dev` — start dev server
- `npm test` — run tests