import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from app.config import settings
from app.logging_config import configure_logging
from app.temporal.activities import process_data
from app.temporal.workflows import ChildWorkflow

logger = logging.getLogger(__name__)


async def main() -> None:
    configure_logging(settings.log_level)
    logger.info(
        "Connecting to Temporal at %s (namespace=%s)",
        settings.temporal_address,
        settings.temporal_namespace,
    )
    client = await Client.connect(
        settings.temporal_address, namespace=settings.temporal_namespace
    )
    logger.info("Connected to Temporal")
    worker = Worker(
        client,
        task_queue=settings.child_task_queue,
        workflows=[ChildWorkflow],
        activities=[process_data],
    )
    logger.info("Child worker listening on %s", settings.child_task_queue)
    await worker.run()
    logger.info("Child worker stopped")


if __name__ == "__main__":
    asyncio.run(main())
