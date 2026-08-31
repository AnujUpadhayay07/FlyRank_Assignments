from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import inngest.fast_api

from app.inngest_client import inngest_client
from app.background_functions import hello_background_job


app = FastAPI(
    title="Background Job API",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


inngest.fast_api.serve(
    app,
    inngest_client,
    [hello_background_job]
)