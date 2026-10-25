#!/usr/bin/env bash
# A streaming completion. The chunks are ordinary server-sent events, so this
# works with any SSE-aware client; jq is used here only to unwrap them.
#   KILIDIFY_API_KEY=kl_live_… ./stream.sh "your prompt"
set -euo pipefail
: "${KILIDIFY_API_KEY:?set KILIDIFY_API_KEY to your kl_live_… key}"
PROMPT="${1:-Count to five.}"
MODEL="${MODEL:-anthropic/claude-sonnet-5.5}"

curl -sS -N https://api.kilidify.com/v1/chat/completions \
  -H "Authorization: Bearer $KILIDIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg m "$MODEL" --arg p "$PROMPT" \
        '{model: $m, messages: [{role: "user", content: $p}], stream: true}')" \
  | while IFS= read -r line; do
      [[ "$line" == data:* ]] || continue
      payload="${line#data: }"
      [[ "$payload" == "[DONE]" ]] && break
      printf '%s' "$(jq -r '.choices[0].delta.content // empty' <<<"$payload")"
    done
echo
