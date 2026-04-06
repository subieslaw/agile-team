.PHONY: dev down logs shell test test-v lint fmt migrate migrate-down migration build

# ── Local development ─────────────────────────────────────────────────────────
dev:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f app

shell:
	docker compose exec app /bin/sh

# ── Testing ───────────────────────────────────────────────────────────────────
test:
	uv run pytest --tb=short -q

test-v:
	uv run pytest -v

# ── Linting / formatting ──────────────────────────────────────────────────────
lint:
	uv run ruff check .
	uv run ruff format --check .

fmt:
	uv run ruff check --fix .
	uv run ruff format .

# ── Database migrations ───────────────────────────────────────────────────────
migrate:
	uv run alembic upgrade head

migrate-down:
	uv run alembic downgrade -1

migration:
	@test -n "$(name)" || (echo "Usage: make migration name=<description>" && exit 1)
	uv run alembic revision --autogenerate -m "$(name)"

# ── Docker ────────────────────────────────────────────────────────────────────
build:
	docker build --target final -t agile-team-helper:local .
