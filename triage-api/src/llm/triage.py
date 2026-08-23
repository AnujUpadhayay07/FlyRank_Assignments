import json
import os
import re
import time
from pathlib import Path
from pydantic import ValidationError

from src.llm.schema import TriageOutput
from src.llm.client import call_model, log_cost

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "triage-v1.md"
PROMPT_VERSION = "triage-v1"
QUARANTINE_PATH = Path(__file__).parent.parent.parent / "logs" / "quarantine.jsonl"

_SYSTEM_PROMPT = None


def get_system_prompt() -> str:
    global _SYSTEM_PROMPT
    if _SYSTEM_PROMPT is None:
        _SYSTEM_PROMPT = PROMPT_PATH.read_text()
    return _SYSTEM_PROMPT


def _extract_json(raw: str) -> dict:
    # Models like to wrap JSON in a ```json fence or add a sentence before it.
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    candidate = fenced.group(1) if fenced else raw
    if not fenced:
        brace = re.search(r"\{.*\}", raw, re.DOTALL)
        if brace:
            candidate = brace.group(0)
    return json.loads(candidate)


def _quarantine(input_text: str, raw_output: str, error: str):
    QUARANTINE_PATH.parent.mkdir(exist_ok=True)
    with open(QUARANTINE_PATH, "a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "prompt_version": PROMPT_VERSION,
            "input": input_text,
            "raw_output": raw_output,
            "error": error,
        }) + "\n")


class TriageFailure(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def run_triage(text: str) -> TriageOutput:
    if os.environ.get("LLM_ENABLED", "true").lower() == "false":
        # Kill switch: deterministic fallback, zero model calls.
        return TriageOutput(
            category="other", urgency="normal", suggested_team="support",
            confidence=0.0, reason="AI triage disabled; routed to default queue.",
        )

    system_prompt = get_system_prompt()
    repaired = False
    raw = None

    for attempt in ("initial", "repair"):
        try:
            if attempt == "initial":
                raw, usage, duration_ms = call_model(system_prompt, text, PROMPT_VERSION)
            else:
                repaired = True
                repair_user_msg = (
                    f"Original message: {text}\n\n"
                    f"Your previous answer was rejected for this reason: {last_error}\n"
                    f"Previous answer: {raw}\n\n"
                    "Return only corrected JSON matching the schema."
                )
                raw, usage, duration_ms = call_model(system_prompt, repair_user_msg, PROMPT_VERSION)

            parsed_dict = _extract_json(raw)
            output = TriageOutput.model_validate(parsed_dict)
            log_cost(PROMPT_VERSION, os.environ["LLM_MODEL"], usage, duration_ms, repaired)
            return output

        except (json.JSONDecodeError, ValidationError) as e:
            last_error = str(e)
            if attempt == "repair":
                _quarantine(text, raw or "", last_error)
                raise TriageFailure(f"Model output failed validation twice: {last_error}")
        except Exception as e:  # noqa: BLE001 - timeouts/API errors from call_model
            raise TriageFailure(f"Model call failed: {e}")