import logging
import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from prometheus_client import start_http_server
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from temporalio.client import Client

from app.auth import get_current_user
from app.config import settings
from app.logging_config import configure_logging
from app.models import ParentInput
from app.temporal.workflows import ParentWorkflow

configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Metrics are served on a dedicated port, not on the public API port
    start_http_server(settings.metrics_port)
    logger.info("Metrics available on port %d", settings.metrics_port)
    logger.info(
        "Connecting to Temporal at %s (namespace=%s)",
        settings.temporal_address,
        settings.temporal_namespace,
    )
    app.state.temporal = await Client.connect(
        settings.temporal_address, namespace=settings.temporal_namespace
    )
    logger.info("Connected to Temporal")
    yield
    logger.info("FastAPI application shutting down")


app = FastAPI(title="FastAPI + Temporal demo", lifespan=lifespan)
Instrumentator().instrument(app)

CurrentUser = Annotated[str, Depends(get_current_user)]


class RunRequest(BaseModel):
    name: str = "demo"
    items: int = Field(default=5, ge=1, le=100)


@app.post("/workflows/run")
async def run_workflows(body: RunRequest, user: CurrentUser) -> dict:
    """Starts the parent workflow (which starts the child one) and waits for the result."""
    client: Client = app.state.temporal
    workflow_id = f"parent-{uuid.uuid4()}"
    logger.info("Starting workflow %s for %d items", workflow_id, body.items)
    result = await client.execute_workflow(
        ParentWorkflow.run,
        ParentInput(name=body.name, items=body.items),
        id=workflow_id,
        task_queue=settings.parent_task_queue,
    )
    logger.info("Workflow %s completed", workflow_id)
    return {"requested_by": user, "result": asdict(result)}


@app.get("/info")
async def info(user: CurrentUser) -> dict:
    """Plain route, no Temporal involved."""
    return {
        "service": "fatemp",
        "user": user,
        "time": datetime.now(UTC).isoformat(),
        "random_number": uuid.uuid4().int % 1000,
    }
