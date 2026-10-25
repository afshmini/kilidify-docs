# Errors

Two rules worth knowing before the table.

**Kilidify's own errors are reshaped to match your client; the upstream's are
not.** A request that fails at the gateway (bad key, no balance, model not
permitted, rate limit) comes back in the shape your client expects. A request
that reached the provider and failed there is relayed byte for byte, because
clients match on the upstream's own wording. Claude Code in particular decides
whether to retry from the text of the upstream error, so rewriting it would
break retries silently.

**Every gateway error carries a Persian message.** `message_fa` sits alongside
`message`, so a Persian-speaking user can be shown the real reason without a
second translation step.

## The two shapes

Which one you get depends on the request, not on a setting. A request counts as
Anthropic if its path starts `/v1/messages` or it carries an `anthropic-version`
header. Everything else gets the OpenAI shape.

OpenAI shape:

```json
{
  "error": {
    "code": "insufficient_balance",
    "message": "Insufficient balance. Top up your wallet to continue.",
    "message_fa": "موجودی کیف پول شما کافی نیست. لطفاً حساب خود را شارژ کنید.",
    "type": "insufficient_quota"
  }
}
```

Anthropic shape, same condition:

```json
{
  "type": "error",
  "error": {
    "type": "billing_error",
    "code": "insufficient_balance",
    "message": "Insufficient balance. Top up your wallet to continue.",
    "message_fa": "موجودی کیف پول شما کافی نیست. لطفاً حساب خود را شارژ کنید."
  }
}
```

The `code` is the same in both and is the field to branch on. The `type` differs
because each ecosystem names its categories differently; in the Anthropic shape
it is derived from the HTTP status (401 becomes `authentication_error`, 402
becomes `billing_error`, and so on).

## Every code

### Authentication, 401

| Code | Meaning | Fix |
| --- | --- | --- |
| `no_api_key` | No credential on the request. | Send `Authorization: Bearer kl_live_…` or `x-api-key`. |
| `invalid_api_key` | No such key. | Check for a truncated paste. Keys are shown once at creation. |
| `key_revoked` | The key was revoked. | Create a new one in the panel. |
| `key_expired` | The key passed its expiry date. | Create a new one, or extend it in the panel. |

### Payment and quota, 402

These mean the request was understood and refused for money, not for form.
Nothing was charged.

| Code | Meaning | Fix |
| --- | --- | --- |
| `not_provisioned` | The account has no upstream access yet. | Add credit; access is provisioned when the first money lands. |
| `insufficient_balance` | The wallet cannot cover the request. | Top up. Balance is checked before forwarding, so you are never taken below zero. |
| `budget_exceeded` | This key hit its own monthly budget, even though the wallet has money. | Raise or clear the key's budget in the panel, or use another key. |
| `trial_tokens_exhausted` | The free trial allowance is spent. | Top up to continue. |

### Permission, 403

| Code | Meaning | Fix |
| --- | --- | --- |
| `account_suspended` | The account is suspended. | Open a support ticket in the panel. |
| `model_not_allowed` | This key may not use the model asked for. | Check the key's permitted models. `GET /v1/models` with the key lists exactly what it may use. A trial key is restricted to a few inexpensive models. |

### Request, 400 / 408 / 413

| Code | Status | Meaning |
| --- | --- | --- |
| `invalid_body` | 400 | The body could not be parsed. |
| `auto_not_configured` | 400 | `kilidify/auto` was requested on a key with no role mapping. Choose a model per role in the panel, or name a model directly. |
| `request_timeout` | 408 | The body did not arrive in time. |
| `payload_too_large` | 413 | The body exceeds the accepted size. |

### Rate limits, 429

| Code | Meaning | Fix |
| --- | --- | --- |
| `rate_limit_exceeded` | The key's requests-per-minute limit. | Back off and retry. The limit is per key and visible in `GET /v1/credits` as `rate_limit_rpm`. |
| `concurrency_limit_exceeded` | Too many requests in flight at once for the account. | Retry when one finishes. This counts simultaneous requests, not a rate, so waiting a moment is the whole fix. |

### Upstream and internal, 500 / 502 / 504

| Code | Status | Meaning |
| --- | --- | --- |
| `internal_error` | 500 | A fault on our side. Safe to retry. |
| `upstream_unavailable` | 502 | The provider is unreachable. |
| `upstream_timeout` | 504 | The provider accepted the request and did not answer in time. |

A 502 or 504 is worth retrying once or twice with a short backoff. If one model
is consistently unavailable while others are fine, it is usually upstream
capacity rather than anything about your account.

## Handling them in code

Branch on `code`, never on `message`. The messages are written for people and
are translated; the codes are the contract.

```python
from openai import OpenAI, APIStatusError

client = OpenAI(base_url="https://api.kilidify.com/v1", api_key=key)

try:
    reply = client.chat.completions.create(model=model, messages=messages)
except APIStatusError as error:
    code = (error.response.json().get("error") or {}).get("code")

    if code in ("insufficient_balance", "trial_tokens_exhausted"):
        ...   # tell the user to top up; retrying will not help
    elif code == "budget_exceeded":
        ...   # this key is capped; the wallet may still have money
    elif code == "model_not_allowed":
        ...   # pick a permitted model
    elif code in ("rate_limit_exceeded", "concurrency_limit_exceeded"):
        ...   # back off and retry
    elif code in ("upstream_unavailable", "upstream_timeout", "internal_error"):
        ...   # retry with backoff
    else:
        raise
```

The three groups that matter operationally: **402 never succeeds on retry**,
**429 always will eventually**, and **5xx usually will.** Treating all failures
as retryable turns an empty wallet into a tight loop against an endpoint that
will keep refusing.
