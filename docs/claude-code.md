# Claude Code through Kilidify

Claude Code talks to whatever `ANTHROPIC_BASE_URL` points at, using the
Anthropic Messages API. Kilidify's gateway answers that API, so Claude Code runs
against your rial-funded wallet with no patching and no proxy of your own.

The full command reference lives with the package, which is the source of truth
and is versioned with the tool:
**[`@kilidify/claude` on npm](https://www.npmjs.com/package/@kilidify/claude)**.
This page is the short path plus the things people get stuck on.

## Install and run

```bash
npm install -g @anthropic-ai/claude-code @kilidify/claude

kilidify login     # paste your kl_live_… key
kilidify           # starts Claude Code through Kilidify
```

Anything you would pass to `claude` works:

```bash
kilidify -p "explain this repository"
kilidify -- --model opus         # everything after -- goes to claude unchanged
```

## Make it permanent

```bash
kilidify setup              # ~/.claude/settings.json, all projects
kilidify setup --project    # .claude/settings.local.json, this project only
kilidify setup --mcp        # also register the MCP server
kilidify setup --undo       # remove what setup wrote
```

After `setup`, plain `claude` goes through Kilidify. It merges into the existing
settings file, preserves every other setting, and writes a backup beside it
first.

**Install globally before running `setup`.** It configures an `apiKeyHelper`
that shells out to `kilidify key`, so if that command lives in a temporary
`npx` cache the helper stops working when the cache is cleared. The symptom is
Claude Code reporting that your `apiKeyHelper` script is failing.

The helper exists so the key stays in Kilidify's own config file, owner-readable
only at `0600`, instead of being written into Claude Code's settings. If you
would rather have it inline, `setup --plain-key` does that.

## Letting Claude see your balance

```bash
kilidify setup --mcp
```

That registers an MCP server exposing `kelid_balance`,
`kelid_exchange_rate`, `kelid_search_models` and `kelid_estimate_cost`, so
Claude itself can answer "what is this going to cost" and "what is my balance"
mid-session. The server re-reads the stored key on every call, so a fresh
`kilidify login` takes effect without restarting Claude Code.

## Checking the setup

```bash
kilidify status     # gateway reachable, key valid, balance in USD and toman, live rate
kilidify models     # Claude models with per-million prices in both currencies
```

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| Claude Code opens its login screen | No credential reached it. Run `kilidify`, or `kilidify setup` to make it permanent. |
| "Your apiKeyHelper script is failing" | The helper path moved, usually an `npx` cache or a reinstall. Install globally, then re-run `kilidify setup`. |
| `401`, invalid API key | Key wrong or revoked. `kilidify login` again. |
| `402 not_provisioned` | The account has no upstream access until its first top-up. |
| `402 insufficient_balance` | Wallet empty. Top up. |
| `403 model_not_allowed` | The key is restricted. Change the key's permitted models, or the model mapping with `kilidify config set model.sonnet …`. |
| `/model` lists no gateway models | Discovery has a three-second timeout and falls back to the built-in list. Aliases still resolve through your model mapping, so this is cosmetic. |
| Web fetch or `/fast` report connectivity errors | Those checks go to `api.anthropic.com` directly rather than through the gateway. Inference is unaffected. |

That last row is the one that alarms people unnecessarily: some of Claude Code's
own auxiliary features phone home to Anthropic regardless of
`ANTHROPIC_BASE_URL`, and from Iran those calls fail. Your actual requests are
not affected. `kilidify config set nonessential on` turns off the traffic that
goes outside the gateway.

## How it works

Claude Code sends Anthropic Messages requests to `ANTHROPIC_BASE_URL`. Kilidify
accepts them on `/v1/messages`, checks the key, the rate limit and the wallet,
forwards the request upstream using your own spend-capped upstream key, streams
the response straight back, and bills your wallet from the token counts and cost
the provider reports.

Because the error shape matters to Claude Code's retry logic, Kilidify returns
Anthropic-shaped errors for Anthropic-shaped requests and relays upstream errors
byte for byte. See [`errors.md`](errors.md).

## Without the package

The package is a convenience, not a requirement. Two environment variables are
the whole mechanism:

```bash
export ANTHROPIC_BASE_URL=https://api.kilidify.com
export ANTHROPIC_AUTH_TOKEN=kl_live_…
claude
```

Model aliases such as `opus` and `sonnet` will not resolve to Kilidify model ids
this way, so name models in full, for example
`claude --model anthropic/claude-sonnet-5.5`. The mapping is most of what the
package adds.
