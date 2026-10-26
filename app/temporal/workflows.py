from datetime import timedelta

from temporalio import workflow

logger = workflow.logger

with workflow.unsafe.imports_passed_through():
    from app.config import settings
    from app.models import ChildInput, ChildResult, ParentInput, ParentResult
    from app.temporal.activities import prepare_data, process_data


@workflow.defn
class ChildWorkflow:
    @workflow.run
    async def run(self, data: ChildInput) -> ChildResult:
        logger.info("Starting child workflow with %d records", len(data.records))
        result = await workflow.execute_activity(
            process_data,
            data,
            start_to_close_timeout=timedelta(seconds=30),
        )
        logger.info("Child workflow processed %d records", result.processed)
        return result


@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, data: ParentInput) -> ParentResult:
        logger.info("Preparing workflow data for %d items", data.items)
        records = await workflow.execute_activity(
            prepare_data,
            data,
            start_to_close_timeout=timedelta(seconds=30),
        )
        logger.info("Starting child workflow with %d records", len(records))
        # The child runs on a different task queue, i.e. on the other worker.
        child = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            ChildInput(name=data.name, records=records),
            id=f"{workflow.info().workflow_id}-child",
            task_queue=settings.child_task_queue,
        )
        return ParentResult(
            name=data.name,
            workflow_id=workflow.info().workflow_id,
            prepared_records=records,
            child=child,
        )
