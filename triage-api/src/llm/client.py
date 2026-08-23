import os
import time
import random
import json
from openai import OpenAI, APITimeoutError, RateLimitError, APIStatusError

TIMEOUT_SECONDS = 30.0
MAX_RETRIES = 2  # on top of the initial attempt, for retryable errors only

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=os.environ["LLM_BASE_URL"],
            api_key=os.environ["LLM_API_KEY"],
            timeout=TIMEOUT_SECONDS,
            max_retries=0,  # we handle retries ourselves, explicitly, below
        )
    return _client


def _is_retryable(exc: Exception) -> bool:
    # Retry on timeouts, 429 (rate limit), and 5xx. Never on 400/401/403 -
    # a bad request or bad key will still be bad on the next attempt.
    if isinstance(exc, APITimeoutError):
        return True
    if isinstance(exc, RateLimitError):
        return True
    if isinstance(exc, APIStatusError):
        return 500 <= exc.status_code < 600
    return False


def log_cost(prompt_version: str, model: str, usage, duration_ms: float, repaired: bool):
    entry = {
        "ts": time.time(),
        "prompt_version": prompt_version,
        "model": model,
        "input_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
        "output_tokens": getattr(usage, "completion_tokens", None) if usage else None,
        "duration_ms": round(duration_ms, 1),
        "repaired": repaired,
    }
    print(json.dumps({"llm_call": entry}))  # structured log line to stdout


def call_model(system_prompt: str, user_content: str, prompt_version: str) -> tuple[str, object]:
    """Calls the model with a timeout and a bounded retry policy.
    Returns (raw_text, usage). Raises the last exception if all attempts fail."""
    client = get_client()
    model = os.environ["LLM_MODEL"]

    attempt = 0
    last_exc = None
    while attempt <= MAX_RETRIES:
        start = time.monotonic()
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.2,
            )
            duration_ms = (time.monotonic() - start) * 1000
            return res.choices[0].message.content, res.usage, duration_ms
        except Exception as exc:  # noqa: BLE001 - deliberately broad, we classify below
            last_exc = exc
            if not _is_retryable(exc) or attempt == MAX_RETRIES:
                raise
            backoff = (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(backoff)
            attempt += 1
    raise last_exc  # pragma: no cover