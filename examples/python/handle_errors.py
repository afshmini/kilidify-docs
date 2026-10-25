"""Branching on Kilidify's error codes.

The point of this file: branch on `code`, never on `message`. Messages are
written for people and come in two languages; the codes are the contract.

    pip install openai
    KILIDIFY_API_KEY=kl_live_… python handle_errors.py
"""

import os
import sys

from openai import APIStatusError, OpenAI

client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key=os.environ.get("KILIDIFY_API_KEY", "kl_live_deliberately_invalid"),
)

# 402 never succeeds on a retry, 429 will eventually, 5xx usually will.
# Retrying everything turns an empty wallet into a tight loop.
TOP_UP_NEEDED = {"insufficient_balance", "trial_tokens_exhausted", "not_provisioned"}
RETRYABLE = {
    "rate_limit_exceeded",
    "concurrency_limit_exceeded",
    "upstream_unavailable",
    "upstream_timeout",
    "internal_error",
}

try:
    reply = client.chat.completions.create(
        model="anthropic/claude-sonnet-5.5",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(reply.choices[0].message.content)

except APIStatusError as error:
    try:
        body = error.response.json().get("error") or {}
    except ValueError:
        body = {}

    code = body.get("code", "unknown")

    # Kilidify sends a Persian message alongside the English one, so a
    # Persian-speaking user can be shown the real reason without translating.
    print(f"status {error.status_code}, code {code}", file=sys.stderr)
    print(f"  en: {body.get('message', '(none)')}", file=sys.stderr)
    print(f"  fa: {body.get('message_fa', '(none)')}", file=sys.stderr)

    if code in TOP_UP_NEEDED:
        print("\n-> Needs money, not a retry.", file=sys.stderr)
    elif code == "budget_exceeded":
        print("\n-> This key is capped; the wallet may still have credit.", file=sys.stderr)
    elif code == "model_not_allowed":
        print("\n-> Key restricted. GET /v1/models with it lists what it may use.", file=sys.stderr)
    elif code in RETRYABLE:
        print("\n-> Retry with backoff.", file=sys.stderr)
    else:
        raise
