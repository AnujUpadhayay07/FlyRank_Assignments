import logging

import inngest


inngest_client = inngest.Inngest(
    app_id="background-job-api",
    logger=logging.getLogger("uvicorn"),
)