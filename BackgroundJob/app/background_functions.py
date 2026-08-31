import inngest

from app.inngest_client import inngest_client


@inngest_client.create_function(
    fn_id="hello-background-job",
    trigger=inngest.TriggerEvent(event="app/background-job")
)
async def hello_background_job(ctx: inngest.Context) -> str:
    ctx.logger.info("Background job started")

    return "Background job completed successfully"