"""Runs evals/cases.json against the live endpoint and reports match rate on category."""
import json
import sys
from pathlib import Path

import requests

ENDPOINT = "http://127.0.0.1:8000/triage"
CASES_PATH = Path(__file__).parent / "cases.json"


def main():
    cases = json.loads(CASES_PATH.read_text())
    correct = 0
    failures = []

    for i, case in enumerate(cases, 1):
        resp = requests.post(ENDPOINT, json={"text": case["text"]})
        if resp.status_code != 200:
            failures.append((i, case["text"], f"HTTP {resp.status_code}: {resp.text}"))
            continue
        body = resp.json()
        got = body.get("category")
        expected = case["expected_category"]
        if got == expected:
            correct += 1
        else:
            failures.append((i, case["text"], f"expected={expected} got={got}"))

    print(f"\n{correct}/{len(cases)} correct on category\n")
    for i, text, reason in failures:
        print(f"  FAIL #{i}: {reason}\n    input: {text[:80]}")

    if not failures:
        print("  All cases passed.")


if __name__ == "__main__":
    main()