# FAQ

### Do I need an international credit card?

No. That is the point of the service. You top up through an Iranian bank gateway
in rial, and the credit lands in your wallet in US dollars. Card details are
entered on the bank's own page and never reach Kilidify.

### Is this an account reseller? Am I sharing a login?

No. You get your own API key, your own balance and your own usage report, and
you are billed per token for what you use. Nothing is shared with another
customer.

### Is it an OpenRouter reseller?

Kilidify routes to upstream providers and adds the layer that does not exist for
customers in Iran: rial payment through local gateways, billing and invoices in
toman, a Persian interface, and per-key spending controls. The inference is not
what it adds; the payment and accounting path is.

### Which models can I use?

Several hundred, from Anthropic, OpenAI, Google, Meta, DeepSeek, Mistral, Z.ai,
Qwen and others. `GET /v1/models` lists them live, and
[kilidify.com/pricing](https://kilidify.com/pricing) shows prices in toman. See
[`models.md`](models.md).

### Will my existing code work?

If it speaks the OpenAI API, change the base URL and the key. If it speaks the
Anthropic Messages API, change the base URL and the key. Both are answered
natively, so the official SDKs for both work without a shim. Model ids are the
upstream ones, so they usually need no editing either.

### How is the cost calculated?

Per token, at the model's own input and output prices, plus a service fee.
Output tokens cost several times input tokens on most models, so generation
length drives a bill more than prompt length does. See [`billing.md`](billing.md).

### Where does the dollar rate come from?

The free market, refreshed every five minutes. The rate used for a top-up is
recorded on that transaction and is not re-applied later, so the dollars you
already bought stay yours regardless of what the rate does afterwards.

### What happens if my balance runs out?

Requests stop with `402 insufficient_balance`. The balance is checked before a
request is forwarded, so you are never charged beyond it and never taken below
zero. Retrying will not help until you top up.

### Can I cap what a key spends?

Yes, and this is worth setting up before you need it. Every key has its own
monthly budget, requests-per-minute limit and list of permitted models,
independent of the wallet. That is what makes a key safe to embed in a client
application or hand to a teammate. See [`billing.md`](billing.md).

### Are my requests and responses stored?

No. Only the model name, token counts, cost and timestamp are recorded, which is
what the invoice and the usage report are built from. This is also why the usage
report can tell you what a request cost but not what it contained.

### Is there a free trial?

Sometimes. When an offer is open the panel says so at sign-up. Trial keys are
restricted to a few inexpensive models, so an unexpected `model_not_allowed` on
a new account usually means a trial key and a model outside the list.

### Does streaming work?

Yes, in both API shapes, as ordinary server-sent events. Any client that already
handles OpenAI or Anthropic streaming handles this.

### Does Claude Code work?

Yes, and it is a first-class path rather than a workaround, since the gateway
answers the Anthropic Messages API directly. See
[`claude-code.md`](claude-code.md).

### Is there a rate limit?

Per key, in requests per minute, visible as `rate_limit_rpm` in
`GET /v1/credits`. There is also a cap on simultaneous in-flight requests per
account, which returns `429 concurrency_limit_exceeded` and clears as soon as
one finishes.

### Is the service open source?

The documentation and examples in this repository are MIT. The service itself is
not open source.

### Something is wrong with my account. Where do I go?

Support tickets in the panel, which are tied to your account and can be answered
against your ledger. A GitHub issue on this repository cannot: this repo is
documentation, and nobody reading it can see your balance. Use issues here for
corrections to the docs.
