#!/usr/bin/env bash
# One completion, the OpenAI shape.
#   KILIDIFY_API_KEY=kl_live_… ./chat.sh "your prompt"
set -euo pipefail
: "${KILIDIFY_API_KEY:?set KILIDIFY_API_KEY to your kl_live_… key}"
PROMPT="${1:-Say hello in Persian.}"
MODEL="${MODEL:-anthropic/claude-sonnet-5.5}"

curl -sS https://api.kilidify.com/v1/chat/completions \
  -H "Authorization: Bearer $KILIDIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg m "$MODEL" --arg p "$PROMPT" \
        '{model: $m, messages: [{role: "user", content: $p}]}')" \
  | jq -r '.choices[0].message.content'
