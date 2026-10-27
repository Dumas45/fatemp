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
- Grafana: http://localhost:3000 (anonymous admin access, demo only)
- Prometheus: http://localhost:9090
- Loki API: http://localhost:3100

## Observability

`docker compose up` also starts Grafana, Prometheus, Loki and Grafana Alloy. Config lives in [observability/](observability).

- Grafana provisions **Prometheus** (default) and **Loki** datasources, so both are available in *Explore*.
- Every service (Temporal server, API, both workers) exposes `/metrics` on the same port, `9464` (configurable with `METRICS_PORT` for the app services). The API serves it on this dedicated port, not on the public port 8000. In Kubernetes, name this container port `metrics` so one scrape rule fits every workload.
- Alloy reads all container logs from the Docker socket and pushes them to Loki, labelled with `compose_service`.

Example queries in Explore: LogQL `{compose_service="api"}`, PromQL `rate(http_requests_total[1m])`.

Application logs are written to stderr with timestamps, severity, and logger names.
Set `LOG_LEVEL` in `.env` to `DEBUG`, `INFO` (default), `WARNING`, `ERROR`, or `CRITICAL`.

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
