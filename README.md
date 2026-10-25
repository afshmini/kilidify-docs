<p align="center">
  <img src="https://kilidify.com/icon.png" width="76" height="76" alt="Kilidify">
</p>

<h1 align="center">Kilidify</h1>

<p align="center">
  <strong>An AI gateway for developers in Iran.</strong><br>
  One OpenAI-compatible API for several hundred models, paid for in Iranian rial.
</p>

<p align="center">
  <a href="https://kilidify.com">kilidify.com</a> ·
  <a href="https://kilidify.com/docs">Docs</a> ·
  <a href="https://kilidify.com/pricing">Pricing</a> ·
  <a href="README.fa.md">فارسی</a>
</p>

---

Kilidify (Persian: کلیدیفای) is a hosted API gateway. One key and one base URL
reach models from Anthropic, OpenAI, Google, Meta, DeepSeek, Mistral, Z.ai,
Qwen and others. Accounts are funded in Iranian rial through domestic bank
gateways, so no international payment card and no foreign bank account is
involved.

It exists because the providers themselves do not sell to Iran. Developers there
are left choosing between a card they cannot get and an account reseller who
sells a shared login. Kilidify is neither: it is a metered API with your own
key, your own balance and your own usage report.

Kilidify does not train or host models. It resells upstream capacity and owns
the billing, the rial payment path and the per-key spending controls.

## Quickstart

The base URL is `https://api.kilidify.com/v1`. Point any OpenAI-compatible
client at it and change the key. Nothing else in existing code changes.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key="kl_live_…",            # from https://kilidify.com/api-keys
)

reply = client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "سلام!"}],
    stream=True,
)

for chunk in reply:
    print(chunk.choices[0].delta.content or "", end="")
```

Runnable versions in [`examples/`](examples/): curl, Python, Node, and the
Anthropic SDK.

## It speaks two API shapes, not one

Most gateways give you an OpenAI-compatible endpoint and stop there. Kilidify
also answers the **Anthropic Messages API**, so the Anthropic SDKs and Claude
Code work against it directly rather than through a translation layer.

| You send | Kilidify replies in |
| --- | --- |
| `POST /v1/chat/completions` | the OpenAI shape |
| `POST /v1/messages`, or any request with an `anthropic-version` header | the Anthropic shape |

Errors follow the same rule, which matters more than it sounds: Claude Code
retries on the wording of upstream errors, so a gateway that returns the wrong
error shape breaks its retry logic silently.

## Claude Code, billed in rial

```bash
npm install -g @anthropic-ai/claude-code @kilidify/claude

kilidify login     # paste your kl_live_… key
kilidify           # starts Claude Code through Kilidify
```

`kilidify setup` makes it permanent, so plain `claude` goes through Kilidify
afterwards. The key is held in Kilidify's own `0600` config file and read
through an `apiKeyHelper`, rather than written into Claude Code's settings.

Full guide: [`docs/claude-code.md`](docs/claude-code.md) ·
package: [`@kilidify/claude`](https://www.npmjs.com/package/@kilidify/claude)

## How it works

| | |
| --- | --- |
| **Interface** | OpenAI-compatible and Anthropic Messages. Chat completions, streaming, model listing, plus everything else in the upstream surface, forwarded verbatim. |
| **Payment** | Funded in Iranian rial through domestic bank gateways. Card details are entered on the bank's own page and never reach Kilidify. |
| **Billing** | Per token, at the model's own rate plus a service fee. Wallet credit is held in US dollars and converted at the free-market rate, refreshed every five minutes. The rate used for a top-up is recorded on that transaction and is not re-applied later. |
| **Spending limits** | Every API key carries its own monthly budget, requests-per-minute limit and list of permitted models. Balance is checked before a request is forwarded, so an empty wallet stops requests instead of running up a debt. |
| **Privacy** | Request and response content is not stored. Only the model name, token counts, cost and timestamp are recorded, which is what the usage report and the invoice are built from. |

## Endpoints

| Method | Path | Auth | Returns |
| --- | --- | --- | --- |
| `GET` | `/v1/models` | optional | The catalogue. Without a key, everything served. With a key, only the models that key may use. |
| `POST` | `/v1/chat/completions` | required | OpenAI-shaped completion, streaming supported. |
| `POST` | `/v1/messages` | required | Anthropic-shaped message, streaming supported. |
| `GET` | `/v1/credits` | required | Balance, reserved and available amounts, RPM limit, monthly budget, permitted models. |
| `GET` | `/v1/me` | required | Same payload as `/v1/credits`. |

Anything else under `/v1` is forwarded to the upstream provider unchanged, so a
new upstream endpoint works the day it ships.

```bash
curl https://api.kilidify.com/v1/credits \
  -H "Authorization: Bearer kl_live_…"
