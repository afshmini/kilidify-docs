# Billing

## The short version

You pay in rial. Your balance is held in dollars. Each request costs the model's
own per-token price plus a service fee, and nothing else. There is no
subscription, no monthly minimum, and no charge for a request that failed before
reaching the provider.

## How a request becomes a charge

1. **Before forwarding**, the gateway checks that the key is valid, that the
   account has balance, that the key is inside its monthly budget and rate
   limit, and that the key may use the model asked for. A request that fails any
   of these is refused and costs nothing.
2. **The request is forwarded** to the upstream provider and an amount is
   reserved against your balance, so two requests in flight at once cannot
   together overspend it. This is the `reserved_usd` you see in
   `GET /v1/credits`.
3. **When the provider answers**, the real token counts are known and the actual
   cost replaces the reservation. The ledger records the model, the token
   counts, the cost and the time.

Because step 1 happens before anything is forwarded, an empty wallet produces a
`402` rather than a debt. You cannot be taken below zero.

## The dollar rate

Wallet credit is held in US dollars because that is what the upstream providers
bill in. Top-ups are paid in rial.

- The rate is read from the free market and refreshed every five minutes.
- The rate used for a top-up is **recorded on that transaction** and is not
  re-applied afterwards. If the rate moves tomorrow, the dollars you already
  bought are still your dollars.
- Prices shown in the panel and on the pricing page are converted at the current
  rate for display, so they move with it. The dollars in your wallet do not.

## What a request costs

Per token, at the model's own input and output prices, plus a service fee.

**The `pricing` field in `/v1/models` already includes that fee**, so it is the
figure you will be billed and not a list price to mark up yourself. The numbers
are per token; multiply by a million to get the usual unit.
`anthropic/claude-sonnet-5.5` reports `0.0000023` input and `0.0000115` output,
which is $2.30 and $11.50 per million.

[The calculator](https://kilidify.com/calculator) turns a workload into toman if
you would rather not do the arithmetic.

Output tokens cost several times input tokens on nearly every model. The
practical consequence: a long prompt with a short answer is cheap, and a short
prompt with a long answer is not. If a bill is higher than expected, the
generation length is the first thing to look at, not the prompt size.

## Keeping a lid on it

Each key carries three independent controls, all visible in `GET /v1/credits`:

| Control | Field | What it does |
| --- | --- | --- |
| Monthly budget | `monthly_budget_usd` | Caps what this key can spend in a month, independently of the wallet. Exceeding it returns `402 budget_exceeded` while other keys keep working. |
| Rate limit | `rate_limit_rpm` | Caps requests per minute for this key. Exceeding it returns `429 rate_limit_exceeded`. |
| Permitted models | `allowed_models` | Restricts which models the key may use. `null` means unrestricted. |

This is the mechanism for giving a key to a client application, a teammate or a
cron job without exposing the whole balance. A per-key budget is the difference
between a runaway loop costing a few dollars and it costing all of them.

There is also a separate wallet-level protection: a low balance notification,
which re-arms each time money arrives.

## Reading your usage

- `GET /v1/credits` for the current balance, reservation and limits.
- The usage report in the panel for per-request history: model, tokens, cost,
  time.
- The Telegram bot for balance and usage without opening the panel.

What is recorded per request is the model name, the token counts, the cost and
the timestamp. The content of requests and responses is not stored, which is
also why the usage report can tell you what a request cost but not what it said.

## Refunds and corrections

Money entering a wallet is idempotent and ledgered, whether it came from a bank
gateway or from an operator correcting something by hand. Every movement has an
entry, so a balance can always be explained by the entries that produced it. If
a balance looks wrong, a support ticket in the panel can be answered against
that ledger.
