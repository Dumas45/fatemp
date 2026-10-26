import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from app.config import settings
from app.temporal.activities import process_data
from app.temporal.workflows import ChildWorkflow


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect(
        settings.temporal_address, namespace=settings.temporal_namespace
    )
    worker = Worker(
        client,
        task_queue=settings.child_task_queue,
        workflows=[ChildWorkflow],
        activities=[process_data],
    )
    logging.info("Child worker listening on %s", settings.child_task_queue)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
