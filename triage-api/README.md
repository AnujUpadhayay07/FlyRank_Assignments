# Triage API

Classifies an incoming customer support message into a category, urgency level, and
suggested team — so it lands in the right queue automatically instead of a human
reading every ticket first.

## Quickstart

```bash
pip install -r requirements.txt
# copy .env.example to .env and add your OpenRouter key
uvicorn src.main:app --port 8000
```

Valid request:
```bash
curl -s -X POST http://127.0.0.1:8000/triage \
  -H "Content-Type: application/json" \
  -d '{"text":"I was charged twice this month, please refund the extra charge"}'
```
Response:
```json
{"category":"billing","urgency":"high","suggested_team":"billing","confidence":0.95,"reason":"Customer reports being charged twice this month and requests a refund for the duplicate charge."}
```

Invalid request (missing field, rejected before any model call):
```bash
curl -s -X POST http://127.0.0.1:8000/triage -H "Content-Type: application/json" -d '{}'
```
```json
{"detail":"Invalid input","errors":[{"field":"text","message":"Field required"}]}
```

## Job card

See [JOB-CARD.md](./JOB-CARD.md) for the full input/output contract, the closed
value lists, and the "must never" rules.

## Provider

- OpenRouter, model `openrouter/free`, via the OpenAI-compatible client
- Env vars needed to swap provider: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
- Swapping to a different OpenAI-compatible provider (e.g. Ollama running locally)
  is a three-value change in `.env` — no code changes needed. That's the whole
  reason nothing in this codebase hard-codes a provider.

## Reliability

- **Timeout:** 30s client-side timeout set explicitly (the SDK's default of 10
  minutes was overridden — see `src/llm/client.py`)
- **Retries:** on timeouts, 429, and 5xx only — never on 400/401/403, since a bad
  request or bad key will still be bad on the next attempt. Exponential backoff
  with jitter, max 2 retries. SDK's own built-in retries were disabled
  (`max_retries=0`) so this policy is the only one in effect.
- **Repair loop:** if the model's output fails JSON parsing or schema validation,
  one repair call is made with the model's own broken output and the exact
  validation error attached. If that also fails, the endpoint returns `422` and
  logs the raw output + error to `logs/quarantine.jsonl`. The process never
  crashes and raw model text is never returned to the caller.
- **Kill switch:** `LLM_ENABLED=false` skips the model call entirely and returns
  a deterministic fallback (`category: other`, `confidence: 0`) instead.
- **Cost logging:** every call logs prompt version, model, input/output token
  counts, duration in ms, and whether a repair was needed, as a structured JSON
  line to stdout.

## Eval

Run with the server up and a real key set:
```bash
python evals/run_eval.py
```
8 hand-labelled cases in `evals/cases.json`, covering a clear case per category,
one deliberately ambiguous case, and one nonsense case meant to trigger the
"when unsure" rule.

- **Score: 7/8** on category match
- **Date:** 2026-08-23
- **Prompt version:** triage-v1
- The one miss: *"Can you explain the difference between the Pro and Team pricing
  tiers?"* — expected `billing`, got `feature`. This is a genuinely ambiguous
  message (pricing info is arguably a product question, not a billing complaint),
  so the model's call isn't unreasonable — it's a case worth revisiting in a v2
  prompt with an extra example to bias it toward `billing` for pricing questions.

## Cost

One real call from the logs: 484 input tokens, 224 output tokens, ~4.7s.
`openrouter/free` costs nothing per call on the free tier, so the cost at 10,000
requests/day is $0 as long as usage stays within OpenRouter's free-tier rate
limits (20 req/min, 50 req/day per key) — which a real production deployment
would exceed immediately, meaning a paid model would be needed at that volume.

## What I'd fix with another day

Widen the eval set to 25 cases split into easy/hard, add a few prompt-injection
attack cases to check whether the "never reveal instructions" rule actually
holds, and add a second example to the prompt for pricing/billing-adjacent
messages to fix the one eval miss above.