```

```json
{
  "data": {
    "user_id": 42,
    "balance_usd": "12.40",
    "reserved_usd": "0.02",
    "available_usd": "12.38",
    "rate_limit_rpm": 60,
    "monthly_budget_usd": "50",
    "allowed_models": null
  }
}
```

`allowed_models` is `null` when the key is unrestricted. A key may send its
credential as `Authorization: Bearer …` or as `x-api-key`, whichever the client
already does.

## Models

Several hundred, listed live at [kilidify.com/pricing](https://kilidify.com/pricing)
with per-million input and output prices in toman. Identifiers are the upstream
ones, so code written against another gateway usually needs no edit:

```
anthropic/claude-opus-5.5        openai/gpt-5-nano
anthropic/claude-sonnet-5.5      google/gemini-4-argon
anthropic/claude-haiku-5.5       deepseek/deepseek-v4-flash
z-ai/glm-5.3-flash               qwen/qwen3.7-flash
```

A `:batch` suffix selects the upstream batch tier where one exists, for example
`anthropic/claude-haiku-5.5:batch`.

`kilidify/auto` picks a model per role from the mapping configured for that key.
It is offered only to keys that have such a mapping; see
[`docs/models.md`](docs/models.md).

## Errors

Gateway errors carry a machine-readable `code` and a Persian `message_fa`
alongside the English one, so the same response can be shown to a Persian
speaker without a second lookup. Errors from the upstream provider are relayed
byte for byte and are not rewritten.

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

Every code, with its status and what to do about it:
[`docs/errors.md`](docs/errors.md).

## Documentation

| | |
| --- | --- |
| [`docs/quickstart.md`](docs/quickstart.md) | Account, key, first request, in any of four languages. |
| [`docs/claude-code.md`](docs/claude-code.md) | Claude Code, permanent setup, MCP tools, troubleshooting. |
| [`docs/models.md`](docs/models.md) | Choosing a model, `kilidify/auto`, batch tiers, per-key restrictions. |
| [`docs/billing.md`](docs/billing.md) | How a request becomes a charge, the dollar rate, budgets and limits. |
| [`docs/errors.md`](docs/errors.md) | Every error code and the fix. |
| [`docs/faq.md`](docs/faq.md) | The questions people actually ask first. |

## Tools

- **[`@kilidify/claude`](https://www.npmjs.com/package/@kilidify/claude)**, the
  Claude Code launcher and MCP server.
- **VS Code extension**, from [kilidify.com/apps](https://kilidify.com/apps).
- **Telegram bot**, to chat with any model in the catalogue from Telegram,
  billed to the same wallet. Connect it from the panel. Worth knowing before
  you use it: Telegram bots have no end-to-end encryption, so messages exist in
  plaintext on Telegram's servers. The bot says so itself on `/start`.

## Status and support

This repository is the public documentation. The product runs at
[kilidify.com](https://kilidify.com); the service code is not open source.

Corrections and additions to these docs are welcome as issues or pull requests.
For account, billing or key problems, use the support tickets in the panel,
which are tied to your account; a GitHub issue is not.

## License

Documentation and examples: [MIT](LICENSE). Copy the examples into your own
project freely.
