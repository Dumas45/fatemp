import asyncio

from temporalio import activity

from app.models import ChildInput, ChildResult, ParentInput


@activity.defn
async def prepare_data(data: ParentInput) -> list[int]:
    """Emulates some slow preparation work."""
    await asyncio.sleep(2)
    return [i * i for i in range(1, data.items + 1)]


@activity.defn
async def process_data(data: ChildInput) -> ChildResult:
    """Emulates some slow processing work."""
    await asyncio.sleep(2)
    return ChildResult(
        name=data.name,
        processed=len(data.records),
        checksum=sum(data.records),
    )
