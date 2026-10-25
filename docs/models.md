# Models

## Finding out what is available

```bash
curl https://api.kilidify.com/v1/models
```

That works without a key and lists everything Kilidify serves, several hundred
models. Each entry carries `id`, `name`, `display_name`, `description` and
`pricing`.

Send a key and the answer changes: you get only the models that key is
permitted to use.

```bash
curl https://api.kilidify.com/v1/models -H "Authorization: Bearer $KILIDIFY_API_KEY"
```

This is the quickest way to diagnose a `model_not_allowed`. If the model is
absent from the keyed listing, the key is restricted, and the panel is where
that is changed. A trial key is restricted to a few inexpensive models by
design.

The human version of the same catalogue, with prices in toman at today's rate,
is at [kilidify.com/pricing](https://kilidify.com/pricing). There is a
side-by-side comparison at [kilidify.com/compare](https://kilidify.com/compare)
and a cost estimator at
[kilidify.com/calculator](https://kilidify.com/calculator).

## Identifiers

Model ids are the upstream ones, `provider/model`, so code written against
another gateway usually moves across unchanged:

```
anthropic/claude-opus-5.5        openai/gpt-5-nano
anthropic/claude-sonnet-5.5      google/gemini-4-argon
anthropic/claude-haiku-5.5       deepseek/deepseek-v4-flash
z-ai/glm-5.3-flash               qwen/qwen3.7-flash
```

The catalogue tracks upstream, so a newly released model generally appears
without anything being deployed here. Do not hardcode a list of ids in your
application; read `/v1/models` instead, or you will be the last to get a new
model and the first to break when an old one is retired.

### Batch tier

A `:batch` suffix selects the provider's batch tier where one exists, for
example `anthropic/claude-haiku-5.5:batch`. It is cheaper per token and slower,
which suits work with no one waiting on it. Not every model has one; the
catalogue shows which do.

### Floating `latest` aliases

A handful of ids begin with `~` and end in `-latest`, for example
`~anthropic/claude-sonnet-latest` or `~deepseek/deepseek-flash-latest`. Each
tracks the newest model in its family, so you get upgrades without editing code.

The tradeoff is the usual one: what answers you today may not be what answers
you next month, and the price can move with it. Use an alias for exploratory
work and a pinned id for anything whose behaviour or cost you need to hold
still.

### Prices in the catalogue already include the service fee

`pricing.prompt` and `pricing.completion` are per-token US dollar figures, and
they are what you will actually be billed: the service fee is already applied.
There is no second multiplication to do.

Per token is awkward to read, so multiply by a million for the unit everyone
quotes. `anthropic/claude-sonnet-5.5` reports `0.0000023` and `0.0000115`, which
is $2.30 per million input tokens and $11.50 per million output.
[`examples/curl/models.sh`](../examples/curl/models.sh) does that conversion and
prints a sorted table.

## `kilidify/auto`

`kilidify/auto` is not a model. It is an alias that resolves, per request, to
whichever model you mapped to that role for the key being used.

It is useful when you want the choice of model to be configuration rather than
code: a script asks for `kilidify/auto`, and which model answers is decided in
the panel, without a redeploy.

Two things to know:

- It is only offered to keys that have a role mapping. The catalogue hides it
  from keys without one, and asking for it on such a key returns
  `400 auto_not_configured`.
- Because it can resolve differently over time, it is a poor choice when you
  need reproducibility. Name the model directly for anything you intend to
  compare across runs.

## Choosing one

A rough guide rather than a ranking, since the catalogue moves:

| If you want | Reach for |
| --- | --- |
| The strongest reasoning, cost secondary | an Opus-tier or flagship model |
| Everyday coding and agent work | a Sonnet-tier model |
| High volume, latency-sensitive, or classification | a Haiku-tier or flash model |
| The cheapest acceptable answer | one of the flash models, for example `z-ai/glm-5.3-flash` or `openai/gpt-5-nano` |

The `pricing` field in `/v1/models` is the authority on cost, and
[the calculator](https://kilidify.com/calculator) turns a workload into a number
in toman. Output tokens cost several times input tokens on most models, so a
prompt-heavy workload is far cheaper than its token count suggests and a
generation-heavy one is dearer.

## Per-key restrictions

Each key carries its own list of permitted models, alongside its monthly budget
and requests-per-minute limit. Reading the current state of a key:

```bash
curl https://api.kilidify.com/v1/credits -H "Authorization: Bearer $KILIDIFY_API_KEY"
```

`allowed_models` is `null` when the key is unrestricted, or an array naming
exactly what it may use. This is the mechanism to reach for when you want a
key embedded in a client application, or handed to someone else, to be unable
to spend your balance on the most expensive model in the catalogue.

One caveat worth stating plainly: the permitted list is fixed when the key is
created. Widening the models a restricted key may use means issuing a new key,
not editing the old one.
