# Quickstart

Five minutes from nothing to a streaming answer.

## 1. Account and key

1. Create an account at [kilidify.com/register](https://kilidify.com/register).
   An email address is enough; no card is asked for at sign-up.
2. Top up the wallet from the panel, through an Iranian bank gateway. The
   amount is paid in rial and the credit lands in your wallet in US dollars at
   that moment's free-market rate, which is recorded on the transaction.
3. Create a key at [kilidify.com/api-keys](https://kilidify.com/api-keys). It
   looks like `kl_live_…` and is shown once.

While a free trial is running you may be able to skip step 2; the panel says so
if an offer is open. A trial key is restricted to a few inexpensive models, so
if a model you ask for comes back `model_not_allowed`, that is why.

## 2. Point a client at it

The base URL is `https://api.kilidify.com/v1`, and the key goes in either
`Authorization: Bearer …` or `x-api-key`. Use whichever your library already
sends; both are accepted everywhere.

### curl

```bash
curl https://api.kilidify.com/v1/chat/completions \
  -H "Authorization: Bearer $KILIDIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-5.5",
    "messages": [{"role": "user", "content": "Say hello in Persian."}]
  }'
```

### Python, OpenAI SDK

```bash
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.kilidify.com/v1",
    api_key=os.environ["KILIDIFY_API_KEY"],
)

reply = client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "Say hello in Persian."}],
)
print(reply.choices[0].message.content)
```

### Node, OpenAI SDK

```bash
npm install openai
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.kilidify.com/v1",
  apiKey: process.env.KILIDIFY_API_KEY,
});

const reply = await client.chat.completions.create({
  model: "anthropic/claude-sonnet-5.5",
  messages: [{ role: "user", content: "Say hello in Persian." }],
});

console.log(reply.choices[0].message.content);
```

### Python, Anthropic SDK

Kilidify answers the Anthropic Messages API too, so the official SDK works with
only a base URL change.

```bash
pip install anthropic
```

```python
import os
from anthropic import Anthropic

client = Anthropic(
    base_url="https://api.kilidify.com",     # no /v1 here; the SDK adds it
    api_key=os.environ["KILIDIFY_API_KEY"],
)

message = client.messages.create(
    model="anthropic/claude-sonnet-5.5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello in Persian."}],
)
print(message.content[0].text)
```

Note the base URL: the OpenAI SDK wants `https://api.kilidify.com/v1` because it
appends paths to it, while the Anthropic SDK wants `https://api.kilidify.com`
because it adds `/v1/messages` itself. Giving either one the other's URL
produces a 404 with a doubled `/v1` in the path, which is the single most common
setup mistake.

## 3. Check it is really you

```bash
curl https://api.kilidify.com/v1/credits -H "Authorization: Bearer $KILIDIFY_API_KEY"
```

If that returns a balance, the key works. If it returns `401 invalid_api_key`,
the key is wrong or revoked; `402 not_provisioned` means the account has no
upstream access yet and needs credit.

## 4. Streaming

Both shapes stream. With the OpenAI SDK, pass `stream=True` and iterate; the
chunks are standard server-sent events, so any client that already handles
OpenAI streaming handles this.

```python
for chunk in client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "Count to five."}],
    stream=True,
):
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

Runnable files for all of the above are in [`../examples/`](../examples/).

## What to read next

- [`models.md`](models.md) to choose a model and understand `kilidify/auto`.
- [`billing.md`](billing.md) for how a request turns into a charge.
- [`errors.md`](errors.md) when something returns a code you do not recognise.
- [`claude-code.md`](claude-code.md) to use Claude Code against your wallet.
