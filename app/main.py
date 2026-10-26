import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from temporalio.client import Client

from app.auth import get_current_user
from app.config import settings
from app.models import ParentInput
from app.temporal.workflows import ParentWorkflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal = await Client.connect(
        settings.temporal_address, namespace=settings.temporal_namespace
    )
    yield


app = FastAPI(title="FastAPI + Temporal demo", lifespan=lifespan)

CurrentUser = Annotated[str, Depends(get_current_user)]


class RunRequest(BaseModel):
    name: str = "demo"
    items: int = Field(default=5, ge=1, le=100)


@app.post("/workflows/run")
async def run_workflows(body: RunRequest, user: CurrentUser) -> dict:
    """Starts the parent workflow (which starts the child one) and waits for the result."""
    client: Client = app.state.temporal
    result = await client.execute_workflow(
        ParentWorkflow.run,
        ParentInput(name=body.name, items=body.items),
        id=f"parent-{uuid.uuid4()}",
        task_queue=settings.parent_task_queue,
    )
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
