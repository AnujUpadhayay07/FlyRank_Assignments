import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.llm.schema import TriageInput, TriageOutput
from src.llm.triage import run_triage, TriageFailure

app = FastAPI(title="Triage API")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Reject bad input with a 400 naming the field, before any model call is made.
    errors = [{"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
              for e in exc.errors()]
    return JSONResponse(status_code=400, content={"detail": "Invalid input", "errors": errors})

STUB_RESPONSE = TriageOutput(
    category="bug",
    urgency="normal",
    suggested_team="engineering",
    confidence=0.87,
    reason="Stub response for local development.",
)


@app.post("/triage", response_model=TriageOutput)
def triage(payload: TriageInput):
    if os.environ.get("LLM_STUB") == "1":
        return STUB_RESPONSE

    try:
        return run_triage(payload.text)
    except TriageFailure as e:
        raise HTTPException(status_code=422, detail=e.message)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Model call timed out.")