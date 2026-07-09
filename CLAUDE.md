# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency and environment management.

```bash
# Install/sync dependencies
uv sync

# Run the API server (auto-reload for development)
uv run uvicorn main:app --reload

# Add a dependency
uv add <package>
```

The server exposes interactive docs at `/docs` (Swagger) and `/redoc` once running.

There is currently no test suite, linter, or formatter configured.

## Configuration

The database connection is read from a `DATABASE_URL` environment variable, loaded from a `.env` file at the repo root via `python-dotenv` (`load_dotenv(override=True)` in `core/database.py`). `psycopg2` is a dependency, so PostgreSQL is the expected backend. Tables are auto-created on startup by `Base.metadata.create_all(bind=engine)` in `main.py` — there are no migrations.

## Architecture

This is a FastAPI CRUD service written with a deliberate Spring Boot-style layered architecture (the code comments draw explicit Java/JPA analogies). Each domain feature flows top-to-bottom through the same four layers, and a new feature should follow the same pattern:

```
api/         Route handlers (APIRouter). HTTP concerns only — status codes,
             HTTPException, dependency injection of the DB session.
services/    Business logic layer. Currently thin pass-throughs to repositories;
             this is where validation/filtering/transformation belongs.
repositories/  Data access. All SQLAlchemy queries (db.query(...)) live here.
models/      SQLAlchemy ORM models (tables), subclassing core.database.Base.
schemas/     Pydantic request/response models with field validation.
```

Cross-cutting infrastructure lives in `core/`:
- `core/database.py` — SQLAlchemy `engine`, `sessionmaker` (`session`), the declarative `Base`, and the `get_db()` generator dependency injected into routes via `Depends(get_db)`.
- `core/limiter.py` — a shared `slowapi` `Limiter` keyed on remote address, applied per-route with the `@limiter.limit(...)` decorator.

`main.py` is the composition root: it creates the `FastAPI` app, wires CORS (allowing `http://localhost:3000`), registers routers, attaches the rate limiter and its `RateLimitExceeded` handler, and adds an HTTP middleware that stamps each response with an `X-Process-Time` header.

### Conventions when adding a feature

- Register new routers in `main.py` via `app.include_router(...)`.
- Route handlers receive the DB session through `db: Session = Depends(get_db)`.
- Keep query logic in the repository layer, not in route handlers — note some existing handlers (e.g. `update_product`, `get_product_by_id` in `api/product_api.py`) query the DB directly, bypassing the service/repository layers; prefer routing through the service layer for new code.
