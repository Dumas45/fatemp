import asyncio
import logging

from temporalio import activity

from app.models import ChildInput, ChildResult, ParentInput

logger = logging.getLogger(__name__)


@activity.defn
async def prepare_data(data: ParentInput) -> list[int]:
    """Emulates some slow preparation work."""
    logger.info("Preparing data for %d items", data.items)
    await asyncio.sleep(2)
    records = [i * i for i in range(1, data.items + 1)]
    logger.info("Prepared %d records", len(records))
    return records


@activity.defn
async def process_data(data: ChildInput) -> ChildResult:
    """Emulates some slow processing work."""
    logger.info("Processing %d records", len(data.records))
    await asyncio.sleep(2)
    result = ChildResult(
        name=data.name,
        processed=len(data.records),
        checksum=sum(data.records),
    )
    logger.info("Processed %d records", result.processed)
    return result
