# Examples

Every file here is runnable as-is. All of them read the key from
`KILIDIFY_API_KEY` and the model from `MODEL`, so nothing has a credential in
it.

```bash
export KILIDIFY_API_KEY=kl_live_…        # from https://kilidify.com/api-keys
```

| File | What it shows |
| --- | --- |
| [`curl/chat.sh`](curl/chat.sh) | One completion, no SDK. |
| [`curl/stream.sh`](curl/stream.sh) | Streaming, unwrapping the server-sent events by hand. |
| [`curl/credits.sh`](curl/credits.sh) | Balance, limits and permitted models. |
| [`curl/models.sh`](curl/models.sh) | The catalogue as a sorted table, priced per million tokens. Works with no key. |
| [`python/chat.py`](python/chat.py) | OpenAI SDK, one completion, with token usage. |
| [`python/stream.py`](python/stream.py) | OpenAI SDK, streaming. |
| [`python/anthropic_sdk.py`](python/anthropic_sdk.py) | The official Anthropic SDK against Kilidify. |
| [`python/handle_errors.py`](python/handle_errors.py) | Branching on error codes properly. |
| [`node/chat.mjs`](node/chat.mjs) | OpenAI SDK, one completion. |
| [`node/stream.mjs`](node/stream.mjs) | OpenAI SDK, streaming. |
| [`node/anthropic-sdk.mjs`](node/anthropic-sdk.mjs) | The official Anthropic SDK against Kilidify. |
| [`node/credits.mjs`](node/credits.mjs) | Plain `fetch`, no SDK, including the error path. |

## The one thing to get right

The two SDKs want different base URLs, and mixing them up is the most common
setup mistake:

| SDK | Base URL | Why |
| --- | --- | --- |
| OpenAI | `https://api.kilidify.com/v1` | It appends paths to what you give it. |
| Anthropic | `https://api.kilidify.com` | It appends `/v1/messages` itself. |

Give either one the other's URL and you get a 404 with a doubled `/v1` in the
path.

## Start without a key

`curl/models.sh` needs no credential, so it is the quickest way to confirm the
gateway is reachable from where you are:

```bash
./curl/models.sh claude
```
