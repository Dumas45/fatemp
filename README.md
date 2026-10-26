# FastAPI + Temporal demo

Learning project: FastAPI (HTTP Basic auth) triggering chained Temporal workflows.

- `ParentWorkflow` (queue `parent-queue`) prepares data, then starts `ChildWorkflow` (queue `child-queue`).
- Each workflow runs in its own worker container.

## Run

```bash
cp .env.example .env   # optional, defaults are admin / changeme
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Temporal UI: http://localhost:8233

```bash
# Triggers Temporal workflows (takes ~4s)
curl -u admin:changeme -X POST localhost:8000/workflows/run \
  -H 'Content-Type: application/json' -d '{"name": "demo", "items": 5}'

# No Temporal involved
curl -u admin:changeme localhost:8000/info
```

## Local development

```bash
uv sync
uv run python -m app.temporal.parent_worker
uv run python -m app.temporal.child_worker
uv run uvicorn app.main:app --reload
```
(requires a Temporal server on `localhost:7233`, e.g. `temporal server start-dev`).
